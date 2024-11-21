from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('CONTADOR', 'Contador'),
        ('GERENTE', 'Gerente'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='CONTADOR')
    groups = models.ManyToManyField(Group, related_name='usuario_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='usuario_permissions', blank=True)

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=8,unique=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# Modelo de Factura Base
class FacturaBase(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PAGADA', 'Pagada'),
        ('VENCIDA', 'Vencida'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='PENDIENTE')

    class Meta:
        abstract = True

# Modelo de Factura de Cliente (Cuentas por Cobrar)
class FacturaCliente(FacturaBase):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')

    def __str__(self):
        return f"Factura {self.numero_factura} - Cliente: {self.cliente.nombre}"

# Modelo de Factura de Proveedor (Cuentas por Pagar)
class FacturaProveedor(FacturaBase):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='facturas')

    def __str__(self):
        return f"Factura {self.numero_factura} - Proveedor: {self.proveedor.nombre}"
