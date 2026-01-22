from rest_framework.viewsets import ModelViewSet
from core.models import UserAiQuestion, UserImageAiQuestion
from core.serializers import UserAiQuestionSerializer, UserImageAiQuestionSerializer
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import os
from django.db import transaction
from rest_framework.serializers import ValidationError 


django_url = os.getenv("BACKEND_URL")

class UserAiQuestionViewSet(ModelViewSet):
    queryset = UserAiQuestion.objects.all()
    serializer_class = UserAiQuestionSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    @action(detail=False, methods=["post"])
    def question_with_image(self, request):
        with transaction.atomic():
            question_serializer = UserAiQuestionSerializer(data=request.data)
            question_serializer.is_valid(raise_exception=True)
            question = question_serializer.save(user=request.user)

            image = request.FILES.get("image")
            if not image:
                raise ValidationError({"image": "Image is required"})

            try:
                uploader_response = requests.post(f"{django_url}/image",files={"file": image})
            except Exception as error:
                raise ValidationError({"uploader": f"Request failed: {error}"})

            if uploader_response.status_code != status.HTTP_201_CREATED:
                raise ValidationError({"uploader": "Error uploading image"})

            uploader_data = uploader_response.json()

            image_serializer = UserImageAiQuestionSerializer(data={"image_url": uploader_data.get("url"),"attachment_key": uploader_data.get("attachment_key")})
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(user_ai_question=question)

            return Response({"message": "Question with image created successfully", "question_uuid": question.uuid},status=status.HTTP_201_CREATED)
        
    
