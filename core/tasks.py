import code

from celery import shared_task
from core.models import UserAiQuestion
import requests
from uploader.models import Image
from django.core.files.base import ContentFile
from urllib.request import urlopen
import mimetypes
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from core.utils import generate_code
from urllib.error import URLError, HTTPError


@shared_task(autoretry_for=(requests.exceptions.Timeout, requests.exceptions.ConnectionError),retry_backoff=5, retry_kwargs={"max_retries": 3}, soft_time_limit=60)
def send_email(email):
    context = {
            "code": str(generate_code()) 
        }

    html_content = render_to_string(
            "welcome.html",
            context
        )
        
    send_email = EmailMultiAlternatives(
            subject="Confirmação de senha",
            body="",
            from_email="martinsbarroskaua85@gmail.com",
            to=[email]
        )
    
    send_email.attach_alternative(
        html_content,
        "text/html"
        )

    send_email.send()  

    return {
        "code": context.get("code"),
        'status': True
    }
