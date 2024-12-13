import os
from django.core.asgi import get_asgi_application

# Ajusta el nombre del módulo de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')

application = get_asgi_application()
