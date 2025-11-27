import { useState, useEffect } from 'react';
import { onAuthStateChanged, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { auth } from '../config/firebase'; 
import { doc, getDoc, setDoc } from "firebase/firestore"; 


export const useAuth = () => {
    // 1. Estado para almacenar la información del usuario autenticado
    const [user, setUser] = useState(null);
    const [role, setRole] = useState(null);
    // 2. Estado para indicar si la verificación inicial está completa
    const [loading, setLoading] = useState(true);

    const getUserProfile = async (uid) => {
        const userRef = doc(db, "users", uid);
        const docSnap = await getDoc(userRef);

        if (docSnap.exists()) {
            const profileData = docSnap.data();
            setRole(profileData.role);
            return profileData.role;
        } else {
            // No existe perfil: es un nuevo usuario o requiere selección de rol
            setRole(null); 
            return null;
        }
    };

    // Función para el inicio de sesión con Google
    const signInWithGoogle = async () => {
        try {
            const provider = new GoogleAuthProvider();
            // Abre una ventana emergente para el inicio de sesión
            const result = await signInWithPopup(auth, provider);
            // El resultado contiene el objeto 'user' de Firebase
            const newUser = result.user;
            // Verificar si el usuario ya tiene un perfil en Firestore
            await getUserProfile(newUser.uid);
            return newUser;
        } catch (error) {
            console.error("Error al iniciar sesión con Google:", error);
            // Manejar errores como la ventana emergente cerrada o fallos de red
            throw error; 
        }
    };

    const createProfile = async (uid, selectedRole, name, email) => {
        const userRef = doc(db, "users", uid);
        const newProfile = {
            role: selectedRole,
            name: name,
            email: email,
            registrationDate: new Date(),
            // nutrilogistId es opcional y se deja fuera si es nutriólogo, o se establece en null si es usuario
        };
        
        await setDoc(userRef, newProfile);
        setRole(selectedRole); // Actualiza el estado local del rol
        return newProfile;
    };

    // Escucha los cambios en el estado de autenticación (se ejecuta al montar)
    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
            if (currentUser) {
                setUser(currentUser);
                // Si hay usuario logeado, cargamos su perfil de Firestore
                await getUserProfile(currentUser.uid);
            } else {
                setUser(null);
                setRole(null);
            }
            setLoading(false);
        });

        // Limpieza: deja de escuchar cuando el componente se desmonta
        return () => unsubscribe();
    }, []);

    // Exportamos el estado y la función de login
    return { user, loading, role, signInWithGoogle, createProfile };
};