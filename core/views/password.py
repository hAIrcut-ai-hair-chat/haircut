from rest_framework.views import APIView
from core.models import User
from rest_framework.response import Response
from rest_framework import status
from core.utils import generate_code
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class ForgetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(data={"message": "User not fought"},status=status.HTTP_400_BAD_REQUEST)
        
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

        return Response(data="message", status=status.HTTP_200_OK)