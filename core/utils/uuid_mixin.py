from django.db import models
import uuid
from core.models import User

class UUIDModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)ss")

    class Meta: 
        abstract = True