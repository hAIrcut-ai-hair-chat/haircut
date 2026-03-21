from argparse import Action

from core.models import Feed
from core.serializers import FeedSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class FeedViewSet(ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer    

    