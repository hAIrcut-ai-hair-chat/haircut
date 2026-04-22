from rest_framework import serializers
from core.models import ImageGeneration
from uploader.models import Image

class ListImageGenerationSerializer(serializers.ModelSerializer):
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

class CreateImageGenerationSerializer(serializers.ModelSerializer):
        image_url= serializers.SerializerMethodField()

        class Meta:
            model = ImageGeneration
            fields = ['uuid', 'author', 'prompt', 'image_url', 'created_at']
            read_only_fields = ['uuid', 'created_at']

        def get_image_url(self, obj):

            file = obj.image_url
            if not file:
                raise ValueError("Image not fought")
            
            uploaded_image = Image.objects.create(
                file=file,
                description=f"Image for prompt: {obj.prompt}"
            )
            return uploaded_image.attachment_key
        
        

        


