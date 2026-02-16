from pyexpat import model
from django.db import models
from core.models import User
import uuid
from uploader.models.image import Image



class UserAiQuestion(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.CharField(max_length=255)
    date= models.DateTimeField(auto_now_add=True, editable=False)
    response = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.question
    
class UserImageAiQuestion(models.Model):
    user_ai_question_uuid = models.ForeignKey(UserAiQuestion, on_delete=models.PROTECT, related_name="ai_question")
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    
class AskAi(models.Model):
    attachment_uuid = models.UUIDField(default=uuid.uuid4, auto_created=True)
    ai_response = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    question_uuid = models.ForeignKey(UserImageAiQuestion, on_delete=models.PROTECT)

    def __str__(self):
        return self.ai_response    
    

    