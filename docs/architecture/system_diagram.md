```mermaid
flowchart LR

    subgraph UserSide[Usuario / Cliente]
        U["User (Web/Móvil)"]
    end

    subgraph Frontend[React App]
        FE[React Components<br>Auth Flow<br>API Calls]
    end

    subgraph Firebase[Firebase Auth]
        FB[ID Token<br>User Management]
    end

    subgraph Backend[FastAPI Backend]
        API[FastAPI Services<br>Business Logic<br>Validation]
    end

    subgraph Database[PostgreSQL]
        DB[(PostgreSQL<br>Tables)]
    end

    U --> FE

    FE -->|Login / Signup| FB
    FB -->|ID Token| FE

    FE -->|"Authenticated Requests<br>(Authorization: Bearer <token>)"| API
    API -->|Queries| DB
    DB -->|Results| API
    API -->|JSON Response| FE
