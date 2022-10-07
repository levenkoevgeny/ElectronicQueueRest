import django_filters
from .models import Queue, Appointment, Employee


class QueueFilter(django_filters.FilterSet):
    class Meta:
        model = Queue
        fields = {
            'queue_name': ['icontains'],
        }


class AppointmentFilter(django_filters.FilterSet):
    class Meta:
        model = Appointment
        fields = {
            'queue__id': ['exact'],
            'employee__id': ['exact'],
            'is_booked': ['exact'],
        }


class EmployeeClientFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'organization__id': ['exact'],
        }