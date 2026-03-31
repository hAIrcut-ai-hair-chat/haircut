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

    @action(detail=False, methods=["post"])
    def generate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prompt = serializer.validated_data.get("prompt")
        image = celeryAiImage.delay(prompt=prompt).get()
        if image:
            serializer.save(image_url=image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Failed to generate image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
                