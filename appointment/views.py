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
import calendar
from dateutil.relativedelta import *
from datetime import *
import json

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

    @action(detail=False, methods=['post'])
    def queue_create(self, request):
        print('queue_create', request.data)

        try:
            queue = Queue.objects.get(pk=request.data['queue_id'])
        except Queue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        employee_list = Employee.objects.filter(id__in=request.data['employees'])

        date_start_req = request.data['date_start']
        date_end_req = request.data['date_end']
        day_time_start = request.data['day_time_start']
        day_time_end = request.data['day_time_end']
        time_interval = request.data['time_interval']

        weekday_list = []

        if request.data['checkbox_monday']:
            weekday_list.append(0)
        if request.data['checkbox_tuesday']:
            weekday_list.append(1)
        if request.data['checkbox_wednesday']:
            weekday_list.append(2)
        if request.data['checkbox_thursday']:
            weekday_list.append(3)
        if request.data['checkbox_friday']:
            weekday_list.append(4)
        if request.data['checkbox_saturday']:
            weekday_list.append(5)
        if request.data['checkbox_sunday']:
            weekday_list.append(6)

        date_start = datetime.strptime(date_start_req + ' {}:00:00'.format(day_time_start), '%Y-%m-%d %H:%M:%S')
        date_end = datetime.strptime(date_end_req + ' {}:00:00'.format(day_time_end), '%Y-%m-%d %H:%M:%S')

        day_time_iterator = date_start

        try:
            while day_time_iterator < date_end:
                day_time_iterator_start_time = day_time_iterator.replace(hour=day_time_start, minute=0)
                day_time_iterator_end_time = day_time_iterator.replace(hour=day_time_end, minute=0) - relativedelta(minutes=time_interval)
                if day_time_iterator.weekday() in weekday_list:
                    if day_time_iterator_start_time <= day_time_iterator <= day_time_iterator_end_time:
                        for employee in employee_list:
                            Appointment.objects.create(queue=queue, employee=employee,
                                                       appointment_date_time=day_time_iterator)
                day_time_iterator = day_time_iterator + relativedelta(minutes=int(time_interval))
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        queryset = Appointment.objects.filter(queue=queue)
        serializer = AppointmentSerializer(queryset, many=True)
        return Response(serializer.data)


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


@api_view(['GET', 'POST'])
def get_calendar(request):
    day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    now = datetime.now()
    prev_date = now - relativedelta(months=1)
    next_date = now + relativedelta(months=1)
    calendar_list = []
    cal = calendar.Calendar()
    for day in cal.itermonthdates(now.year, now.month):
        is_other_month = True if day.month != now.month else False
        cal_day = CalendarDay(day, day.weekday(), day_names[day.weekday()], is_other_month)
        calendar_list.append(json.dumps(cal_day.__dict__, default=json_serial, ensure_ascii=False))
    return Response({'calendar': calendar_list, 'prev_date': json_serial(prev_date),
                     'next_date': json_serial(next_date)})


class CalendarDay:
    def __init__(self, day_date, day_number, day_name, is_other_month):
        self.day_date = day_date
        self.day_number = day_number
        self.day_name = day_name
        self.is_other_month = is_other_month

    def __repr__(self):
        return '{} {} {}'.format(str(self.day_date), self.day_number, self.day_name)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

