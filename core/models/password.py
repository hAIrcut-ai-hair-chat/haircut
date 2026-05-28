from django.db import models
from core.models import User

class ForgetPassword(models.Model):
    email = models.ForeignKey(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.code