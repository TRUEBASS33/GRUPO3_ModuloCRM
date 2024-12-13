from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 
from .views import (
    home,
    productos,
    ClienteViewSet,
    ProductoViewSet,
    PedidoViewSet,
    DetallePedidoViewSet,
    TareaViewSet,
    UsuarioViewSet,
    ActividadViewSet,
    HistorialPrecioViewSet,
    PagoViewSet,
    MovimientoInventarioViewSet,
)

# Router para las API
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalle-pedidos', DetallePedidoViewSet)
router.register(r'tareas', TareaViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'actividades', ActividadViewSet)
router.register(r'historial-precios', HistorialPrecioViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'movimientos-inventario', MovimientoInventarioViewSet)

urlpatterns = [
    path('', home, name='home'),  # Vista para la página de inicio
    path('api/', include(router.urls)),  # Rutas de API
    
    # Rutas para vistas tradicionales (clientes, productos, edición)
    path('clientes/', views.obtener_clientes, name='obtener_clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('productos/', productos, name='productos'),  # Ruta basada en templates

    path('productos/', views.productos, name='productos'),  # Página de listado de productos
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),  # Editar producto
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),  # Crear un nuevo cliente
    path('clientes/actualizar/<int:id>/', views.actualizar_cliente, name='actualizar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleados/crear/', views.crear_empleado, name='crear_empleado'),
    path('empleados/editar/<int:empleado_id>/', views.editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/confirmar/', views.confirmar_eliminacion_producto, name='confirmar_eliminacion_producto'),


]
