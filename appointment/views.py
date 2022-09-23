from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from jose import jwt

from .models import Organization, Employee, Appointment, Queue
from .serializers import OrganizationSerializer, EmployeeSerializer, AppointmentSerializer, QueueSerializer
from .consumers import AppointmentsConsumer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class QueueViewSet(viewsets.ModelViewSet):
    def list(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
            payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        except jwt.JWTError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        try:
            organization_data = Organization.objects.get(user_id=payload['user_id'])
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if organization_data.user.is_superuser:
            queryset = Queue.objects.all()
        else:
            queryset = Queue.objects.filter(organization=organization_data)
        serializer = QueueSerializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['queue', 'employee', 'appointment_lastname']
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = Organization.objects.get(user_id=payload['user_id'])
        serializer = OrganizationSerializer(user_data)
        return Response(serializer.data)
    except Organization.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=Appointment)
def appointment_post_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, Appointment):
        if created:
            queue_group_name = 'queue_%s' % instance.queue.id
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(queue_group_name, {"type": "appointment_message",
                                                                       'message': AppointmentSerializer(instance).data})


def send_email(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['amiapythonprojects@gmail.com'],
        fail_silently=False,
    )