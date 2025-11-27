import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const ProtectedRoute = ({ allowedRoles, children }) => {
    const { user, loading, role } = useAuth();
    const location = useLocation();

    // Si todavía está cargando, retorna null para evitar parpadeo
    if (loading) return null; 

    // 1. Verificar si el usuario está autenticado y tiene rol
    if (user && role !== null) {
        // 2. Verificar si el rol del usuario está en la lista de roles permitidos
        if (allowedRoles.includes(role)) {
            return children;
        } else {
            // 3. Acceso Denegado: Redirigir a una página de inicio o de error
            // Asumimos que ROUTES.HOME es accesible para todos
            alert(`Acceso denegado. Tu rol (${role}) no puede ver esta página.`);
            return <Navigate to={ROUTES.HOME} replace />;
        }
    }
    
    // Si no está autenticado, el AuthGuard principal ya lo habrá capturado y redirigido al Login.
    // Si por algún motivo llegamos aquí, redirigimos a HOME (o Login si tienes esa ruta)
    return <Navigate to={ROUTES.HOME} replace />;
};

export default ProtectedRoute;

// Necesitas definir tus rutas, por ejemplo, en un archivo de constantes
const ROUTES = {
    HOME: '/',
    SHOPPING_LIST: '/shopping-list',
    WEEK_PLAN: '/week-plan',
    // ...
};