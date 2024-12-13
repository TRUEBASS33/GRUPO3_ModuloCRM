import requests
import json
import pytz
from .models import Employee
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Cliente, Producto, Pedido, DetallePedido, Tarea, Usuario, Actividad, HistorialPrecio, Pago, MovimientoInventario
from .serializers import (
    ClienteSerializer,
    ProductoSerializer,
    PedidoSerializer,
    DetallePedidoSerializer,
    TareaSerializer,
    UsuarioSerializer,
    ActividadSerializer,
    HistorialPrecioSerializer,
    PagoSerializer,
    MovimientoInventarioSerializer,
)
from .forms import ClienteForm, ProductoForm  # Correcto
from rest_framework.decorators import action
from rest_framework.response import Response
import requests

# URL base para la API de la aplicación en producción
BASE_URL = 'https://contactomodulo-production.up.railway.app/api/clientes'
EMPLOYEES_API_URL = "https://rrhhapi-production.up.railway.app/api/rrhh_module/employees/all"

# Vista para renderizar la página principal
def home(request):
    return render(request, 'base.html')  # Cambia 'base.html' por la plantilla correspondiente


def listar_empleados(request):
    try:
        response = requests.get(EMPLOYEES_API_URL)
        if response.status_code == 200:
            empleados = response.json()
            return render(request, 'empleados_list.html', {'empleados': empleados})
        else:
            return render(request, 'empleados_list.html', {'empleados': []})
    except requests.exceptions.RequestException as e:
        return render(request, 'empleados_list.html', {'error': f"Error al conectar con la API: {e}"})
        
def clientes(request):
    clientes = Cliente.objects.all()  # Obtiene todos los clientes
    return render(request, 'clientes.html', {'clientes': clientes})  # Renderiza el template
def productos(request):
    productos = Producto.objects.all()  # Obtén todos los productos
    return render(request, 'productos.html', {'productos': productos})
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos')  # Redirige a la lista de productos después de crear
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)  # Busca el producto por ID
    producto.delete()  # Elimina el producto
    return redirect('productos')  # Redirige a la lista de productos
def confirmar_eliminacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'confirmar_eliminacion_producto.html', {'producto': producto})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)  # Obtiene el cliente por ID
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)  # Rellena el formulario con los datos del cliente
        if form.is_valid():
            form.save()  # Guarda los cambios en la base de datos
            return redirect('clientes')  # Redirige a la página de clientes después de la edición
    else:
        form = ClienteForm(instance=cliente)  # Si es un GET, carga el formulario con los datos actuales del cliente

    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente}) 

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)  # Obtiene el producto por ID
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)  # Rellena el formulario con los datos del producto
        if form.is_valid():
            form.save()  # Guarda los cambios en la base de datos
            return redirect('productos')  # Redirige a la página de productos después de la edición
    else:
        form = ProductoForm(instance=producto)  # Si es un GET, carga el formulario con los datos actuales del producto

    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})  # Renderiza el formulario en el template
# Obtener todos los clientes (GET)
def obtener_clientes(request):
    try:
        # Realizamos la solicitud GET a la API
        response = requests.get(BASE_URL)
        
        if response.status_code == 200:
            clientes = response.json()
            
            # Zona horaria de Perú (UTC-5)
            peru_tz = pytz.timezone('America/Lima')
            
            # Formateamos la fecha de cada cliente
            for cliente in clientes:
                if 'fechaRegistro' in cliente and isinstance(cliente['fechaRegistro'], str):  # Aseguramos que la fecha sea una cadena
                    try:
                        # Convertimos la fecha del formato ISO a datetime
                        fecha_obj = datetime.fromisoformat(cliente['fechaRegistro'])
                        
                        # Convertimos la fecha a la zona horaria de Perú
                        fecha_obj = fecha_obj.replace(tzinfo=pytz.utc).astimezone(peru_tz)
                        
                        # Formateamos la fecha en el formato deseado
                        cliente['fechaRegistro'] = fecha_obj.strftime("%d/%m/%Y")
                    except ValueError:
                        # Si no se puede convertir la fecha, dejamos la original (puedes poner un valor predeterminado)
                        cliente['fechaRegistro'] = cliente['fechaRegistro']  # O puedes poner algo como "Fecha inválida"
                else:
                    cliente['fechaRegistro'] = "Fecha inválida"  # En caso de que no sea una cadena o esté vacío
            
            # Pasamos los datos al template
            return render(request, 'clientes_list.html', {'clientes': clientes})
        else:
            print(f"Error al obtener los datos de la API: {response.status_code}")
            return render(request, 'clientes_list.html', {'clientes': []})
    
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return render(request, 'clientes_list.html', {'clientes': []})

# Crear un nuevo cliente (POST)
def crear_cliente(request):
    if request.method == 'POST':
        try:
            # Recoger los datos del formulario
            cliente_data = {
                'nombres': request.POST['nombre'],
                'apellidos': request.POST['apellido'],
                'dni': request.POST['dni'],
                'correo': request.POST['correo'],
                'telefono': request.POST['telefono'],
                # No incluir 'fechaRegistro' ya que se genera automáticamente
            }
            
            # Realizar la solicitud POST a la API
            headers = {'Content-Type': 'application/json'}
            response = requests.post(BASE_URL, data=json.dumps(cliente_data), headers=headers)

            if response.status_code == 200:
                return redirect('obtener_clientes')
            else:
                error_data = response.json()
                return JsonResponse({'error': f"Error al crear el cliente: {error_data}"}, status=response.status_code)
        except KeyError as e:
            return JsonResponse({'error': f"Campo faltante: {e}"}, status=400)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f"Error al conectar con la API: {e}"}, status=500)
    else:
        return render(request, 'crear_cliente.html')


# Actualizar un cliente (PUT)
def actualizar_cliente(request, id):
    try:
        cliente = requests.get(f'{BASE_URL}/{id}').json()  # GET para obtener los datos del cliente
        if request.method == 'POST':
            data = {
                'nombres': request.POST['nombre'],
                'apellidos': request.POST['apellido'],
                'dni': request.POST['dni'],
                'correo': request.POST['correo'],
                'telefono': request.POST['telefono'],
            }
            response = requests.put(f'{BASE_URL}/{id}', json=data)  # PUT a la API
            if response.status_code == 200:
                return redirect('obtener_clientes')
            else:
                error_data = response.json()
                return JsonResponse({'error': f"No se pudo actualizar el cliente: {error_data}"}, status=response.status_code)
        return render(request, 'actualizar_cliente.html', {'cliente': cliente})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"Error al conectar con la API: {e}"}, status=500)

# Eliminar un cliente (DELETE)
def eliminar_cliente(request, id):
    try:
        response = requests.delete(f'{BASE_URL}/{id}')  # DELETE a la API
        if response.status_code == 200:
            return redirect('obtener_clientes')
        else:
            error_data = response.json()
            return JsonResponse({'error': f"No se pudo eliminar el cliente: {error_data}"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"Error al conectar con la API: {e}"}, status=500)


# Crear un nuevo empleado
def crear_empleado(request):
    if request.method == 'POST':
        empleado_data = {
            'firstName': request.POST['firstName'],
            'lastName': request.POST['lastName'],
            'address': request.POST['address'],
            'email': request.POST['email'],
            'phoneNumber': request.POST['phoneNumber'],
            'hireDate': request.POST['hireDate'],
            'dni': request.POST['dni'],
            'status': request.POST['status'],
            'jobPosition': {
                'pkInt': request.POST['jobPositionId'],  # Identificador del puesto
            },
            'salaryHistory': {
                'currentSalary': request.POST['currentSalary'],  # Salario actual
                'changeReason': "Creación inicial"
            }
        }
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(EMPLOYEES_API_URL, json=empleado_data, headers=headers)
            if response.status_code == 201:
                return redirect('listar_empleados')
            else:
                return render(request, 'crear_empleado.html', {'error': response.json()})
        except requests.exceptions.RequestException as e:
            return render(request, 'crear_empleado.html', {'error': f"Error al conectar con la API: {e}"})
    return render(request, 'crear_empleado.html')

# Editar un empleado
def editar_empleado(request, empleado_id):
    try:
        # Obtener los datos actuales del empleado
        response = requests.get(f"{EMPLOYEES_API_URL}/{empleado_id}")
        if response.status_code == 200:
            empleado = response.json()
        else:
            return redirect('listar_empleados')

        if request.method == 'POST':
            empleado_data = {
                'firstName': request.POST['firstName'],
                'lastName': request.POST['lastName'],
                'address': request.POST['address'],
                'email': request.POST['email'],
                'phoneNumber': request.POST['phoneNumber'],
                'hireDate': request.POST['hireDate'],
                'dni': request.POST['dni'],
                'status': request.POST['status'],
                'jobPosition': {
                    'pkInt': request.POST['jobPositionId']
                },
                'salaryHistory': {
                    'currentSalary': request.POST['currentSalary'],
                    'changeReason': "Actualización"
                }
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.put(f"{EMPLOYEES_API_URL}/{empleado_id}", json=empleado_data, headers=headers)
            if response.status_code == 200:
                return redirect('listar_empleados')
            else:
                return render(request, 'editar_empleado.html', {'empleado': empleado, 'error': response.json()})

        return render(request, 'editar_empleado.html', {'empleado': empleado})

    except requests.exceptions.RequestException as e:
        return redirect('listar_empleados')

# Eliminar un empleado
def eliminar_empleado(request, empleado_id):
    try:
        response = requests.delete(f"{EMPLOYEES_API_URL}/{empleado_id}")
        if response.status_code == 204:
            return redirect('listar_empleados')
        else:
            return JsonResponse({'error': f"No se pudo eliminar el empleado: {response.json()}"})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"Error al conectar con la API: {e}"})
        
# ViewSets de la API
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha')
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        datos_pedido = request.data
        idCliente = datos_pedido.get('idCliente')  # Obtenemos el ID del cliente
        detalles = datos_pedido.get('detalles', [])

        # Consulta a la API externa para obtener los datos del cliente
        nombre_cliente = None
        try:
            response = requests.get(f"{BASE_URL}/{idCliente}/")
            if response.status_code == 200:
                cliente_data = response.json()
                nombre_cliente = cliente_data.get('nombres', 'Cliente Desconocido')
            else:
                return Response({"error": f"No se encontró el cliente en la API externa: {response.status_code}"}, status=400)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error al conectar con la API de clientes: {e}"}, status=500)

        # Crear el pedido
        pedido = Pedido.objects.create(idCliente=idCliente, nombre_cliente=nombre_cliente, total=0)

        # Crear los detalles del pedido
        total = 0
        for detalle in detalles:
            producto = Producto.objects.get(id=detalle['producto'])
            cantidad = detalle['cantidad']
            subtotal = producto.precio * cantidad

            # Crear el detalle del pedido
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal,
            )
            total += subtotal

        # Actualizar el total del pedido
        pedido.total = total
        pedido.save()

        serializer = self.get_serializer(pedido)
        return Response(serializer.data)

class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer

class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer

# ViewSet para Usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

# ViewSet para Actividad
class ActividadViewSet(viewsets.ModelViewSet):
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

# ViewSet para HistorialPrecio
class HistorialPrecioViewSet(viewsets.ModelViewSet):
    queryset = HistorialPrecio.objects.all()
    serializer_class = HistorialPrecioSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
