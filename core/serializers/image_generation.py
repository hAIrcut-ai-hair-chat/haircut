from rest_framework import serializers
from core.models import ImageGeneration

class ImageGenerationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageGeneration
        fields = ['uuid', 'author', 'prompt', 'image_url', 'created_at', 'feedback']
        read_only_fields = ['uuid', 'created_at'] 
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image_url and request:
            return request.build_absolute_uri(obj.image_url.url)
        elif obj.image_url:
            return obj.image_url.url
        return None
