from celery import shared_task
from core.models import UserAiQuestion
from core.services import PotasKwenAi, PotasImageAI



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

@shared_task(autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def celeryAiImage(prompt: str, image, question_uuid: str):
    ai_service = PotasImageAI().image(prompt=prompt, question_uuid=question_uuid)
    
    response_text = ai_service["json"]["response"]
    
    if not response_text:
        raise ValueError("Invalid AI image response")

    return {
        "message": "New image generated with successfully",
        "response": response_text,
        "question_uuid": question_uuid
    
    }