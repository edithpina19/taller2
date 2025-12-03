import os
from dotenv import load_dotenv  # Importa la librería dotenv
from google import genai
from google.genai.errors import APIError

# Carga las variables del archivo .env
load_dotenv()

# La librería de Google ya busca la clave en la variable GEMINI_API_KEY
# pero la cargamos explícitamente para asegurar que dotenv funcione.
API_KEY = os.getenv("GEMINI_API_KEY")


def get_gemini_response(prompt):
    """
    Envía un prompt a la API de Gemini y devuelve la respuesta.
    """
    if not API_KEY:
        return "Error: Clave API no encontrada en el entorno."

    try:
        # Inicializa el cliente usando la clave cargada
        client = genai.Client(api_key=API_KEY)

        # Usaremos el historial de chat para mantener el contexto
        # Si esta es la primera pregunta, crea el chat; sino, continúa.
        # (Para este ejemplo simple, creamos un chat nuevo en cada llamada)

        # Configuramos el modelo para que actúe como un asistente de reparaciones
        system_prompt = "Eres un asistente experto para 'Instalaciones Universales', enfocado en diagnosticar y orientar sobre servicios de reparación de electrónica y electrodomésticos."

        chat = client.chats.create(
            model="gemini-2.5-flash",
            system_instruction=system_prompt  # Le da un rol específico
        )

        response = chat.send_message(prompt)

        return response.text

    except APIError as e:
        return f"Error de API (consulta los logs del servidor): {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado: {e}"

# --- Ejemplo de prueba ---
# if __name__ == '__main__':
#     test_prompt = "¿Qué debo hacer si mi televisor LED no enciende?"
#     print(f"Asistente responde: {get_gemini_response(test_prompt)}")