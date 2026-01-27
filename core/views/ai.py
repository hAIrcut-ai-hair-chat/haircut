from email.mime import audio
from uuid import UUID
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
import requests
import os
from core.models import ai
from core.models.ai import AskAi, UserImageAiQuestion
from core.services import HuggingFaceChatService
from core.models import UserAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer, AskAiSerializer
from rest_framework.views import APIView


django_url = os.getenv("BACKEND_URL")
hf_chat = HuggingFaceChatService()


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
            raise ValidationError({"db": f"Saving image info failed: \n {error}"})
        
        question_text = str(question.question)

        try:
            ai_response = hf_chat.ask(question=question_text)
        except Exception as e:
            raise ValidationError({"ai": f"AI request failed: {e}"})

        if not ai_response:
            raise ValidationError({"ai": "AI returned empty response"})

        ask_ai_serializer = AskAiSerializer(data={
            "question_uuid": question.uuid,
            "ai_response": ai_response
        })

        ask_ai_serializer.is_valid(raise_exception=True)
        ask_ai_serializer.save()

        return Response({
            "message": "Question to ai created with successfully",
            "question_uuid": str(question.uuid),
            "ai_response": str(ask_ai_serializer.ai_response)
        }, status=status.HTTP_201_CREATED)
 

class TestRagApiView(APIView):
    def post(self, request):
        question: str = question.data.get("question")
        user_id: str = question.data.get("user_id")
        
        if not question or not user_id:
            return Response({"message": "Question or user_id didn't offered"}, status=status.HTTP_400_BAD_REQUEST)
        
        