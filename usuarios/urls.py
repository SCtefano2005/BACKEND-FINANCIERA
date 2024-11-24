from django.urls import path,include
from .views import CrearUsuarioView, UsuarioListView, ActualizarUsuarioView, ClienteViewSet, ProveedorViewSet, FacturaClienteViewSet, FacturaProveedorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'facturas-clientes', FacturaClienteViewSet)
router.register(r'facturas-proveedores', FacturaProveedorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/crear-usuario/', CrearUsuarioView.as_view(), name='crear_usuario'),
    path('api/listar-usuarios/', UsuarioListView.as_view(), name='listar_usuarios'),
    path('api/actualizar-usuario/<int:pk>/', ActualizarUsuarioView.as_view(), name='actualizar_usuario'),
]
