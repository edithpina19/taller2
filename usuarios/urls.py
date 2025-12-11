from django.urls import path
from .import views
from .views import bienvenido_view, ver_mi_cuenta, logout_view

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path("bienvenido/", bienvenido_view, name="bienvenido"),
    path("mi-cuenta/", ver_mi_cuenta, name="mi_cuenta"),
    path("logout/", logout_view, name="logout"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name='password_reset'),
path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name='password_reset_complete'),
]
