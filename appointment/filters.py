import django_filters
from .models import Queue, Appointment


class QueueFilter(django_filters.FilterSet):
    class Meta:
        model = Queue
        fields = {
            'random_uuid': ['exact'],
        }


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = {
            'queue__id': ['exact'],
            'employee__id': ['exact'],
            'is_booked': ['exact'],
        }