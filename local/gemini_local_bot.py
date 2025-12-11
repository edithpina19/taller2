import os
from google import genai
from google.genai.errors import APIError
import time

# ==============================
# CONFIGURACIÓN GEMINI API (VERSION CORREGIDA CON LIBRERÍA OFICIAL)
# ==============================

# 1. Usar la clave directamente para tu prueba (Malo para producción, bueno para probar)
# En un entorno real, usarías os.environ.get("GEMINI_API_KEY")
API_KEY = "AIzaSyBvfB68OeSxrh-OBYl8aRHJZ-su-LeB28M"

# 2. Inicializar el cliente de la API (Solo si la clave está disponible)
CLIENT = None
if API_KEY and API_KEY.startswith("AIza"):
    try:
        CLIENT = genai.Client(api_key=API_KEY)
    except Exception as e:
        print(f"Error al inicializar el cliente de Gemini: {e}")
        CLIENT = None

if CLIENT is None:
    print("¡ERROR CRÍTICO! El cliente de la API de Gemini no se pudo inicializar.")

# 3. Definición del Contexto/Personalidad
LOCAL_INFO = """
Eres el asistente virtual oficial de *Instalaciones Universales*. 
Tu objetivo es responder preguntas sobre reparaciones, horarios, y cotizaciones iniciales. 
Sé conciso y profesional.
"""


def responder(pregunta: str, max_retries=3) -> str:
    """
    Realiza la llamada a la API de Gemini con lógica de reintento usando el cliente oficial.
    """
    if CLIENT is None:
        return "El servicio de chat no está configurado correctamente."

    # Combinamos la instrucción de contexto con la pregunta del usuario
    full_prompt = [LOCAL_INFO, pregunta]

    for attempt in range(max_retries):
        try:
            # 4. Llamada al Modelo (gestiona automáticamente la URL y los encabezados)
            response = CLIENT.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt
            )
            # 5. Respuesta exitosa
            return response.text

        except APIError as e:
            # Manejo de errores de la API (ej. clave incorrecta, límite de tasa 429)
            if attempt < max_retries - 1:
                print(f"Intento {attempt + 1} fallido (Error: {e}). Reintentando en 2 segundos...")
                time.sleep(2)
            else:
                return f"El servicio de chat no pudo responder después de {max_retries} intentos. Error final: {e}"
        except Exception as e:
            # Manejo de otros errores (red, JSON, etc.)
            return f"Ocurrió un error inesperado: {e}"

    # Fallback final si el bucle termina por alguna razón
    return "El servicio de chat no pudo responder después de varios intentos. Intente nuevamente más tarde."


# --- Ejemplo de uso ---
if __name__ == '__main__':
    if CLIENT:
        print(f"Respuesta de la IA: {responder('¿Cuál es su horario de atención hoy?')}")
    else:
        print("No se puede ejecutar la prueba debido a un error de configuración.")
