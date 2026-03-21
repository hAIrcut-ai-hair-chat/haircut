from django.db import models
from core.models import User
import uuid
from uploader.models import Image

class Feed(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Views(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    viewer = models.ForeignKey(Views, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Save(models.Model):
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Feed, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
