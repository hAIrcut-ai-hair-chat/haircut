from turtle import mode

from charset_normalizer.constant import TRACE
from django.db import models
from uvicorn.logging import TRACE_LOG_LEVEL
from core.utils.uuid_mixin import UUIDModel
from uploader.models import Image

class Story(UUIDModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="image")
    description = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.description 
