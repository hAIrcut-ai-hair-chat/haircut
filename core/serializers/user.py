from os import read, write
from pickletools import read_long1

from charset_normalizer.constant import TRACE
from redis.exceptions import TryAgainError
from rest_framework.serializers import ModelSerializer

from core.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        depth = 1
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class AvatarSerializer():
    class Meta:
        model = User
        fields  = ["avatar"]
        