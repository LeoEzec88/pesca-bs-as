/** @type {import('tailwindcss').Config} */
export default {
  // Asegúrate de que Tailwind escanee todos tus archivos de componentes React
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Puedes añadir aquí fuentes, colores, etc. personalizados
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}