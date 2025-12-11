# ARCHIVO DE VIEWS/LOCAL
import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import Usuario, Comentario, Consulta, Solicitud, ServicioSolicitado, Cita
from .gemini_local_bot import responder

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data.get("message", "")

            respuesta = responder(message)

            return JsonResponse({"reply": respuesta})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

# ------------------------------
# PÁGINAS BÁSICAS
# ------------------------------

def index(request):
    return render(request, 'local/index.html')


def servicios(request):
    return render(request, 'local/servicios.html')


def sobre_nosotros_view(request):
    return render(request, "local/sobre_nosotros.html")


def contacto(request):
    return render(request, 'local/contacto.html')

def terminos(request):
    return render(request, 'local/terminos.html')

# ------------------------------
# OPINIONES / COMENTARIOS
# ------------------------------

def opiniones(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        comentario_texto = request.POST.get('comentario')

        if nombre and apellido and comentario_texto:
            Comentario.objects.create(
                nombre=nombre,
                apellido=apellido,
                email=email,
                texto_comentario=comentario_texto
            )

        return redirect('opiniones')

    comentarios = Comentario.objects.all().order_by('-fecha_creacion')

    return render(request, 'local/opiniones.html', {'comentarios': comentarios})


# ------------------------------
# AUTENTICACIÓN / REGISTRO
# ------------------------------

def autenticacion_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    return render(request, 'local/iniciar_sesion.html')


def login_view(request):
    # Si YA está logueado → lo mandamos al inicio, NO al login
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'local/iniciar_sesion.html')

def registro(request):

    # Forzar limpieza de sesión fantasma
    if request.user.is_authenticated:
        logout(request)

    if request.method == 'POST':
        username = request.POST.get('new_username')
        password = request.POST.get('new_password')
        email = request.POST.get('email')

        if not username or not password:
            messages.error(request, 'Faltan datos obligatorios')
            # Si usas 'registro' en tu urls.py para la vista de registro (cuenta.html), usa 'registro'. 
            # Si usas 'cuenta', usa 'cuenta'. Asumo que estás usando 'registro' para esta vista, pero redirige a la URL 'registro'
            return redirect('registro') 

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Ese usuario ya existe')
            return redirect('registro')

        # Crea el usuario en la tabla de User de Django
        User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        messages.success(request, 'Cuenta creada correctamente. ¡Ahora inicia sesión!')
        
        # 🚨 CORRECCIÓN CLAVE: Redirige al usuario a la página de LOGIN ('iniciar_sesion')
        # para que ingrese con la cuenta recién creada.
        return redirect('iniciar_sesion')

    # Renderiza la plantilla de registro ('cuenta.html' es tu plantilla de registro)
    return render(request, 'local/cuenta.html')

def consulta_personalizada(request):
    if request.method == "POST":
        usuario_nombre = request.POST.get("usuario")

        # Primero obtener o crear el User
        user_obj, created = User.objects.get_or_create(username=usuario_nombre)
        # Luego obtener o crear el Usuario relacionado
        usuario_obj, created = Usuario.objects.get_or_create(user=user_obj)

        Consulta.objects.create(
            usuario=usuario_obj,
            codigo_postal=request.POST.get("codigo_postal"),
            colonia=request.POST.get("colonia"),
            num_exterior=request.POST.get("num_exterior"),
            referencias=request.POST.get("referencias"),
            comentario=request.POST.get("comentario"),
            telefono=request.POST.get("telefono"),
        )

        return render(request, "local/consulta_personalizada.html", {
            "mensaje": "Tu consulta fue enviada con éxito"
        })

    return render(request, "local/consulta_personalizada.html")

# ------------------------------
# CUENTA / SOLICITUDES
# ------------------------------

@login_required
def mis_solicitudes(request):
    # 1. Obtener solicitudes del modelo antiguo (si todavía lo usas)
    solicitudes_antiguas = Solicitud.objects.filter(cliente=request.user).order_by('-fecha_creacion')

    # 2. Obtener los servicios solicitados masivamente
    servicios_solicitados = ServicioSolicitado.objects.filter(usuario=request.user).order_by('-fecha_solicitud')

    contexto = {
        'solicitudes_antiguas': solicitudes_antiguas,
        'servicios_solicitados': servicios_solicitados,
    }

    return render(request, 'local/mis_solicitudes.html', contexto)


@login_required
def cuenta(request):
    # Nota: Esta vista está protegida por @login_required. 
    # Si el registro redirigiera aquí, causaría el error anterior si el usuario no estuviera logueado.
    solicitudes = Solicitud.objects.filter(cliente=request.user)

    return render(request, 'local/cuenta.html', {
        'usuario': request.user,
        'solicitudes': solicitudes
    })


# ------------------------------
# CERRAR SESIÓN
# ------------------------------

def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')

def logout_view(request):
    request.session.flush()  # elimina toda la sesión
    return redirect("index")  # lo manda a la página principal 

def huella_carbono(request):
    return render(request, 'huella_carbono.html')


@login_required
def agregar_servicio(request):
    if request.method == 'POST':

        # 1. 🔑 OBTENER DATOS DE FORMA SEGURA USANDO .get()
        aparato_codigo = request.POST.get('aparato_code')
        cantidad_str = request.POST.get('cantidad')

        if not aparato_codigo or not cantidad_str:
            messages.error(request, "Error: Faltan datos esenciales del formulario (código o cantidad).")
            return redirect('servicios')

        # 2. 🔢 VALIDAR Y CONVERTIR LA CANTIDAD
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                messages.error(request, "La cantidad debe ser mayor a cero.")
                return redirect('servicios')

        except (ValueError, TypeError):
            messages.error(request, "Error: La cantidad enviada no es un número válido.")
            return redirect('servicios')

        # 3. 💾 LÓGICA DE GUARDADO EN LA BASE DE DATOS
        try:
            ServicioSolicitado.objects.create(
                usuario=request.user,  
                aparato_nombre=aparato_codigo,  
                cantidad=cantidad,
            )

            # 4. ✅ MENSAJE DE ÉXITO Y REDIRECCIÓN
            messages.success(request, f"¡Solicitud de {cantidad}x {aparato_codigo} registrada en Admin con éxito!")
            return redirect('servicios')  

        except Exception as e:
            # 5. ❌ MANEJO DE ERRORES DE LA BASE DE DATOS
            print(f"ERROR DURANTE EL GUARDADO: {e}")
            messages.error(request, f"No se pudo registrar la solicitud: {e}")
            return redirect('servicios')


@login_required
def agregar_servicios_masivo(request):
    if request.method == 'POST':
        try:
            total_items_count = int(request.POST.get('total_items_count', 0))
        except (ValueError, TypeError):
            total_items_count = 0

        if total_items_count == 0:
            messages.warning(request, "No se encontraron aparatos seleccionados.")
            return redirect('servicios')

        for i in range(total_items_count):
            aparato_code = request.POST.get(f'item_{i}_code')
            cantidad = request.POST.get(f'item_{i}_qty')

            try:
                cantidad = int(cantidad)
            except (TypeError, ValueError):
                cantidad = 0

            if aparato_code and cantidad > 0:
                ServicioSolicitado.objects.create(
                    aparato_nombre=aparato_code,
                    cantidad=cantidad,
                    usuario=request.user
                )

        messages.success(request,
                         f"Se registraron {total_items_count} tipo(s) de servicio masivamente. ¡Ahora agenda tu cita!")

        return redirect('agendar_cita')

    return redirect('servicios')


@login_required
def agendar_cita(request):
    """
    Renderiza la plantilla HTML del calendario.
    """
    return render(request, 'local/agendar_cita.html')


# --------------------------------------------------------------------------
# ⭐️ VISTA DE API PARA PROCESAR EL POST (Backend POST) ⭐️
# --------------------------------------------------------------------------

@csrf_exempt 
@login_required
def api_agendar_cita_post(request):
    """
    API para recibir la cita agendada por el cliente (POST) y guardarla en la BD.
    """
    if request.method == 'POST':
        try:
            # 1. Obtener datos JSON del cuerpo de la solicitud
            data = json.loads(request.body)

            # 2. Obtener y validar datos
            fecha_cita_str = data.get('fecha_cita')
            hora_inicio_str = data.get('hora_inicio')
            hora_fin_str = data.get('hora_fin')

            cliente = request.user 

            # 3. Conversión de formatos para el modelo Cita
            fecha_cita_obj = datetime.strptime(fecha_cita_str, '%Y-%m-%d').date()
            hora_inicio_obj = datetime.strptime(hora_inicio_str, '%H:%M:%S').time()
            hora_fin_obj = datetime.strptime(hora_fin_str, '%H:%M:%S').time()

            # 4. Crear y guardar la instancia del modelo
            cita = Cita.objects.create(
                cliente=cliente,
                fecha_cita=fecha_cita_obj,
                hora_inicio=hora_inicio_obj,
                hora_fin=hora_fin_obj,
                estado='PENDIENTE'
            )

            # 5. Respuesta de éxito
            return JsonResponse({
                'status': 'success',
                'message': 'Cita guardada con éxito',
                'cita_id': cita.pk,
            }, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest(json.dumps({'status': 'error', 'message': 'Formato JSON inválido.'}),
                                          content_type="application/json")
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def api_disponibilidad(request):
    # Esta función asume que tienes definida la variable CUPOS_MAXIMOS_POR_DIA en algún lugar
    # Si no la tienes, esta función generará un NameError.
    
    # Define CUPOS_MAXIMOS_POR_DIA aquí si no está globalmente definido
    # CUPOS_MAXIMOS_POR_DIA = 10 
    
    start_date_str = request.GET.get('start')
    end_date_str = request.GET.get('end')

    if not start_date_str or not end_date_str:
        return JsonResponse([], safe=False)

    try:
        # Intenta obtener la variable global, si no está definida, usa un valor por defecto seguro.
        CUPOS_MAXIMOS_POR_DIA = globals().get('CUPOS_MAXIMOS_POR_DIA', 10)
    except NameError:
         CUPOS_MAXIMOS_POR_DIA = 10 

    citas_en_rango = Cita.objects.filter(
        fecha_cita__gte=start_date_str,
        fecha_cita__lte=end_date_str,
        estado='CONFIRMADA'
    ).values('fecha_cita').annotate(conteo=Count('fecha_cita'))

    eventos = []

    for cita_dia in citas_en_rango:
        dia = cita_dia['fecha_cita'].isoformat()
        conteo = cita_dia['conteo']

        cupos_restantes = CUPOS_MAXIMOS_POR_DIA - conteo

        if cupos_restantes <= 0:
            color = '#ff4d4d'
            titulo = 'DÍA LLENO'
        elif cupos_restantes <= 3:
            color = '#ffa500'
            titulo = f'Quedan {cupos_restantes} cupos'
        else:
            color = '#38b000'
            titulo = f'{cupos_restantes} cupos disponibles'

        eventos.append({
            'title': titulo,
            'start': dia,
            'allDay': True,
            'color': color,
            'display': 'background',
        })

    return JsonResponse(eventos, safe=False)
