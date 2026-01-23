from rest_framework.serializers import ModelSerializer, ImageField, SlugRelatedField
from core.models import UserAiQuestion, UserImageAiQuestion
from uploader.models import Image

class UserAiQuestionSerializer(ModelSerializer):
    image = ImageField(write_only=True, required=True)
    class Meta:
        model = UserAiQuestion
        fields = ["uuid", "question", "image", "user"]
        read_only_fields = ["uuid"]        

class UserImageAiQuestionSerializer(ModelSerializer):
    image = SlugRelatedField(
        slug_field="attachment_key",
        queryset=Image.objects.all()
    )

    class Meta:
        model = UserImageAiQuestion
        fields = ["user_ai_question_uuid", "image"]