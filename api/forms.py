from django import forms
from .models import Cliente , Producto

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        
        fields = ['nombres', 'apellidos', 'correo', 'telefono', 'dni', 'fechaRegistro']  
        exclude = ['fechaRegistro']  # Excluye el campo no editable

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock']  # Ajusta los campos según lo que necesites