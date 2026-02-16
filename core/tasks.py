from core.services import PotasKwenAi
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist


potas_kwen_ai = PotasKwenAi()

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def celeryAiChat(prompt: str):
    response = potas_kwen_ai.generate(prompt=prompt)
    
    return response
