from os import read
from pickletools import read_long1

from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password", "passage_id", "name"]
        read_only_fields = ["passage_id"]
        depth = 1

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user