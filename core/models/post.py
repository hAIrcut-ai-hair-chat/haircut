from django.db import models
from uploader.models import Image
from core.utils import UUIDModel


class Post(UUIDModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="image_post", null=True, blank=True)
    text = models.TextField(max_length=5000, null=True, blank=True)
    author_comment = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.text}" + f"{self.author_comment}"

    