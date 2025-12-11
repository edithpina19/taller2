from django.urls import path
from .import views
from .views import bienvenido_view, ver_mi_cuenta, logout_view

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path("bienvenido/", bienvenido_view, name="bienvenido"),
    path("mi-cuenta/", ver_mi_cuenta, name="mi_cuenta"),
    path("logout/", logout_view, name="logout"),
]
