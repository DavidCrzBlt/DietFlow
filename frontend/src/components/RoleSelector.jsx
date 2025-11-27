// src/components/RoleSelector.jsx

import React from 'react';
import { useAuth } from '../hooks/useAuth';

const RoleSelector = () => {
    // Obtenemos las funciones necesarias del hook
    const { user, createProfile } = useAuth();

    const selectRole = async (selectedRole) => {
        if (!user) {
            console.error("No hay usuario autenticado para crear el perfil.");
            return;
        }

        try {
            await createProfile(
                user.uid, 
                selectedRole, 
                user.displayName, 
                user.email
            );
            // El hook useAuth ahora actualizará el estado 'role' y la redirección se ejecutará
            alert(`¡Perfil de ${selectedRole} creado con éxito!`);
        } catch (error) {
            console.error("Error al crear el perfil:", error);
            alert("Hubo un error al guardar tu perfil. Intenta de nuevo.");
        }
    };

    return (
        <div style={{ padding: '40px', textAlign: 'center' }}>
            <h2>¡Bienvenido a DietFlow!</h2>
            <p>Parece que es la primera vez que inicias sesión. Por favor, selecciona tu tipo de perfil:</p>
            
            <div style={{ display: 'flex', justifyContent: 'center', gap: '30px', marginTop: '30px' }}>
                <button 
                    onClick={() => selectRole('nutriologo')}
                    style={roleButtonStyle('nutriologo')}
                >
                    Soy Nutriólogo
                </button>
                <button 
                    onClick={() => selectRole('usuario')}
                    style={roleButtonStyle('usuario')}
                >
                    Soy Usuario (Paciente)
                </button>
            </div>
        </div>
    );
};

// Estilos básicos para las opciones
const roleButtonStyle = (role) => ({
    padding: '15px 30px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    borderRadius: '8px',
    border: `2px solid ${role === 'nutriologo' ? '#38A169' : '#3182CE'}`,
    backgroundColor: role === 'nutriologo' ? '#48BB78' : '#4299E1',
    color: 'white'
});

export default RoleSelector;