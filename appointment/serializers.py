from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Organization, Employee, Appointment, Queue


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 1


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('id', 'organization', 'queue_name', 'date_time_added', 'is_active', 'appointment_count',
                  'get_free_appointment_count', 'get_booked_appointment_count')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)