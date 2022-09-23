import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class AppointmentsConsumer(WebsocketConsumer):
    def connect(self):
        self.queue = self.scope['url_route']['kwargs']['queue']
        self.queue_group_name = 'queue_%s' % self.queue

        async_to_sync(self.channel_layer.group_add)(
            self.queue_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.queue_group_name,
            self.channel_name
        )

    def receive(self, appointment_data):
        pass
        # text_data_json = json.loads(appointment_data)
        # message = text_data_json['message']
        #
        # async_to_sync(self.channel_layer.group_send)(
        #     self.queue_group_name,
        #     {
        #         'type': 'appointment_message',
        #         'message': message
        #     }
        # )

    def appointment_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))