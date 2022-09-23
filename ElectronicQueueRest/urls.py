from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from appointment import views

router = routers.DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'employees', views.EmployeeViewSet)
router.register(r'appointments', views.AppointmentViewSet)
router.register(r'queues', views.QueueViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/users/me/', views.get_me),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
