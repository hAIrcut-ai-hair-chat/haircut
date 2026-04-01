from celery import shared_task
from core.models import UserAiQuestion
from core.services import PotasKwenAi, PotasImageAI
import requests
from core.services import ParaFal
from uploader.models import Image
from django.core.files.base import ContentFile
from urllib.request import urlopen
import mimetypes
import logging
from urllib.error import URLError, HTTPError

logger = logging.getLogger(__name__)

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
def celeryAiImage(prompt: str):
    try:
        logger.info(f"Starting image generation for prompt: {prompt[:50]}...")
        
        fal = ParaFal()
        image_url = fal.generate_image(prompt=prompt)
        
        if not image_url:
            logger.error("Failed to generate image URL")
            raise ValueError("Failed to generate image URL")
        
        logger.info(f"Downloading image from: {image_url}")
        
        try:
            response = urlopen(image_url, timeout=30)
            image_content = ContentFile(response.read())
        except HTTPError as e:
            logger.error(f"HTTP error downloading image: {e.code} - {e.reason}")
            raise Exception(f"Failed to download image: HTTP {e.code}") from e
        except URLError as e:
            logger.error(f"URL error downloading image: {str(e)}")
            raise Exception(f"Failed to download image: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error downloading image: {str(e)}")
            raise
        
        if not image_content or image_content.size == 0:
            logger.error("Downloaded image is empty")
            raise ValueError("Downloaded image is empty")
        
        mime_type, _ = mimetypes.guess_type(image_url)
        extension = mimetypes.guess_extension(mime_type) if mime_type else '.jpg'
        filename = f"generated_{int(__import__('time').time())}{extension}"
        
        logger.info(f"Creating Image object with filename: {filename}")
        
        try:
            image_obj = Image.objects.create(description=f"Generated from prompt: {prompt}")
            image_obj.file.save(filename, image_content, save=True)
            logger.info(f"Image saved successfully with UUID: {image_obj.uuid}")
            return image_obj.uuid
        except Exception as e:
            logger.error(f"Error saving image to database: {str(e)}")
            raise Exception(f"Failed to save image: {str(e)}") from e
    
    except Exception as e:
        logger.error(f"Image generation task failed: {str(e)}")
        raise

@shared_task(autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),retry_backoff=5, retry_kwargs={"max_retries": 3}, soft_time_limit=60)
def celeryAiFeed(image_b64: str):
    image = image_b64.split(",")[1] if "," in image_b64 else image_b64

    if not image:
        raise ValueError("Invalid image data")

    
    
