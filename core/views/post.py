from django_filters.filters import QuerySetRequestMixin

from core.serializers import PostSerializer, ListPostSerializer
from core.models import Post
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ListPostSerializer
        return PostSerializer