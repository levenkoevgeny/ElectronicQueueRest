from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_email as send_email_def


@shared_task
def send_email(email_list, subject="No subject", message=""):
    send_email_def(email_list, subject, message)
