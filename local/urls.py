from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('servicios/', views.servicios, name='servicios'),
path('iniciar-sesion/', views.login_view, name='iniciar_sesion'),
    path('contacto/', views.contacto, name='contacto'),
    path("sobre-nosotros/", views.sobre_nosotros_view, name="sobre_nosotros"),
    path("cuenta/", views.cuenta, name="cuenta"),
    path('cuentas/', include('usuarios.urls')),
    path('registro/', views.registro, name='registro'),
    path('opiniones/', views.opiniones, name='opiniones'),
    path('consulta_personalizada/', views.consulta_personalizada, name='consulta_personalizada'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('agregar-servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('agregar-servicios-masivo/', views.agregar_servicios_masivo, name='agregar_servicios_masivo'),
    path('agendar-cita/', views.agendar_cita, name='agendar_cita'),
    path('api/agendar-cita/', views.api_agendar_cita_post, name='api_agendar_cita_post'),
    path('api/disponibilidad/', views.api_disponibilidad, name='api_disponibilidad'),
    path("api/chatbot/", views.chatbot_api, name="chatbot_api"),
    path("logout/", views.logout_view, name="logout"),
    path("huella_carbono/", views.huella_carbono, name="huella_carbono"),
    path("terminos/", views.terminos, name="terminos"),

]
