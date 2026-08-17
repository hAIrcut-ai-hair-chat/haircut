from rest_framework import serializers
from core.models import Story
from uploader.models import Image

class StorySerializer(serializers.ModelSerializer):
    image = serializers.SlugRelatedField(
        queryset=Image.objects.all(),
        slug_field="attachment_key",
        allow_null=True,
        required=False
    )

    class Meta:
        model = Story
        fields = ['user', 'image', 'description']
        read_only_fields = ['user']

    def get_image(self, obj):
        if obj.image and obj.image.file:
            return obj.image.file.url
        return None