import uuid

from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    organization_name = models.TextField(verbose_name="Organization name")

    def __str__(self):
        return self.organization_name

    class Meta:
        ordering = ('organization_name',)
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class Employee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Organization")
    last_name = models.CharField(verbose_name="Last name", max_length=100)

    def __str__(self):
        return self.last_name

    class Meta:
        ordering = ('last_name',)
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class Queue(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Organization")
    queue_name = models.CharField(verbose_name="Queue name", max_length=255)
    date_time_added = models.DateTimeField(auto_now_add=True, verbose_name="Date time added")
    is_active = models.BooleanField(verbose_name="Is active", default=False)
    random_uuid = models.UUIDField(verbose_name="UUID", default=uuid.uuid4, editable=True)

    def __str__(self):
        return self.queue_name

    class Meta:
        ordering = ('queue_name',)
        verbose_name = 'Queue'
        verbose_name_plural = 'Queues'


class Appointment(models.Model):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, verbose_name="Queue")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    appointment_date_time = models.DateTimeField(verbose_name="Appointment date-time")
    appointment_lastname = models.CharField(verbose_name="Appointment lastname", max_length=100, blank=True, null=True)
    appointment_firstname = models.CharField(verbose_name="Appointment firstname", max_length=100, blank=True, null=True)
    appointment_patronymic = models.CharField(verbose_name="Appointment patronymic", max_length=100, blank=True, null=True)
    appointment_email = models.EmailField(verbose_name="Appointment email", max_length=100, blank=True, null=True)
    appointment_phone = models.CharField(verbose_name="Appointment phone", max_length=20, blank=True, null=True)
    date_time_added = models.DateTimeField(auto_now_add=True, verbose_name="Date time added")
    is_booked = models.BooleanField(verbose_name="Booked", default=False)
    appointment_comment = models.TextField(verbose_name="Comment", blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(self.appointment_date_time.date(), self.appointment_date_time.time(), self.employee.last_name)

    class Meta:
        ordering = ('appointment_date_time',)
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'