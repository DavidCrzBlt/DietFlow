import React from 'react';
import { useAuth } from '../hooks/useAuth';
import Login from './Login';
import RoleSelector from './RoleSelector';
// Importa el componente que quieres mostrar cuando el usuario está listo (tu <Navbar />)

const AuthGuard = ({ children }) => {
    const { user, loading, role } = useAuth();

    // 1. Estado de Carga Inicial
    if (loading) {
        // Podrías mostrar un Spinner o Skeleton
        return <div style={{ textAlign: 'center', padding: '50px' }}>Cargando datos de usuario...</div>;
    }

    // 2. Estado: Usuario No Autenticado
    if (!user) {
        // Si no hay usuario, redirigimos a la pantalla de Login
        // NOTA: Si usas react-router-dom, podrías redirigir a una ruta /login
        // Pero para simplificar, lo mostramos directamente aquí.
        return <Login />;
    }

    // 3. Estado: Usuario Autenticado pero sin Rol (Primera vez)
    if (user && role === null) {
        // Forzar la selección de rol. Esto bloqueará el resto de la aplicación
        return <RoleSelector />;
    }

    // 4. Estado: Usuario Autenticado Y con Rol
    // Si llegamos aquí, el usuario está listo para usar la app
    return <>{children}</>;
};

export default AuthGuard;