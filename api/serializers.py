# crm/serializers.py
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import (
    Cliente,
    Producto,
    Pedido,
    DetallePedido,
    Tarea,
    Usuario,
    Actividad,
    HistorialPrecio,
    Pago,
    MovimientoInventario,
)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class HistorialPrecioSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Relación con Producto

    class Meta:
        model = HistorialPrecio
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())  # Solo la clave primaria del cliente

    class Meta:
        model = Pedido
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'subtotal']

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    class Meta:
        model = Usuario
        fields = '__all__'

class ActividadSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())  # Relación con Cliente

    class Meta:
        model = Actividad
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    pedido = serializers.PrimaryKeyRelatedField(queryset=Pedido.objects.all())  # Relación con Pedido

    class Meta:
        model = Pago
        fields = '__all__'


class MovimientoInventarioSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Relación con Producto

    class Meta:
        model = MovimientoInventario
        fields = '__all__'
