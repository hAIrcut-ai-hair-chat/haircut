import base64
import requests

from django.conf import settings
from django.db import transaction
from django.db.transaction import on_commit

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from core.models import UserAiQuestion
from core.serializers import (
    UserAiQuestionSerializer,
    UserImageAiQuestionSerializer,
)
from core.tasks import celeryAiImage, celeryAiChat


class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        serializer = UserAiQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = serializer.validated_data.pop("image", None)
        prompt = serializer.validated_data.get("question")

        question = serializer.save()

        attachment_key = None
        image_base64 = None

        if image:
            image_bytes = image.read()
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            image.seek(0)

            uploader_response = requests.post(
                f"{settings.DJANGO_URL}/image/",
                files={"file": image},
                timeout=10
            )

            attachment_key = uploader_response.json().get("attachment_key")

            image_serializer = UserImageAiQuestionSerializer(data={
                "image": attachment_key,
                "user_ai_question_uuid": question.uuid
            })
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save()

            celeryAiImage.delay(prompt=prompt, image_b64=image_base64)

        celeryAiChat.delay(
            prompt=prompt,
            question_uuid=str(question.uuid)
        )

        return Response(
            {
                "message": "Question created successfully",
                "question_uuid": question.uuid,
                "attachment_key": attachment_key,
            },
            status=status.HTTP_201_CREATED
        )
