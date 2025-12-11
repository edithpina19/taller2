from pathlib import Path
import os
from dotenv import load_dotenv   # <-- IMPORTANTE
import dj_database_url
# Cargar variables del archivo .env (si existe)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-m_k-c_k820d=d(e8_e=q=0+e(f1c50y*f+y)n-n)e-n-n'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','taller2-1-ct9t.onrender.com','.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'local',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reparaciones.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reparaciones.wsgi.application'
# --- INICIO DEL CÓDIGO MODIFICADO PARA COMPATIBILIDAD RENDER/LOCAL ---
# Intentamos obtener la URL de la base de datos de la variable de entorno (Render)
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # ----------------------------------------------------
    # CONFIGURACIÓN DE PRODUCCIÓN (RENDER)
    # ----------------------------------------------------
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            # Render a menudo requiere SSL si se usa una conexión externa
            # Si la conexión falla, podrías necesitar añadir:
            # ssl_require=True
        )
    }

    # También es una buena práctica forzar DEBUG=False y usar la clave secreta de Render
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY) # Usa la variable de entorno si existe
    
    # Configura ALLOWED_HOSTS para que funcione en Render (usando el nombre del host externo)
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

else:
    # ----------------------------------------------------
    # CONFIGURACIÓN DE DESARROLLO (LOCAL)
    # ----------------------------------------------------
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'LOCAL', # Tu nombre local
            'USER': 'postgres', # Tu usuario local
            'PASSWORD': '1234Abcd.', # Tu contraseña local
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    
    # En desarrollo, mantenemos el DEBUG y el ALLOWED_HOSTS originales
    # DEBUG = True (ya está al principio, lo mantenemos)
    # ALLOWED_HOSTS = ['127.0.0.1', 'localhost', ...] (ya está al principio, lo mantenemos)

# --- FIN DEL CÓDIGO MODIFICADO ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
LOGIN_URL = 'iniciar_sesion'
LOGIN_REDIRECT_URL = 'mis_solicitudes'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# --- Configuración del servidor (CRÍTICO) ---
# Usamos Gmail directamente. Si estuviera en .env, sería: os.environ.get('EMAIL_HOST')
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
EMAIL_USE_SSL = False # Si usas 587 con TLS, asegúrate de que SSL sea False

# --- Credenciales ---
# Las usaremos directamente aquí ya que las proporcionaste:
EMAIL_HOST_USER = 'pinaportilloedith2@gmail.com'  
EMAIL_HOST_PASSWORD = 'mfoq ukzq ymhp qhsg' 

# --- Remitentes ---
# La dirección que aparecerá como remitente por defecto (IMPORTANTE: ¡DEBE COINCIDIR CON HOST_USER!)
DEFAULT_FROM_EMAIL = 'INSTALACIONES UNIVERSALES <pinaportilloedith2@gmail.com>' 
# El texto que envías ('no-responder@tudominio.com') debe ser el mismo correo de EMAIL_HOST_USER, 
# o Gmail lo bloqueará.

SERVER_EMAIL = EMAIL_HOST_USER # Correo para errores del servidor
# =============================================================
# -------------------------------------------------------------

# ... (resto de tu código)

# Dirección que aparecerá como remitente por defecto
DEFAULT_FROM_EMAIL = 'INSTALACIONES UNIVERSALES <no-responder@tudominio.com>' 
SERVER_EMAIL = EMAIL_HOST_USER # Correo para errores del servidor

# Configuración adicional para Django Auth (Recuperación de Contraseña)
# URL a la que redirigir después de que el proceso de restablecimiento ha sido completado.
PASSWORD_RESET_REDIRECT_URL = 'iniciar_sesion' # Redirigir a la página de inicio de sesión

# =============================================================
# -------------------------------------------------------------

LANGUAGE_CODE = 'es-mx'
# ... (resto de tu código)

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ... Después de STATIC_ROOT ...

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # <--- ¡AGREGA ESTA LÍNEA!


