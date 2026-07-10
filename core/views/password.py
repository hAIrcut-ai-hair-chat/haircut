import stat
from xxlimited import new

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from twisted.logger import LoggingFile
from twisted.logger import LoggingFile
from core.models import User, ForgetPassword
from core.tasks import send_email
import logging
import logging

class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response(
                data={"message": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                data={"message": "User not found with this email"},
                status=status.HTTP_404_NOT_FOUND
            )

        new_email = send_email(email)
        print(new_email.get('code'))
            

        if new_email.get('status'):

            ForgetPassword.objects.create(
                email=user,
                code=new_email.get('code')
            )

            return Response(
                data={"message": "Email sent successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            data={"message": "Email not sending"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def get(self, request):
        return Response(
            data={"message": "Hello world"},
            status=status.HTTP_200_OK
        )


class UpdatePasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('password')
        print(email, code, new_password)

        required_fields = {
            "email": email,
            "code": code,
            "password": new_password
        }

        for key, value in required_fields.items():
            if not value:
                return Response({"message": f"{key} is required to redefine password"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            return Response(
                data={"message": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            forget_password = ForgetPassword.objects.get(
                email=user,
                code=code
            )

        except ForgetPassword.DoesNotExist:
            return Response(
                data={"message": "Invalid code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        forget_password.delete()

        return Response(
            data={"message": "Password updated successfully"},
            status=status.HTTP_200_OK
        )