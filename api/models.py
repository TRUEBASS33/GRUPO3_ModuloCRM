from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)  # Identificador principal
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=255, default="Sin Apellido")
    dni = models.CharField(max_length=8, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    fechaRegistro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField(blank=True, null=True)  # Descripción
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    stock = models.PositiveIntegerField(default=0)  # Cantidad en inventario
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Última actualización

class HistorialPrecio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto asociado
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    fecha_inicio = models.DateTimeField(auto_now_add=True)  # Inicio del periodo de precio
    fecha_fin = models.DateTimeField(blank=True, null=True)  # Fin del periodo de precio
    
class Pedido(models.Model):
    idCliente = models.IntegerField()  # ID del cliente (vinculado a la API externa)
    nombre_cliente = models.CharField(max_length=255, blank=True)  # Nombre del cliente (opcional)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.nombre_cliente}"


class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto.nombre} (x{self.cantidad})"

        
class Actividad(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Cliente asociado
    tipo_actividad = models.CharField(max_length=50, choices=[
        ('llamada', 'Llamada'),
        ('correo', 'Correo'),
        ('reunion', 'Reunión')
    ])  # Tipo de actividad
    fecha = models.DateTimeField()  # Fecha de la actividad
    notas = models.TextField(blank=True, null=True)  # Notas adicionales
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=15, blank=True, null=True)
    rol = models.CharField(max_length=50, choices=[
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor')
    ], default='vendedor')

class Tarea(models.Model):
    asignado_a = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Usuario asignado
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)  # Cliente relacionado
    descripcion = models.TextField()  # Descripción de la tarea
    fecha_limite = models.DateTimeField()  # Fecha límite
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completada', 'Completada')], default='pendiente')  # Estado de la tarea
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)  # Pedido asociado
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del pago
    fecha_pago = models.DateTimeField(auto_now_add=True)  # Fecha del pago
    metodo_pago = models.CharField(max_length=50, choices=[
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia Bancaria'),
        ('efectivo', 'Efectivo'),
        ('otros', 'Otros')
    ])  # Método de pago
    estado_pago = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente')  # Estado del pago

class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Producto asociado
    cantidad = models.IntegerField()  # Cantidad (positiva para entradas, negativa para salidas)
    tipo_movimiento = models.CharField(max_length=20, choices=[('entrada', 'Entrada'), ('salida', 'Salida')])  # Tipo de movimiento
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha del movimiento
    descripcion = models.TextField(blank=True, null=True)  # Descripción del movimiento
class Department(models.Model):
    pkInt = models.IntegerField(primary_key=True)
    departmentName = models.CharField(max_length=255)
    description = models.TextField()

class JobPosition(models.Model):
    pkInt = models.IntegerField(primary_key=True)
    jobPositionName = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

class SalaryHistory(models.Model):
    pkInt = models.IntegerField(primary_key=True)
    changeDate = models.DateField()
    previousSalary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currentSalary = models.DecimalField(max_digits=10, decimal_places=2)
    changeReason = models.TextField()

class Employee(models.Model):
    pkInt = models.IntegerField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=20)
    hireDate = models.DateField()
    dni = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    jobPosition = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    salaryHistory = models.OneToOneField(SalaryHistory, on_delete=models.CASCADE)

