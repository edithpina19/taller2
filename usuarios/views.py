from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def login_view(request):
    if request.method == "POST":
        user = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=user, password=password)

        if usuario is not None:
            login(request, usuario)
            request.session["username"] = usuario.username
            return redirect("bienvenido")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "usuarios/login.html")

def bienvenido_view(request):
    nombre = request.session.get("username", "Invitado")
    return render(request, "usuarios/bienvenido.html", {"nombre": nombre})

def ver_mi_cuenta(request):
    usuario = request.session.get("username")

    if not usuario:
        messages.error(request, "Debes iniciar sesión o crear una cuenta para ver tu perfil.")
        return redirect("login")  # Lo mandamos al login

    # Si está logeado, muestra su perfil
    return render(request, "usuarios/mi_cuenta.html", {"usuario": usuario})

def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    return redirect("index")  # lo manda a la página principal

# Create your views here.

@csrf_exempt
def chat_with_gemini(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            prompt = data.get('prompt', '')

            if not prompt:
                return JsonResponse({'success': False, 'error': 'No se proporcionó pregunta'}, status=400)

            respuesta_ia = get_gemini_response(prompt)
            return JsonResponse({'success': True, 'response': respuesta_ia})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f"Error interno: {str(e)}"}, status=500)

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
