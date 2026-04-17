from core.models import ImageGeneration
from core.serializers.image_generation import ListImageGenerationSerializer, CreateImageGenerationSerializer
from rest_framework.viewsets import ModelViewSet

class ImageGenerationViewSet(ModelViewSet):
    queryset = ImageGeneration.objects.all()
    serializer_class = ListImageGenerationSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateImageGenerationSerializer
        return ListImageGenerationSerializer


