from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
import requests
import os
from core.services import HuggingFaceChatService


from core.models import UserAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer

django_url = os.getenv("BACKEND_URL")


class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        question_serializer = UserAiQuestionSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)

        image = question_serializer.validated_data.pop("image")
        question = question_serializer.save()

        try:
            uploader_response = requests.post(f"{django_url}/image/",files={"file": image},timeout=10)
            uploader_response.raise_for_status()
        except Exception as error:
            question.delete()
            raise ValidationError({"uploader": f"Upload failed: {error}"})

        uploader_data = uploader_response.json()

        try:
            image_serializer = UserImageAiQuestionSerializer(data={
                "image": uploader_data["attachment_key"], 
                "user_ai_question_uuid": question.uuid
                }
            )
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()
        except Exception as error:
            question.delete()
            raise ValidationError({"db": f"Saving image info failed: \n {error}"})

        return Response(
            {"message": "Question with image created successfully", "question_uuid": question.uuid}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def ask_ai(question: str) -> str:
        pass