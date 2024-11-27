from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Cliente, Proveedor, FacturaCliente, FacturaProveedor, Usuario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['rol'] = self.user.rol  # Agrega el rol del usuario al token
        return data

# Serializador para Crear Usuario
class CrearUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'rol']

    def create(self, validated_data):
        # Encriptar la contraseña antes de crear el usuario
        user = Usuario.objects.create(**validated_data)
        return user

# Serializador para Visualizar Usuario (sin contraseña)
class UsuarioReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'rol', 'nombre_completo', 'activo']

# Serializador para Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

    def validate_dni(self, value):
        # Validar que el DNI tenga exactamente 8 caracteres numéricos
        if len(value) != 8 or not value.isdigit():
            raise serializers.ValidationError("El DNI debe tener exactamente 8 dígitos numéricos.")
        return value

# Serializador para Proveedor
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

    def validate_ruc(self, value):
        # Validar que el RUC tenga exactamente 11 caracteres numéricos
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("El RUC debe tener exactamente 11 dígitos numéricos.")
        return value

# Serializador para FacturaCliente
class FacturaClienteSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = FacturaCliente
        fields = '__all__'

    def validate_monto_total(self, value):
        # Validar que el monto total sea positivo
        if value <= 0:
            raise serializers.ValidationError("El monto total debe ser mayor a cero.")
        return value

# Serializador para FacturaProveedor
class FacturaProveedorSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)

    class Meta:
        model = FacturaProveedor
        fields = '__all__'
        
    def validate_monto_total(self, value):
        # Validar que el monto total sea positivo
        if value <= 0:
            raise serializers.ValidationError("El monto total debe ser mayor a cero.")
        return value