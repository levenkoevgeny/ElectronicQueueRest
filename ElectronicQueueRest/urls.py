from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from rest_framework import routers

from appointment import views

router = routers.DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'queues', views.QueueViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
