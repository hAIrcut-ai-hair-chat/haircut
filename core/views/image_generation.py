from core.models import ImageGeneration
from core.serializers.image_generation import ImageGenerationSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from core.tasks import celeryAiImage
from uploader.models import Image

class ImageGenerationViewSet(ModelViewSet):
    queryset = ImageGeneration.objects.all()
    serializer_class = ImageGenerationSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        prompt = serializer.validated_data.get("prompt")
        image_uuid = celeryAiImage.delay(prompt=prompt).get()
        if image_uuid:
            try:
                image_obj = Image.objects.get(uuid=image_uuid)
                image_generation = ImageGeneration.objects.create(
                    author=request.user,
                    prompt=prompt,
                    image_url=image_obj
                )
                serializer = self.get_serializer(image_generation, context={'request': request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Image.DoesNotExist:
                return Response({"detail": "Image not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"detail": "Failed to generate image."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
                