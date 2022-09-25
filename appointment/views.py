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
from django.contrib.auth.models import User
from django.conf import settings

from jose import jwt

from .models import Organization, Employee, Appointment, Queue
from .serializers import OrganizationSerializer, EmployeeSerializer, AppointmentSerializer, QueueSerializer, \
    UserSerializer, UserNamesSerializer
from .consumers import AppointmentsConsumer
from .tasks import send_email
from .utils import get_payload_from_request_token


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        payload = get_payload_from_request_token(request)
        try:
            organization_data = Organization.objects.get(user_id=payload['user_id'])
        except Organization.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        queryset = Employee.objects.filter(organization=organization_data)
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class QueueViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        payload = get_payload_from_request_token(request)
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

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [permissions.IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        updated_appointment = serializer.save()
        if updated_appointment.is_booked:
            if updated_appointment.appointment_email:
                send_email.delay([updated_appointment.appointment_email], "Запись на ЦТ", "Вы записаны")

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['queue', 'employee', 'appointment_lastname']
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserNamesViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserNamesSerializer
    filterset_fields = {
        'username': ['exact'],
    }


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


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if isinstance(instance, User):
        if created:
            Organization.objects.create(user=instance, organization_name="Без названия")