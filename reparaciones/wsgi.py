import os

from django.core.wsgi import get_wsgi_application

# Asegúrate de que 'reparaciones' sea el nombre de tu carpeta de configuración
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reparaciones.settings')

application = get_wsgi_application()