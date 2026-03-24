from core.models import ImageGeneration
from core.serializers.image_generation import ImageGenerationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.tasks import celeryAiImage

class ImageGenerationViewSet(ModelViewSet):
    queryset = ImageGeneration.objects.all()
    serializer_class = ImageGenerationSerializer

    @action(detail=True, methods=['post'])
    def image_generate(self, request, pk=None):
        instance = self.get_object()
        prompt = instance.prompt

        celeryAiImage.delay(prompt=prompt, image_generation_uuid=str(instance.uuid))

        return Response({"detail": "Image generation started."}, status=status.HTTP_202_ACCEPTED)