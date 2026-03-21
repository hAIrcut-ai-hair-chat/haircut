from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user