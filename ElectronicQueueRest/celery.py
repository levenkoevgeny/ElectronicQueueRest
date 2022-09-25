import os

from celery import Celery
from django.core.mail import send_mail
from django.conf import settings
from celery.schedules import crontab
from appointment.tasks import send_email

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ElectronicQueueRest.settings')

app = Celery('ElectronicQueueRest')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, send_email.s(), name='add every 10')


@app.task
def test(arg):
    print(arg)

# @app.task
# def add(x, y):
#     print(x + y)

# @app.task
# def send_email():
#     send_mail(
#         'Subject here',
#         'Here is the message.',
#         settings.EMAIL_HOST_USER,
#         ['amiapythonprojects@gmail.com'],
#         fail_silently=False,
#     )