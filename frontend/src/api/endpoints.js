// Leemos la URL base de nuestro archivo .env
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Creamos un objeto que contendrá todas nuestras URLs y funciones de ayuda
export const API = {
  // Función para obtener la URL del plan del día
  getDailyPlanUrl: () => `${API_BASE_URL}/plan/hoy`,

  // Función para construir la URL de la lista de compras con sus parámetros
  getShoppingListUrl: (startDate, endDate) => {
    return `${API_BASE_URL}/lista-compras/view-shopping-list?dia_inicio=${startDate}&dia_fin=${endDate}`;
  },

  // Función para enviar la lista de compra a Google Tasks
  sendToTasksUrl: () => `${API_BASE_URL}/lista-compras/export-to-tasks`,

  // Función para enviar el plan a Google Tasks
  sendPlanToTasks: () => `${API_BASE_URL}/export-tasks/weekly-plan`,
  
  // Función para hacer el plan de toda la semana
  getWeeklyPlanUrl: () => `${API_BASE_URL}/plan/semanal`,

};

