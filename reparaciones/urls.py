from django.contrib import admin
from django.urls import path, include # ¡IMPORTANTE importar include!

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conecta todas las URLs de tu app 'local' a la ruta raíz del sitio
    path('', include('local.urls')),
]