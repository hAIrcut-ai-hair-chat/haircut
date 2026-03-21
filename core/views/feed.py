from core.models import Feed, Views, Like, Save
from core.serializers import FeedSerializer, ViewSerializer, LikeSerializer, SaveSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer    

class ViewViewSet(ModelViewSet):
    queryset = Views.objects.all()
    serializer_class = ViewSerializer  

class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class SaveViewSet(ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer