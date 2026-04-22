from rest_framework.serializers import ModelSerializer, ImageField, SlugRelatedField
from core.models import UserAiQuestion, UserImageAiQuestion, AskAi
from uploader.models import Image

class UserImageAiQuestionSerializer(ModelSerializer):
    image = SlugRelatedField(
        slug_field="attachment_key",
        queryset=Image.objects.all()
    )
    class Meta:
        model = UserImageAiQuestion
        fields = ["user_ai_question_uuid", "image", "room"]

class UserAiQuestionSerializer(ModelSerializer):
    image = ImageField(write_only=True, required=True)
    images = UserImageAiQuestionSerializer(many=True, read_only=True)
    class Meta:
        model = UserAiQuestion
        fields = ["uuid", "question", "image", "user", "response", "images", "room"]
        read_only_fields = ["uuid"]   
        
    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        question = UserAiQuestion.objects.create(**validated_data)
        for img in images_data:
            UserImageAiQuestion.objects.create(
                **img
            )
        return question
         
class AskAiSerializer(ModelSerializer):
    class Meta:
        model = AskAi
        fields = ["attachment_uuid", "ai_response", "created_at", "question_uuid"]
        read_only_fields = ["attachment_uuid", "created_at"]