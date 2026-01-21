from django.db import models
from core.models import User
import uuid
from uploader.models.image import Image



class UserAiQuestion(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.CharField(max_length=255)
    date= models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.question
    
class UserImageAiQuestion(models.Model):
    user_ai_question_uuid = models.ForeignKey(UserAiQuestion, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    
    
    

    