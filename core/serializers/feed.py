from core.models import Feed, Views, Like, Save
from uploader.models import Image
from rest_framework import serializers

class FeedSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    image_attachment_key = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Feed
        fields = ["image", "image_attachment_key", "author", "created_at", "uuid"]
        read_only_fields = ["uuid", "created_at"]

    def get_image(self, obj):
        if obj.image:
            return obj.image.file.url
        return None

    def create(self, validated_data):
        image_key = validated_data.pop('image_attachment_key', None)
        feed = Feed.objects.create(**validated_data)
        if image_key:
            try:
                image = Image.objects.get(attachment_key=image_key)
                feed.image = image
                feed.save()
            except Image.DoesNotExist:
                pass
        return feed
    
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