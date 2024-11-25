from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('CONTADOR', 'Contador'),
        ('GERENTE', 'Gerente'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=10, choices=ROLES, default='CONTADOR')
    nombre_completo = models.CharField(max_length=255, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    # Agregar related_name para evitar conflictos
    groups = models.ManyToManyField(
        Group,
        related_name="usuario_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuario_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"

    
class AuditLog(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    accion = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - {self.accion} - {self.fecha_hora}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=8, unique=True, default='00000000')
    ruc = models.CharField(max_length=11, unique=True, default='00000000000') 
    telefono = models.CharField(max_length=9, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    dni = models.CharField(max_length=8, unique=True, default='00000000')
    ruc = models.CharField(max_length=11, unique=True, default='00000000000')
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

