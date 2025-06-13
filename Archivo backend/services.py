import os
import openai
from openai import OpenAI
from backend.config import settings # Importa la configuración de la clave API

# Inicializa el cliente de OpenAI con la clave API
# Usamos la clave de las settings, que la obtiene de las variables de entorno
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def get_ai_fishing_info(user_query: str) -> str:
    """
    Solicita información de pesca a la API de OpenAI.

    Args:
        user_query (str): La pregunta o consulta del usuario.

    Returns:
        str: La respuesta generada por la IA.
    """
    try:
        # Definición del sistema de la IA para guiar sus respuestas.
        # Es crucial para que la IA se comporte como un experto en pesca en BA.
        system_prompt = (
            "Eres un asistente experto en lugares y técnicas de pesca en la provincia de Buenos Aires, Argentina. "
            "Proporciona información útil y precisa sobre especies, carnadas, temporadas, "
            "reglamentaciones y ubicaciones específicas. Responde de manera clara y concisa, "
            "enfocándote en la pesca en Buenos Aires. Si la pregunta no está relacionada con la pesca en Buenos Aires, "
            "amablemente indícalo."
        )

        # Realiza la llamada a la API de OpenAI
        chat_completion = await client.chat.completions.create(
            model="gpt-4o",  # Puedes usar otros modelos como "gpt-3.5-turbo" si prefieres
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            max_tokens=500,  # Limita la longitud de la respuesta para evitar costos excesivos
            temperature=0.7, # Controla la creatividad de la respuesta (0.0 es más determinista)
        )

        # Extrae el contenido de la respuesta
        ai_response_content = chat_completion.choices[0].message.content
        return ai_response_content

    except openai.APIConnectionError as e:
        # Manejo de errores de conexión a la API
        print(f"Error de conexión a la API de OpenAI: {e}")
        return "Lo siento, hubo un problema de conexión con la inteligencia artificial. Por favor, verifica tu conexión a internet o intenta de nuevo más tarde."
    except openai.RateLimitError as e:
        # Manejo de errores de límite de solicitudes
        print(f"Error de límite de solicitudes de la API de OpenAI: {e}")
        return "Hemos alcanzado el límite de solicitudes. Por favor, espera un momento e intenta de nuevo."
    except openai.APIStatusError as e:
        # Manejo de otros errores de la API (ej. clave inválida, error interno del servidor)
        print(f"Error de la API de OpenAI (código {e.status_code}): {e.response}")
        return "Lo siento, la inteligencia artificial devolvió un error. Asegúrate de que tu clave API sea válida."
    except Exception as e:
        # Manejo de cualquier otro error inesperado
        print(f"Ocurrió un error inesperado al interactuar con la IA: {e}")
        return "Lo siento, ocurrió un error inesperado al procesar tu solicitud. Por favor, intenta de nuevo."

# Si quisieras integrar una base de datos (ejemplo conceptual, no implementado aquí):
# async def get_fishing_places_from_db(place_name: str):
#     """
#     Función conceptual para buscar lugares de pesca en una base de datos local.
#     Esto se ejecutaría DESPUÉS de que la IA mencione un lugar.
#     """
#     # Aquí iría tu lógica para conectar con PostgreSQL/MongoDB
#     # y buscar información detallada del lugar (coordenadas, fotos, etc.)
#     pass
# Nota: Asegúrate de que la clave API de OpenAI esté configurada correctamente
# en tu entorno de producción (DigitalOcean) para que este servicio funcione.