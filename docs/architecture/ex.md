HIGH LEVEL ARCHITECTURE — DietFlow (versión MVP)

Descripción general
DietFlow es una aplicación web enfocada en digitalizar el proceso de creación, gestión y seguimiento de planes de alimentación entre nutriólogos y pacientes. El objetivo principal es eliminar la fricción de los PDFs, automatizar recordatorios, generar listas de compras y facilitar el seguimiento del progreso del usuario —todo desde una interfaz web accesible en móvil mediante PWA.

🔥 1. Actores del sistema
Paciente (Usuario final)

Consulta el plan de alimentación diario.

Recibe recordatorios de comidas.

Ve recetas y cantidades exactas.

Genera su lista de compras semanal.

Registra progreso (peso, fotos, métricas).

Nutriólogo

Crea y gestiona pacientes.

Diseña planes de alimentación.

Registra recetas, ingredientes y cantidades.

Asigna planes a cada usuario.

Supervisa progreso del paciente.

(Futuro) Empresas de Meal Prep

Reciben la dieta del paciente.

Preparan y entregan comidas según receta.

⚙️ 2. Tecnologías principales
Frontend

React (con posibilidad de ser PWA)

Manejo de estado opcional: Zustand / Context

Consumo de API vía fetch/axios

Router: React Router

Backend

FastAPI

Validación de tokens Firebase (JWT)

Endpoints REST

Background tasks para recordatorios (en MVP)

Dockerized

Autenticación

Firebase Authentication

Manejo de:

Registro/login

Refresh tokens

Roles: paciente vs. nutriólogo

ID Tokens enviados en cada request

Base de datos

PostgreSQL

Tablas principales:

Usuarios (referenciados por UID de Firebase)

Recetas

Ingredientes

Planes de alimentación

Asignación de planes

Registros de progreso

🧩 3. Módulos principales del sistema
1. User Management (Firebase + Backend)

Firebase almacena usuarios y roles.

Backend valida tokens y crea “perfil” interno en Postgres.

2. Nutrition Content Module

Creación de recetas.

Lista de ingredientes y cantidades.

Agrupación en comidas y días de la semana.

Planes completos de alimentación.

3. Diet Assignment Module

Nutriólogo asigna un plan a un paciente.

Backend registra la relación en la BD.

4. Daily Diet Viewer

Usuario ve qué le toca comer hoy.

Datos vienen del backend según fecha actual.

5. Shopping List Generator

Backend calcula ingredientes totales de la semana.

Frontend exporta la lista a Google Tasks (MVP).

6. Reminders Module

Notifica al usuario qué comida sigue.

MVP: background tasks en FastAPI.

Futuro: un servicio de notificaciones independiente.

7. Progress Tracking

Usuario registra peso, fotos, medidas.

Backend guarda historial.

Nutriólogo ve el progreso.

🔄 4. Flujo de datos (alto nivel)

El usuario abre la app → React.

React solicita login → Firebase.

Firebase devuelve ID Token → React.

React envía ID Token al backend → FastAPI.

FastAPI valida el token y consulta Postgres.

La respuesta vuelve en JSON → React.

React muestra datos, crea interfaz, envía formularios, etc.

🗄️ 5. Infraestructura
Docker Compose

frontend → contenedor React (Vite o CRA)

backend → contenedor FastAPI + Uvicorn

db → contenedor PostgreSQL

Servicios se comunican por red interna Docker.

Deployment (futuro)

Frontend → Vercel / Netlify / Cloudflare

Backend → Render / Railway / Cloud Run

BD → Neon / Supabase / Railway

Firebase Auth → siempre en la nube

🧩 6. Límites del MVP

Para mantener el producto liviano y validable:

No hay meal prep companies todavía.

No hay realtime.

No hay machine learning.

Recordatorios funcionan de forma básica.

No hay dashboards avanzados.

📐 7. Relación con el System Diagram

Todo lo que está explicado aquí se resume visualmente en el System Diagram en mermaid que ya tienes (y que vas a pulir con tus propios módulos).

🎯 Conclusión

System Diagram → Un dibujo.

High Level Architecture → El documento que explica TODO en palabras.

Ya tienes el documento base, David.
Solo falta construir tu diagrama propio con tus decisiones específicas.