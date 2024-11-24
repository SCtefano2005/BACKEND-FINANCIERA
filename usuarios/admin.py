from django.contrib import admin
from .models import Usuario, Cliente, Proveedor, FacturaCliente, FacturaProveedor

# Configuración personalizada para el modelo Usuario
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'activo', 'fecha_creacion')
    search_fields = ('username', 'email', 'rol')
    list_filter = ('rol', 'activo')
    ordering = ('fecha_creacion',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Información Personal', {
            'fields': ('nombre_completo', 'rol')
        }),
        ('Permisos', {
            'fields': ('activo',)
        }),
    )

# Configuración personalizada para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'dni', 'telefono')
    search_fields = ('nombre', 'email', 'dni')
    list_filter = ('nombre',)
    ordering = ('nombre',)

# Configuración personalizada para el modelo Proveedor
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'dni', 'ruc', 'telefono')
    search_fields = ('nombre', 'email', 'ruc')
    list_filter = ('nombre',)
    ordering = ('nombre',)

# Configuración personalizada para el modelo FacturaCliente
@admin.register(FacturaCliente)
class FacturaClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'estado')
    search_fields = ('numero_factura', 'cliente__nombre')
    list_filter = ('estado', 'fecha_emision')
    ordering = ('fecha_emision',)

# Configuración personalizada para el modelo FacturaProveedor
@admin.register(FacturaProveedor)
class FacturaProveedorAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'proveedor', 'fecha_emision', 'fecha_vencimiento', 'monto_total', 'estado')
    search_fields = ('numero_factura', 'proveedor__nombre')
    list_filter = ('estado', 'fecha_emision')
    ordering = ('fecha_emision',)

