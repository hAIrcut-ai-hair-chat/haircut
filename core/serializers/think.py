from rest_framework.serializers import ModelSerializer
from core.models import Think

class ThinkSerializer(ModelSerializer):
    class Meta:
        model = Think
        fields = ["emoji", "thought", "user"]