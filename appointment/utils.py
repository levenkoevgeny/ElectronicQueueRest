from django.core.mail import send_mail
from django.conf import settings
from jose import jwt
from rest_framework.response import Response
from rest_framework import status


def get_payload_from_request_token(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        return payload
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)


def send_email(email_list, subject="No subject", message=""):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        email_list,
        fail_silently=False,
    )