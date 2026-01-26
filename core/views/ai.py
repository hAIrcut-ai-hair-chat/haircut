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
from core.models.ai import AskAi, UserImageAiQuestion
from core.services import HuggingFaceChatService
from core.models import UserAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer, AskAiSerializer

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
    def ask_ai(self, request) -> str:
        ask_ai_serializer = AskAiSerializer(data=request.data)
        ask_ai_serializer.is_valid(raise_exception=True)
        question_uuid = ask_ai_serializer.validated_data.pop("question_uuid")

        question = UserImageAiQuestion.objects.filter(uuid=question_uuid)
        if not question:
            return Response({"message": "Question didn't exists"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            ai_response = hf_chat.ask(question=question.user_ai_question_uuid.question)
        except Exception as error:
            return Response({"message": f"There's error in hf chat service \n {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #"attachment_uuid", "ai_response", "created_at", "question_uuid"
        serialized_instance = {
            "question_uuid": question,
            "ai_response": ai_response
        }
        
        ask_ai_serializer.save(serialized_instance)
        
        return Response(
            {
                
                "message": "New question created with succesfully",
                "ai_response": str(ask_ai_serializer.ai_question)
            }, status=status.HTTP_201_CREATED
        )
        
 
class AskAiViewSet(ModelViewSet):
     queryset = AskAi
     serializer_class = AskAiSerializer