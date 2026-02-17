from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import transaction

import requests
import os

from core.models import UserAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer
from core.tasks import celeryAiChat

django_url = os.getenv("BACKEND_URL")
class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        serializer = UserAiQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data.pop("image", None)
        prompt = serializer.validated_data.get("question", None)

        question = serializer.save()
        attachment_key = None  

        if image:
            try:
                image.seek(0)
                
                print("1")
                uploader_response = requests.post(
                    f"{django_url}/image/",
                    files={"file": image},
                    timeout=10
                )
                print("2")
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
                print(3)
                image_serializer.save()
                print(4)
            except Exception as error:
                question.delete()
                raise ValidationError({"db": f"Saving image info failed: {error}"})
            


        try:
            ai_response = celeryAiChat.delay(prompt=prompt, question_uuid=str(question.uuid))
            task_id = ai_response.id

        except Exception as error:
            question.delete()
            raise ValidationError({"ai": f"AI generation failed: {error}"})

        return Response(
            {
                "message": "Question created successfully",
                "question_uuid": question.uuid,
                "image_attachment_key": attachment_key,
                "task_id": task_id
            },
            status=status.HTTP_201_CREATED
        )
