# usuarios/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Añadir al grupo de notificaciones
        self.room_group_name = 'notificaciones'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo de notificaciones
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje desde WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensaje = text_data_json['mensaje']

        # Enviar mensaje al grupo de notificaciones
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'enviar_notificacion',
                'mensaje': mensaje
            }
        )

    # Recibir mensaje del grupo
    async def enviar_notificacion(self, event):
        mensaje = event['mensaje']

        # Enviar mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'mensaje': mensaje
        }))
