from django.contrib import admin
from .models import Organization, Employee, Appointment, Queue


admin.site.register(Organization)
admin.site.register(Employee)
admin.site.register(Appointment)
admin.site.register(Queue)

