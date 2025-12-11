import os
import time
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv  # ### NUEVO: Importar librería para leer .env

# ==============================
# CONFIGURACIÓN GEMINI API (MODO SEGURO)
# ==============================

# 1. Cargar las variables del archivo .env
# Esto busca un archivo .env en la carpeta y carga las claves en memoria
load_dotenv() 

# 2. Obtener la clave desde el entorno (Ya no está escrita aquí)
# "GEMINI_API_KEY" debe coincidir con el nombre que escribiste dentro del archivo .env
API_KEY = os.getenv("GEMINI_API_KEY") 

# Verificación de seguridad antes de intentar conectar
if not API_KEY:
    print("¡ERROR CRÍTICO! No se encontró la variable GEMINI_API_KEY.")
    print("Asegúrate de haber creado el archivo .env y que tenga la clave dentro.")
else:
    print("Clave detectada correctamente (Oculta por seguridad).")

# 3. Inicializar el cliente de la API
CLIENT = None
if API_KEY:
    try:
        CLIENT = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error al inicializar el cliente de Gemini: {e}")
        CLIENT = None

if CLIENT is None:
    print("No se pudo iniciar el cliente. Revisa tu conexión o tu API Key.")

# 4. Definición del Contexto/Personalidad
LOCAL_INFO = """
Eres el asistente virtual oficial de Instalaciones Universales. 
Tu objetivo es responder preguntas sobre reparaciones, horarios, y cotizaciones iniciales. 
Sé conciso y profesional.
"""

def responder(pregunta: str, max_retries=3) -> str:
    """
    Realiza la llamada a la API de Gemini con lógica de reintento.
    """
    if CLIENT is None:
        return "Error interno: El servicio de chat no está configurado (Falta API Key)."

    # Combinamos la instrucción de contexto con la pregunta del usuario
    full_prompt = [LOCAL_INFO, pregunta]

    for attempt in range(max_retries):
        try:
            # Llamada al Modelo
            response = CLIENT.models.generate_content(
                model="gemini-2.5-flash", # Ojo: Verifica si usas 1.5 o 2.0 según tu acceso
                contents=full_prompt
            )
            return response.text

        except APIError as e:
            # Manejo de errores de la API
            if attempt < max_retries - 1:
                print(f"Intento {attempt + 1} fallido (Error: {e}). Reintentando en 2 segundos...")
                time.sleep(2)
            else:
                return f"El servicio de chat no pudo responder. Error final: {e}"
        except Exception as e:
            return f"Ocurrió un error inesperado: {e}"

    return "El servicio no responde. Intente más tarde."


# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Esta prueba solo corre si ejecutas el archivo directamente
    if CLIENT:
        print("Probando conexión...")
        respuesta = responder('¿Cuál es su horario de atención hoy?')
        print(f"Respuesta de la IA: {respuesta}")
    else:
        print("No se puede ejecutar la prueba. Falta configuración.") 
