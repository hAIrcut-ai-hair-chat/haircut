from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
import requests
import os

from core.models import UserAiQuestion, UserImageAiQuestion
from core.serializers import UserAiQuestionSerializer
from uploader.models.image import Image

django_url = os.getenv("BACKEND_URL")


class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        question_serializer = UserAiQuestionSerializer(data=request.data)
        question_serializer.is_valid(raise_exception=True)

        image_file = question_serializer.validated_data.pop("image")
        question = question_serializer.save()

        try:
            uploader_response = requests.post(
                f"{django_url}/image/",
                files={"file": image_file},
                timeout=10
            )
            uploader_response.raise_for_status()
        except Exception as error:
            question.delete()
            raise ValidationError({"uploader": f"Upload failed: {error}"})

        uploader_data = uploader_response.json()

        try:
            image_instance = Image.objects.get(pk=uploader_data["id"])
        except Image.DoesNotExist:
            question.delete()
            raise ValidationError({"image": "Uploaded image not found in DB"})

        UserImageAiQuestion.objects.create(
            user_ai_question_uuid=question,
            image=image_instance
        )

        return Response(
            {
                "message": "Question with image created successfully",
                "question_uuid": question.uuid
            },
            status=status.HTTP_201_CREATED
        )
