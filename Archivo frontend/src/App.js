import React, { useState } from 'react';

function App() {
  const [query, setQuery] = useState(''); // Estado para la consulta del usuario
  const [response, setResponse] = useState(''); // Estado para la respuesta de la IA
  const [loading, setLoading] = useState(false); // Estado para indicar si la IA está pensando
  const [error, setError] = useState(''); // Estado para mensajes de error

  // Obtiene la URL del backend desde las variables de entorno (Vite)
  // Asegúrate de que esta variable esté configurada en tu archivo .env del frontend
  const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

  // Función para manejar el envío de la consulta
  const handleSubmit = async (e) => {
    e.preventDefault(); // Previene el comportamiento por defecto del formulario
    if (!query.trim()) {
      setError('Por favor, ingresa una pregunta.');
      return;
    }

    setLoading(true); // Activa el estado de carga
    setError(''); // Limpia cualquier error previo
    setResponse(''); // Limpia la respuesta anterior

    try {
      // Realiza una petición POST a tu API de backend
      const res = await fetch(`${BACKEND_URL}/ask-ai`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }), // Envía la consulta del usuario en formato JSON
      });

      if (!res.ok) {
        // Si la respuesta no es OK (ej. 400, 500), lanza un error
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Error al comunicarse con el servidor.');
      }

      const data = await res.json(); // Parsea la respuesta JSON
      setResponse(data.response); // Actualiza el estado con la respuesta de la IA
    } catch (err) {
      console.error('Error al enviar la consulta:', err);
      setError(`Ocurrió un error: ${err.message}. Por favor, intenta de nuevo.`);
    } finally {
      setLoading(false); // Desactiva el estado de carga
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-blue-400 to-green-500 font-inter">
      <div className="bg-white p-8 rounded-xl shadow-2xl w-full max-w-2xl transform transition-all duration-300 hover:scale-[1.01]">
        <h1 className="text-4xl font-bold text-center text-blue-700 mb-6">
          Pesc<span className="text-green-600">AI</span>: Guía de Pesca Inteligente
        </h1>
        <p className="text-center text-gray-600 mb-8">
          Pregúntale a la IA sobre lugares de pesca, especies, carnadas y más en Buenos Aires.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500 resize-y min-h-[100px]"
            placeholder="Ej: ¿Dónde puedo pescar pejerrey en la zona sur de Buenos Aires?"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setError(''); // Limpiar error al escribir
            }}
            disabled={loading}
          ></textarea>

          {error && (
            <p className="text-red-600 text-center text-sm">{error}</p>
          )}

          <button
            type="submit"
            className={`w-full py-3 px-4 rounded-lg text-white font-semibold transition-all duration-300 transform ${
              loading
                ? 'bg-blue-300 cursor-not-allowed animate-pulse'
                : 'bg-blue-600 hover:bg-blue-700 active:scale-95 shadow-md hover:shadow-lg'
            }`}
            disabled={loading}
          >
            {loading ? 'Pensando...' : 'Preguntar a PescAI'}
          </button>
        </form>

        {response && (
          <div className="mt-8 p-6 bg-blue-50 rounded-xl shadow-inner border border-blue-200">
            <h2 className="text-xl font-semibold text-blue-700 mb-3">Respuesta de PescAI:</h2>
            <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
              {response}
            </p>
          </div>
        )}
      </div>

      <footer className="mt-8 text-white text-sm text-center">
        &copy; {new Date().getFullYear()} PescAI. Desarrollado para pescadores en Buenos Aires.
      </footer>
    </div>
  );
}

export default App;
