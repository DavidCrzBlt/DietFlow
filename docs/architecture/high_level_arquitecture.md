```mermaid
---
title: Arquitectura de la solución
---

flowchart TD

%% ---- Devices ----
UserPhone["Smartphone<br>(Web App / PWA)"]
LaptopUser[Laptop/PC]

%% ---- Frontend ----
subgraph Frontend["React Frontend (Web + Mobile Web)"]
    FE1[Nutriólogo Dashboard]
    FE2[Paciente UI]
    FE3["PWA Layer<br>(Offline Cache, Icono, etc.)"]
end

%% ---- Firebase ----
subgraph Firebase["Firebase Services"]
    FB1["Firebase Auth<br>(Email, Google, etc.)"]
end

%% ---- Backend ----
subgraph Backend["FastAPI Backend"]
    BE1["Auth Middleware<br>(Valida token de Firebase)"]
    BE2["User Manager<br>(Pacientes/Nutriólogos)"]
    BE3[Plan Builder]
    BE4[Recipe Manager]
    BE5[Meal Scheduler]
    BE6[Shopping List Engine]
    BE7["Notification Worker<br>(FCM + Crons)"]
end

%% ---- Infra ----
subgraph Infra["Dockerized Services"]
    DockerFE[Frontend Container]
    DockerBE[Backend Container]
    DockerDB[PostgreSQL Container]
end

%% ---- Database ----
subgraph Database["PostgreSQL"]
    DB1[(Usuarios)]
    DB2[(Nutriólogos)]
    DB3[(Pacientes)]
    DB5[(Planes)]
    DB6[(Recetas)]
    DB7[(Ingredientes)]
    DB8[(Comidas asignadas)]
    DB9[(Progreso)]
end

%% Connections
UserPhone --> FE1
UserPhone --> FE2
LaptopUser --> FE1

FE1 --> FB1
FE2 --> FB1

FB1 --> BE1

FE1 --> Backend
FE2 --> Backend

Backend --> DockerDB
DockerDB --> Database

Frontend --> DockerFE
Backend --> DockerBE
