from django.db import models
from django.contrib.auth.models import User

class Comentario(models.Model):
    """Modelo para almacenar las opiniones de los clientes."""

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    texto_comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Muestra el nombre completo y la fecha de creación en el panel de administración
        return f'{self.nombre} {self.apellido} - ({self.fecha_creacion.strftime("%Y-%m-%d")})'

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        # Accede al username del usuario relacionado
        if self.user:
            return self.user.username
        return f"Usuario ID: {self.id}"

class Consulta(models.Model):
    # Cliente que hace la consulta
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        related_name='consultas_domicilio',
        verbose_name='Cliente',
        null=True,
        blank=True
    )

    # 1. Datos del Cliente y Ubicación Básica
    codigo_postal = models.CharField(max_length=10, verbose_name='Código Postal')
    colonia = models.CharField(max_length=100, verbose_name='Colonia')
    num_exterior = models.CharField(max_length=20, verbose_name='Número Exterior')
    comentario = models.TextField(verbose_name='Comentario')
    referencias = models.TextField(verbose_name='Referencias', null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    # 2. Referencias y Solicitud
    referencias = models.TextField(
        blank=True,
        null=True,
        verbose_name='Referencias',
        help_text="Color de casa, calle o negocio cercano."
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Solicitud'
    )

    class Meta:
        verbose_name = "Consulta a Domicilio"
        verbose_name_plural = "Consultas a Domicilio"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        if self.usuario and self.usuario.user:
            return f"Consulta de {self.usuario.user.username} - CP {self.codigo_postal}"
        return f"Consulta sin usuario - CP {self.codigo_postal}"

class Solicitud(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.username} - {self.servicio}"

class ServicioSolicitado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    aparato_nombre = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

class Cita(models.Model):
    """Modelo para registrar una cita de servicio agendada."""

    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('FINALIZADA', 'Finalizada'),
    ]

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='citas_agendadas'
    )

    fecha_cita = models.DateField(verbose_name="Fecha de la Cita")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita de {self.cliente.username} el {self.fecha_cita} a las {self.hora_inicio}"


