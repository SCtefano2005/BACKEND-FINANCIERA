from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Conectar al grupo de notificaciones
        self.group_name = "notificaciones_facturas"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Desconectar del grupo
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def enviar_notificacion(self, event):
        # Enviar notificación al WebSocket
        mensaje = event["mensaje"]
        await self.send(text_data=json.dumps({
            "mensaje": mensaje
        }))
