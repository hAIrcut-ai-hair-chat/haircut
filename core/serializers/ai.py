from rest_framework.serializers import ModelSerializer
from core.models import UserAiQuestion, UserImageAiQuestion

class UserAiQuestionSerializer(ModelSerializer):
    class Meta:
        model = UserAiQuestion
        fields = "__all__"
        

class UserImageAiQuestionSerializer(ModelSerializer):
    class Meta:
        model = UserImageAiQuestion
        fields = "__all__"