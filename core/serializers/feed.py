from core.models import Feed, Views, Like, Save
from rest_framework import serializers

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["image", "author", "created_at", "uuid"]
        read_only_fields = ["uuid", "created_at"]
