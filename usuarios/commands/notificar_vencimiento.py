from django.core.management.base import BaseCommand
from usuarios.views import notificar_facturas_vencimiento

class Command(BaseCommand):
    help = "Notifica sobre facturas próximas a vencer"

    def handle(self, *args, **kwargs):
        notificar_facturas_vencimiento()
        self.stdout.write("Notificaciones de vencimiento enviadas con éxito.")
