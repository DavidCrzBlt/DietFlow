# Architecture overview

This document provides a high-level architecture overview for the DietFlow project. It shows core components (frontend, backend, workers), data stores, and infrastructure components. Use this as a starting point and adjust specific services and names to match the actual implementation.

```mermaid
flowchart LR
  %% Clients
  subgraph Clients
    Web["Web App (JavaScript)"] -->|HTTPS| APIGW["API Gateway / Reverse Proxy"]
    Mobile["Mobile App"] -->|HTTPS| APIGW
  end

  %% Frontend
  subgraph Frontend
    SPA["Single-Page App (JavaScript)"] -->|REST / GraphQL| APIGW
  end

  %% API & Services
  APIGW --> Auth["Auth Service (JWT / OAuth)"]
  APIGW --> API["Backend API (Python)"]
  API --> DB[("Primary DB — Postgres")]
  API --> Cache[("Redis Cache")]
  API --> Storage[("Object Storage — S3")]
  API --> Queue[("Message Broker — RabbitMQ / Redis Streams")]
  Queue --> Worker["Background Workers (Python)"]
  Worker --> DB
  Worker --> Storage

  %% Observability & infra
  API -->|metrics/logs| Observability["Monitoring & Logging (Prometheus / ELK)"]
  APIGW -->|access| Observability

  subgraph Infra
    Docker["Docker / Containers"]
    CI["CI/CD"] -->|build & deploy| Docker
    Docker --- API
    Docker --- Worker
    Docker --- SPA
  end

  %% Notes
  DB -.->|backups| Backup["Backups / Snapshots"]
  Storage -.->|lifecycle| Backup

  classDef infra fill:#f0f8ff,stroke:#333,stroke-width:1px;
  classDef clients fill:#fff2cc,stroke:#333,stroke-width:1px;
  class Clients,Frontend,Infra infra;
  class Web,Mobile,SPA clients;

  %% layout hints
  linkStyle default interpolate basis
```

## Legend
- Web App / Mobile: JavaScript clients (SPA, PWA, or native wrappers)
- API Gateway: reverse proxy or API gateway (NGINX / Traefik)
- Backend API: Python service(s) exposing REST or GraphQL endpoints
- Background Workers: Python processes handling async jobs
- DB / Cache / Storage: typical persistence and caching layers
- Docker: services run in containers; CI/CD builds and deploys images

Adjust component names and technologies to match the repository's actual services and deployment model.