import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
# Esto es útil para el desarrollo local. En producción (DigitalOcean),
# las variables de entorno serán inyectadas directamente.
load_dotenv()

class Settings:
    """Clase para gestionar las configuraciones de la aplicación."""
    # Obtiene la clave API de OpenAI de las variables de entorno.
    # Si no se encuentra, se lanza un ValueError para evitar que la aplicación
    # inicie sin la clave necesaria.
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    if OPENAI_API_KEY is None:
        raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada.")

    # Puedes añadir otras configuraciones aquí, como la URL de la base de datos
    # DATABASE_URL: str = os.getenv("DATABASE_URL")
    # if DATABASE_URL is None:
    #     print("Advertencia: DATABASE_URL no está configurada. La funcionalidad de DB podría no funcionar.")


# Instancia de la configuración que se utilizará en la aplicación
settings = Settings()
# Puedes acceder a las configuraciones de la siguiente manera:
# print(settings.OPENAI_API_KEY)