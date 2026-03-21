from core.models import Feed, Views, Like, Save
from rest_framework import serializers

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ["image", "author", "created_at", "uuid"]
        read_only_fields = ["uuid", "created_at"]
        
class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields = ["feed", "viewer", "created_at"]
        read_only_fields = ["created_at"]
        depht = 1


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["feed", "viewer", "created_at"]
        read_only_fields = ["created_at"]
        depht = 1


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = ["post", "viewer", "created_at"]
        read_only_fields = ["created_at"]
        depht = 1