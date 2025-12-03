from django.contrib import admin
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario, Comentario, Consulta, ServicioSolicitado, Cita

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'fecha_creacion', 'texto_comentario_resumen')
    list_filter = ('fecha_creacion',)
    search_fields = ('nombre', 'apellido', 'texto_comentario')

    def nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"
    nombre_completo.short_description = 'Autor'

    def texto_comentario_resumen(self, obj):
        return obj.texto_comentario[:75] + '...' if len(obj.texto_comentario) > 75 else obj.texto_comentario
    texto_comentario_resumen.short_description = 'Comentario'


class UsuarioAdmin(admin.ModelAdmin):
    # ⭐️ CORRECCIÓN CLAVE: Usar 'phone' en list_display
    list_display = ('get_username', 'get_email', 'phone')

    # ⭐️ CORRECCIÓN CLAVE: Usar 'phone' en search_fields
    search_fields = ('user__username', 'user__email', 'phone')

    # Métodos para acceder a los campos de User...
    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('get_usuario_nombre', 'codigo_postal', 'colonia', 'num_exterior', 'fecha_solicitud', 'comentario', 'telefono')
    list_filter = ('fecha_solicitud', 'codigo_postal')
    search_fields = (
        'usuario__user__username',
        'codigo_postal',
        'colonia',
        'referencias',
        'comentario',
        'telefono'
    )
    readonly_fields = (
        'usuario',
        'codigo_postal',
        'colonia',
        'num_exterior',
        'referencias',
        'fecha_solicitud',
        'comentario',
        'telefono'
    )
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('usuario', 'fecha_solicitud'),
        }),
        ('Detalles de la Ubicación y Problema', {
            'fields': (
                'codigo_postal',
                'colonia',
                'num_exterior',
                'referencias',
                'comentario',
                'telefono'
            ),
        }),
    )

    def get_usuario_nombre(self, obj):
        if obj.usuario and obj.usuario.user:
            return obj.usuario.user.username
        return f"Usuario ID: {obj.usuario.id}" if obj.usuario else "Sin usuario"
    get_usuario_nombre.short_description = 'Usuario'

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'servicio', 'fecha', 'comentario')
    list_filter = ('servicio', 'fecha')
    search_fields = ('usuario__username', 'servicio', 'comentario')

@admin.register(ServicioSolicitado)
class ServicioSolicitadoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'aparato_nombre', 'cantidad', 'fecha_solicitud')
    list_filter = ('aparato_nombre', 'fecha_solicitud')
    search_fields = ('usuario__username', 'aparato_nombre')


class CitaAdmin(admin.ModelAdmin):
    # list_display: Usamos los nombres reales de los campos del modelo
    # y los métodos personalizados (cliente_nombre, estado_display).
    list_display = (
        'cliente_nombre',
        'fecha_cita',
        'hora_inicio',
        'hora_fin',
        'estado_display',
        'fecha_creacion'
    )

    # list_filter: SOLO acepta campos de modelo o relaciones.
    # Usamos los nombres reales: 'cliente' y 'fecha_cita', 'estado'.
    list_filter = ('cliente', 'fecha_cita', 'estado')

    # search_fields: Usamos los nombres reales de los campos donde se puede buscar.
    search_fields = (
        'cliente__username',  # Busca por el nombre de usuario del cliente
        'fecha_cita',  # Busca por fecha (aunque es un DateField, permite búsquedas parciales)
        'estado'
    )

    # readonly_fields: Usa los nombres reales de los campos del modelo.
    readonly_fields = (
        'cliente',
        'fecha_cita',
        'hora_inicio',
        'hora_fin',
        'estado',
        'fecha_creacion'  # El campo auto_now_add siempre es de solo lectura
    )

    fieldsets = (
        ('Información del Cliente y Creación', {
            'fields': ('cliente', 'fecha_creacion'),
        }),
        ('Detalles de la Cita', {
            # Los campos deben ser los nombres reales: fecha_cita, hora_inicio, hora_fin, estado
            'fields': ('fecha_cita', 'hora_inicio', 'hora_fin', 'estado'),
        }),
    )

    # --- Métodos personalizados ---

    def cliente_nombre(self, obj):
        # El campo real se llama 'cliente', accedemos a su username.
        return obj.cliente.username

    cliente_nombre.short_description = 'Cliente'

    def estado_display(self, obj):
        # Muestra el estado legible. Django lo hace automáticamente para campos 'choices',
        # pero podemos usar este método para dar formato si es necesario.
        return obj.get_estado_display()

    estado_display.short_description = 'Estado'

    # Nota: No necesitamos el método 'estado_cita' basado en timezone,
    # ya que tu modelo tiene un campo 'estado' explícito.

admin.site.register(Cita, CitaAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Consulta, ConsultaAdmin)

