from rest_framework.serializers import ModelSerializer, ImageField
from core.models import UserAiQuestion, UserImageAiQuestion

class UserAiQuestionSerializer(ModelSerializer):
    image = ImageField(write_only=True, required=True)
    class Meta:
        model = UserAiQuestion
        fields = ["uuid", "question", "image", "user"]
        read_only_fields = ["uuid"]        

class UserImageAiQuestionSerializer(ModelSerializer):
    class Meta:
        model = UserImageAiQuestion
        fields = "__all__"