from django.db import models
from core.utils import UUIDModel    

class Think(UUIDModel):
    emoji = models.CharField(max_length=255, null=True, blank=True)
    thought = models.CharField(max_length=255, null=True, blank=True)
