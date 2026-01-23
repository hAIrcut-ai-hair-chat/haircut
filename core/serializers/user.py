from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        depth = 1
