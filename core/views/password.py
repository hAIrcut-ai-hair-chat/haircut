import stat

from rest_framework.views import APIView
from core.models import User
from rest_framework.response import Response
from rest_framework import status
from core.utils import generate_code
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from core.tasks import send_email

class ForgetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(data={"message": "User not fought"},status=status.HTTP_400_BAD_REQUEST)
        
        new_email = send_email(email)
         

        return Response(data="message", status=status.HTTP_200_OK)
    
    def get(self, request):
        return Response(data={"message": "Hello world"}, status=status.HTTP_200_OK)