from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ClienteViewSet, ProveedorViewSet, FacturaClienteViewSet,
    FacturaProveedorViewSet, FacturaPDFView, GenerarExcelFacturasView
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'facturas-clientes', FacturaClienteViewSet, basename='factura-cliente')
router.register(r'facturas-proveedores', FacturaProveedorViewSet, basename='factura-proveedor')

urlpatterns = [
    path('', include(router.urls)),  
    path('facturas-clientes/<int:factura_id>/pdf/', FacturaPDFView.as_view(), name='factura_pdf'),
    path('facturas/excel/', GenerarExcelFacturasView.as_view(), name='generar_excel_facturas'),
]
