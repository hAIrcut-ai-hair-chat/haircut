from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SlugRelatedField, SerializerMethodField
from core.models import Post
from uploader.models import Image


class PostSerializer(ModelSerializer):
    image = SlugRelatedField(
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        allow_null=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ['text', 'image', 'user']  
        read_only_fields = ["user"]

class ListPostSerializer(ModelSerializer):
    image = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['text', 'image', 'user']
        depth = 1

    def get_image(self, obj):
        if obj.image and obj.image.file:
            return obj.image.file.url
        return None


