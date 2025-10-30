// Leemos la URL base de nuestro archivo .env
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Creamos un objeto que contendrá todas nuestras URLs y funciones de ayuda
export const API = {
  // Función para obtener la URL del plan del día
  getDailyPlanUrl: () => `${API_BASE_URL}`,

  // Función para construir la URL de la lista de compras con sus parámetros
  getShoppingListUrl: (startDate, endDate) => {
    return `${API_BASE_URL}/lista-compras?dia_inicio=${startDate}&dia_fin=${endDate}`;
  },

  // Si tuviéramos más endpoints, los añadiríamos aquí como nuevas funciones
  // sendToTasksUrl: () => `${API_BASE_URL}/api/send-to-tasks`,
};