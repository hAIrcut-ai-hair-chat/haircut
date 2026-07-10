from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status


class MockAiViewSet(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')

        prompt = request.data.get('prompt')
        room_uuid = request.data.get('room_uuid')
        style = request.data.get('style')

        if image is None:
            return Response(
                {'error': 'Nenhuma imagem enviada.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'prompt': prompt,
                'room_uuid': room_uuid,
                'style': style,
                'image': {
                    'filename': image.name,
                    'content_type': image.content_type,
                    'size': image.size,
                }
            },
            status=status.HTTP_200_OK
        )
