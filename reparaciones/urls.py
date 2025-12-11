from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # <-- Importamos las vistas de autenticación de Django

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. URLs de la aplicación 'local' (para la raíz del sitio)
    path('', include('local.urls')),
    
    # 2. URLs de la aplicación 'usuarios' (donde está tu vista de registro 'cuenta' y login)
    path('', include('usuarios.urls')), 
    
    # ====================================================================
    # 🔑 FLUJO DE RECUPERACIÓN DE CONTRASEÑA DE DJANGO
    # (Estas URLs usan el sistema de correo que configuraste en settings.py)
    # ====================================================================
    
    # 1. Muestra el formulario para ingresar el correo electrónico
    path('restablecer_contrasena/', 
         auth_views.PasswordResetView.as_view(
             template_name='usuarios/password_reset_form.html',
             email_template_name='usuarios/password_reset_email.html',
             subject_template_name='usuarios/password_reset_subject.txt',
             success_url='/restablecer_contrasena/enviado/'
         ), 
         name='restablecer_contrasena'), # Este 'name' es crucial, lo usa el enlace en tu HTML

    # 2. Página que informa que se ha enviado el correo
    path('restablecer_contrasena/enviado/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/password_reset_done.html'
         ), 
         name='password_reset_done'),

    # 3. Vista para cambiar la contraseña (usando el token del correo)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset_confirm.html',
             success_url='/restablecer_contrasena/completado/'
         ), 
         name='password_reset_confirm'),

    # 4. Confirmación de que el cambio fue exitoso
    path('restablecer_contrasena/completado/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
