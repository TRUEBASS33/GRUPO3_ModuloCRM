from django.contrib import admin
from .models import Cliente, Producto, Pedido, DetallePedido, Actividad, Usuario, Tarea, Pago, MovimientoInventario, HistorialPrecio

# Configura cada modelo con su administración personalizada
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idCliente', 'nombres', 'apellidos', 'correo', 'telefono', 'fechaRegistro')
    search_fields = ('nombres', 'apellidos', 'correo', 'dni')  # Ahora funciona correctamente
    list_filter = ('fechaRegistro',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'fecha_actualizacion')
    search_fields = ('nombre',)
    list_filter = ('fecha_actualizacion',)
    ordering = ('-fecha_actualizacion',)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'idCliente', 'nombre_cliente', 'fecha', 'total']
    ordering = ['-fecha']
    list_filter = ['fecha']

admin.site.register(Pedido, PedidoAdmin)  # Solo una vez

class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad', 'subtotal']  # Usa campos válidos

admin.site.register(DetallePedido, DetallePedidoAdmin)


@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('idCliente', 'tipo_actividad', 'fecha', 'notas')
    list_filter = ('tipo_actividad',)
    search_fields = ('idCliente__nombres', 'idCliente__apellidos')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'is_staff', 'is_active')
    list_filter = ('rol', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'asignado_a', 'fecha_limite', 'estado')
    list_filter = ('estado', 'fecha_limite')
    search_fields = ('descripcion', 'asignado_a__username')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'monto_pago', 'fecha_pago', 'metodo_pago', 'estado_pago')
    list_filter = ('metodo_pago', 'estado_pago')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'tipo_movimiento', 'fecha', 'descripcion')
    list_filter = ('tipo_movimiento',)

@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'precio', 'fecha_inicio', 'fecha_fin')
    search_fields = ('producto__nombre',)
