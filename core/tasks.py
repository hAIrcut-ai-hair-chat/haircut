from celery import shared_task
from core.models import UserAiQuestion
from core.services import PotasKwenAi, PotasImageAI
import requests


@shared_task(autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def celeryAiChat(prompt: str, question_uuid: str):
    
    ai_service = PotasKwenAi().generate(prompt=prompt)
    
    response_text = ai_service["json"]["response"]
    
    if not response_text: 
        raise ValueError("Invalid AI chat response")
    
    ai_question = UserAiQuestion.objects.get(uuid=question_uuid)
    ai_question.response = response_text
    
    ai_question.save(update_fields=["response"])
    
    return {"uuid": str(question_uuid), "ai_response": response_text}

@shared_task(autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),retry_backoff=5, retry_kwargs={"max_retries": 3}, soft_time_limit=60)
def celeryAiImage(prompt: str, image_b64: str):
    return PotasImageAI().image(prompt=prompt, image_b64=image_b64)