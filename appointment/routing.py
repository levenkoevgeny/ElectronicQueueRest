from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/appointments/(?P<queue>\w+)/$', consumers.AppointmentsConsumer.as_asgi()),
]