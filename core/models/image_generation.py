from django.db import models
from core.models import User
from uploader.models import Image
import uuid

class ImageGeneration(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.TextField()
    image_url = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Feedback(models.TextChoices):
        LIKE = 'like', 'Like'
        DISLIKE = 'dislike', 'Dislike'
        NEUTRAL = 'neutral', 'Neutral'
    feedback = models.CharField(max_length=10, choices=Feedback.choices, default=Feedback.NEUTRAL, null=True, blank=True)
    
    def __str__(self):
        return self.prompt 