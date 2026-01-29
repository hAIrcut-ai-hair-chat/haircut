from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView

import requests
import os

from core.models import UserAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer
from core.services import GeminiService

gemini_service = GeminiService()

django_url = os.getenv("BACKEND_URL")
print(django_url)

class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        serializer = UserAiQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data.pop("image", None)
        question = serializer.save()

        attachment_key = None

        if image:
            try:
                image.seek(0)
                uploader_response = requests.post(
                    f"{django_url}/image/",
                    files={"file": image},
                    timeout=10
                )
                uploader_response.raise_for_status()
                uploader_data = uploader_response.json()
                attachment_key = uploader_data.get("attachment_key")
            except Exception as error:
                question.delete()
                raise ValidationError({"uploader": f"Upload failed: {error}"})

            try:
                image_serializer = UserImageAiQuestionSerializer(data={
                    "image": attachment_key,
                    "user_ai_question_uuid": question.uuid
                })
                image_serializer.is_valid(raise_exception=True)
                image_serializer.save()
            except Exception as error:
                question.delete()
                raise ValidationError({"db": f"Saving image info failed: {error}"})

        return Response(
            {
                "message": "Question created successfully",
                "question_uuid": question.uuid,
                "image_attachment_key": attachment_key,
            },
            status=status.HTTP_201_CREATED
        )
  
class TestAPIView(APIView):
    def post(self, request):
        
        context: str = request.data.get("context")
        
        if not context:
            return Response({"message": f"Context didn't not offered"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            gemini_response = gemini_service.generate_response(context=context, prompt=context)
        except Exception as error:
            return Response (
                {
                    "messaage": f"There's a exception with relationship gemini service: {error}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        print(gemini_response)
        if not gemini_response['success']:
            return Response({"message": f"There's a error in generate response in gemini service"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(
            {
                "message": "Gemini response generated with successfully!",
                "gemini_response": str(gemini_response['content'])
            }, status=status.HTTP_201_CREATED
        )
            