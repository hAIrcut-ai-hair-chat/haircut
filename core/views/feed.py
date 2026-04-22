from core.models import Feed, Views, Like, Save
from core.serializers import FeedSerializer, ViewSerializer, LikeSerializer, SaveSerializer, ListFeedSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer   
 
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return ListFeedSerializer
        return FeedSerializer   

class ViewViewSet(ModelViewSet):
    queryset = Views.objects.all()
    serializer_class = ViewSerializer  

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class SaveViewSet(ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer

    @action(detail=False, methods=['get'])
    def saved_posts(self, request):
        user = self.kwargs.get('email')
        saved_posts = Save.objects.filter(viewer_email=user)
        if not self.saved_posts.exists():
            return Response({"detail": "No saved posts found for this user."}, status=200)
        serializer = self.get_serializer(saved_posts, many=True)
        return Response(serializer.data)