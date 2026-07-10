from rest_framework.viewsets import ModelViewSet
from core.serializers import ThinkSerializer
from core.models import Think
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action



class ThinkViewSet(ModelViewSet):
    queryset = Think.objects.all()
    serializer_class = ThinkSerializer
    #permission_classes = [IsAuthenticated]