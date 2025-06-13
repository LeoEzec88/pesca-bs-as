import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css'; // Importa los estilos de Tailwind

// Crea una raíz de renderizado para tu aplicación React
const root = ReactDOM.createRoot(document.getElementById('root'));

// Renderiza el componente App dentro de la raíz
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
// Si estás utilizando React 18 o superior, asegúrate de que tu archivo index.js esté configurado correctamente
// para usar ReactDOM.createRoot como se muestra arriba.