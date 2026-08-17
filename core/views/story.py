from rest_framework.viewsets import ModelViewSet
from core.serializers import StorySerializer
from core.models import Story

class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def perform_create(self, serializer):
        return super(user=self.request.user)

    