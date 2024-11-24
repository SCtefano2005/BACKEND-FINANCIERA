from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Cliente, Proveedor, FacturaCliente, FacturaProveedor
from .serializers import (
    ClienteSerializer, ProveedorSerializer, FacturaClienteSerializer, FacturaProveedorSerializer, CrearUsuarioSerializer, UsuarioReadSerializer
)
from .permissions import IsAdminOrContadorOrGerente
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

Usuario = get_user_model()

# Vistas para Clientes, Proveedores y Facturas con permisos personalizados
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrContadorOrGerente]  # Aplicar el permiso personalizado

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminOrContadorOrGerente]  # Aplicar el permiso personalizado

class FacturaClienteViewSet(viewsets.ModelViewSet):
    queryset = FacturaCliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAdminOrContadorOrGerente]  # Aplicar el permiso personalizado

class FacturaProveedorViewSet(viewsets.ModelViewSet):
    queryset = FacturaProveedor.objects.all()
    serializer_class = FacturaProveedorSerializer
    permission_classes = [IsAdminOrContadorOrGerente]  # Aplicar el permiso personalizado

# Vista para Crear Usuarios (Solo administradores pueden crear usuarios)
class CrearUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Solo el usuario con rol ADMIN puede crear usuarios
        if request.user.rol != 'ADMIN':
            return Response({'error': 'No tiene permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CrearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(UsuarioReadSerializer(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para Listar Usuarios (Solo administradores pueden ver la lista de usuarios)
class UsuarioListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Solo el usuario con rol ADMIN puede listar usuarios
        if request.user.rol != 'ADMIN':
            return Response({'error': 'No tiene permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

        usuarios = Usuario.objects.all()
        serializer = UsuarioReadSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para Actualizar Usuario (Solo administradores pueden actualizar usuarios)
class ActualizarUsuarioView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk):
        # Solo el usuario con rol ADMIN puede actualizar usuarios
        if request.user.rol != 'ADMIN':
            return Response({'error': 'No tiene permisos para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = CrearUsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(UsuarioReadSerializer(user).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def notificar_vencimiento_factura(request, factura_id):
    factura = get_object_or_404(FacturaCliente, id=factura_id)
    mensaje = f"La factura {factura.numero_factura} está próxima a vencer"

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notificaciones',
        {
            'type': 'enviar_notificacion',
            'mensaje': mensaje
        }
    )

    return JsonResponse({'status': 'notificado'})
