// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
  apiKey: import.meta.env.VITE_APIKEY_FIREBASE,
  authDomain: import.meta.env.VITE_AUTHDOMAIN_FIREBASE,
  projectId: import.meta.env.VITE_PROJECTID_FIREBASE,
  storageBucket: import.meta.env.VITE_STORAGEBUCKET_FIREBASE,
  messagingSenderId: import.meta.env.VITE_MESSAGINGSENDERID_FIREBASE,
  appId: import.meta.env.VITE_APPID_FIREBASE,
  measurementId: import.meta.env.VITE_MEASUREMENTID_FIREBASE
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

const analytics = getAnalytics(app);
// Exportar servicios que usaremos (Auth y Firestore)
export const auth = getAuth(app);
export const db = getFirestore(app);