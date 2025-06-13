from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Para definir la estructura de los datos de entrada
from backend.services import get_ai_fishing_info # Importa la función de servicio de la IA

# Inicializa la aplicación FastAPI
app = FastAPI(
    title="PescAI Backend API",
    description="API para obtener información de pesca asistida por IA para Buenos Aires.",
    version="1.0.0"
)

# Configuración de CORS (Cross-Origin Resource Sharing)
# Esto es crucial para que tu frontend (que corre en un dominio/puerto diferente)
# pueda hacer peticiones a tu backend.
origins = [
    "http://localhost",
    "http://localhost:5173",  # Puerto por defecto de Vite
    "http://localhost:3000",  # Puerto por defecto de Create React App
    # Cuando despliegues en DigitalOcean, añadirás aquí las URLs de tu frontend desplegado
    # Ejemplo: "https://your-frontend-app.ondigitalocean.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite solicitudes desde los orígenes especificados
    allow_credentials=True,      # Permite el uso de cookies y credenciales
    allow_methods=["*"],         # Permite todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],         # Permite todos los encabezados HTTP
)

# Define el modelo de datos para la solicitud de la IA
# El frontend enviará un JSON con un campo 'query'
class QueryRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    """Ruta raíz para verificar que la API está funcionando."""
    return {"message": "¡Bienvenido a la API de PescAI! La API está funcionando."}

@app.post("/ask-ai")
async def ask_ai_endpoint(request: QueryRequest):
    """
    Endpoint para solicitar información de pesca a la IA.

    Recibe una consulta de texto y devuelve la respuesta generada por la IA.
    """
    if not request.query.strip():
        # Si la consulta está vacía, devuelve un error 400 Bad Request
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")

    # Llama a la función de servicio que interactúa con la IA
    ai_response_text = await get_ai_fishing_info(request.query)

    # Devuelve la respuesta de la IA al frontend
    return {"response": ai_response_text}

# Puedes añadir más rutas aquí en el futuro para:
# - CRUD de lugares de pesca (si tienes una DB)
# - Autenticación de usuarios
# - Otros servicios
# Nota: Asegúrate de que tu archivo .env esté configurado correctamente
# y que las variables de entorno estén disponibles en tu entorno de despliegue.