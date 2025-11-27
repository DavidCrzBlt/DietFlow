import React from 'react';
import { useAuth } from '../hooks/useAuth';

const Login = () => {
    // Usamos el hook para obtener la función de login
    const { signInWithGoogle } = useAuth();

    const handleLogin = async () => {
        try {
            const user = await signInWithGoogle();
            
            if (user) {
                // *** AQUÍ ES DONDE PASAREMOS AL PASO 4 ***
                // Por ahora, solo confirmamos que el login fue exitoso.
                console.log("¡Usuario autenticado con éxito!", user.uid);
                // Aquí se llamaría a la lógica para verificar/crear el perfil
            }
        } catch (error) {
            alert("Fallo al iniciar sesión. Verifica la consola.");
        }
    };

    return (
        <div style={{ padding: '20px', textAlign: 'center' }}>
            <h2>Bienvenido a DietFlow</h2>
            <p>Inicia sesión para comenzar el seguimiento de tu dieta.</p>
            <button 
                onClick={handleLogin} 
                style={{ padding: '10px 20px', cursor: 'pointer', backgroundColor: '#4285F4', color: 'white', border: 'none', borderRadius: '5px' }}
            >
                Iniciar Sesión con Google
            </button>
        </div>
    );
};

export default Login;