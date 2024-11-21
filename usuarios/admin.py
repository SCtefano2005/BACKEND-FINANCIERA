from django.contrib import admin
from .models import Usuario, Cliente, Proveedor, FacturaCliente, FacturaProveedor

admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(FacturaCliente)
admin.site.register(FacturaProveedor)
