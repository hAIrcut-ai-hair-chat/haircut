from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MockAiViewSet(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        room_uuid = request.data.get('prompt')
        image = request.FILES.get('image')

        if not prompt or not room_uuid or not image:
            return Response({"message": "prompt, room uuid and image is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            

        })
