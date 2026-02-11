# Volunteer Connect Web Application Architecture

## System Overview

```mermaid
graph TB
    subgraph "User Interface Layer"
        A[Web Browser]
    end
    
    subgraph "Flask Application"
        B[Application Factory<br/>__init__.py]
        C[Auth Blueprint<br/>auth.py]
        D[Opportunities Blueprint<br/>opportunities.py]
        E[Database Module<br/>db.py]
        F[Import Command<br/>import_opportunities.py]
    end
    
    subgraph "Data Layer"
        G[(SQLite Database)]
        H[CSV Files]
    end
    
    subgraph "Templates"
        I[Base Template]
        J[Auth Templates]
        K[Opportunity Templates]
    end
    
    subgraph "Static Assets"
        L[CSS Styles]
    end
    
    A -->|HTTP Requests| B
    B --> C
    B --> D
    B --> F
    C --> E
    D --> E
    E --> G
    F --> G
    H -->|Import| F
    B --> I
    I --> J
    I --> K
    B --> L
```

## Data Flow

```mermaid
sequenceDiagram
    actor User
    participant Browser
    participant Flask
    participant Auth
    participant Opportunities
    participant Database
    
    User->>Browser: Access webapp
    Browser->>Flask: GET /
    Flask->>Auth: Check session
    Auth->>Database: Load user
    Database-->>Auth: User data
    Auth-->>Flask: User context
    Flask->>Opportunities: Load opportunities
    Opportunities->>Database: Query assigned
    Database-->>Opportunities: Opportunity list
    Opportunities-->>Flask: Render template
    Flask-->>Browser: HTML Response
    Browser-->>User: Display dashboard
```

## Verification Workflow

```mermaid
flowchart TD
    Start([CSV Import]) --> Import[Import Opportunities]
    Import --> Pending[Status: Pending]
    Pending --> Assign[Assign to User]
    Assign --> Review{User Reviews}
    Review -->|Accurate| Verified[Status: Verified]
    Review -->|Inaccurate| Rejected[Status: Rejected]
    Review -->|Uncertain| NeedsReview[Status: Needs Review]
    NeedsReview --> SecondReview{Second Review}
    SecondReview -->|Accurate| Verified
    SecondReview -->|Inaccurate| Rejected
    Verified --> AuditLog[Log to Verifications Table]
    Rejected --> AuditLog
    AuditLog --> End([Complete])
```

## Database Schema

```mermaid
erDiagram
    USER ||--o{ OPPORTUNITY : assigns
    USER ||--o{ VERIFICATION : performs
    OPPORTUNITY ||--o{ VERIFICATION : has
    
    USER {
        int id PK
        string username UK
        string password
        string role
        timestamp created_at
    }
    
    OPPORTUNITY {
        int id PK
        string organization_name
        string volunteer_title
        string url
        string image
        string position_date
        text description
        string age_requirement
        string skill_requirement
        string address_virtual
        string passion_areas
        string specific_skills
        string filters
        int assigned_user_id FK
        string verification_status
        timestamp created_at
    }
    
    VERIFICATION {
        int id PK
        int opportunity_id FK
        int user_id FK
        string status
        text notes
        timestamp verified_at
    }
```

## Component Interaction

```mermaid
graph LR
    subgraph "Request Handling"
        A[HTTP Request] --> B{Route}
        B -->|/auth/*| C[Auth Blueprint]
        B -->|/| D[Opportunities Blueprint]
        B -->|/*| D
    end
    
    subgraph "Authentication"
        C --> E[Check Credentials]
        E --> F[Session Management]
        F --> G{Valid?}
        G -->|Yes| H[Set g.user]
        G -->|No| I[Redirect to Login]
    end
    
    subgraph "Authorization"
        H --> J{@login_required}
        J -->|Authorized| K[Process Request]
        J -->|Unauthorized| I
    end
    
    subgraph "Data Access"
        K --> L[get_db]
        L --> M[Execute Query]
        M --> N[Return Results]
    end
    
    subgraph "Response"
        N --> O[Render Template]
        O --> P[HTTP Response]
    end
```

## File Structure

```
volunteerconnectco-webscraper/
├── webapp/                          # Main application directory
│   ├── __init__.py                 # Application factory
│   ├── auth.py                     # Authentication blueprint
│   ├── db.py                       # Database utilities
│   ├── opportunities.py            # Opportunities blueprint
│   ├── import_opportunities.py     # CSV import CLI command
│   ├── schema.sql                  # Database schema
│   ├── requirements.txt            # Python dependencies
│   ├── README.md                   # Technical documentation
│   ├── .env.example               # Configuration template
│   ├── .gitignore                 # Git ignore rules
│   ├── static/
│   │   └── style.css              # Application styles (700+ lines)
│   └── templates/
│       ├── base.html              # Base template with navigation
│       ├── auth/
│       │   ├── login.html        # Login page
│       │   └── register.html     # Registration page
│       └── opportunities/
│           ├── index.html        # User dashboard
│           ├── all.html          # All opportunities list
│           ├── detail.html       # Opportunity detail view
│           ├── verify.html       # Verification form
│           └── stats.html        # Statistics dashboard
├── run_webapp.sh                   # Automated startup script
├── QUICKSTART.md                   # User guide
├── WEBAPP_SUMMARY.md               # Implementation summary
├── ARCHITECTURE.md                 # This file
└── volunteer_output.csv            # Sample data for import
```

## Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **Database**: SQLite (embedded database)
- **Security**: Werkzeug (password hashing, security utilities)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with CSS Variables
- **Templates**: Jinja2 (Flask's template engine)

## Security Architecture

```mermaid
graph TD
    A[User Input] --> B{Input Validation}
    B -->|Valid| C[Parameterized Queries]
    B -->|Invalid| D[Error Message]
    C --> E[Database]
    
    F[Password] --> G[Werkzeug Hash]
    G --> H[Hashed Password]
    H --> E
    
    I[Session] --> J[Flask Session]
    J --> K[Signed Cookie]
    K --> L[Client Browser]
    
    M[Login Check] --> N{Session Valid?}
    N -->|Yes| O[Access Granted]
    N -->|No| P[Redirect to Login]
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        A[Flask Dev Server<br/>Port 5000]
        B[SQLite Database<br/>instance/flaskr.sqlite]
    end
    
    subgraph "Production Option 1: Simple"
        C[Gunicorn<br/>WSGI Server]
        D[SQLite Database<br/>/var/db/volunteer.sqlite]
        E[Nginx<br/>Reverse Proxy]
    end
    
    subgraph "Production Option 2: Scalable"
        F[Gunicorn Workers<br/>Multiple Processes]
        G[PostgreSQL<br/>Database Server]
        H[Nginx + SSL<br/>Load Balancer]
    end
    
    A --> B
    C --> D
    E --> C
    F --> G
    H --> F
```

## Key Design Decisions

### 1. Application Factory Pattern
- Allows multiple instances with different configs
- Facilitates testing
- Enables blueprint registration

### 2. Blueprint Architecture
- Separates concerns (auth vs. opportunities)
- Makes code more maintainable
- Enables modular development

### 3. SQLite Database
- Zero configuration
- Perfect for small-to-medium deployments
- Easy backup (single file)
- Can upgrade to PostgreSQL if needed

### 4. Status-Based Workflow
- Clear state transitions
- Audit trail via verifications table
- Flexible for future status additions

### 5. Server-Side Rendering
- Better SEO
- Faster initial load
- Progressive enhancement
- No complex build process

## Performance Characteristics

- **Database Queries**: Optimized with proper indexing on foreign keys
- **Page Load**: Fast with minimal external dependencies
- **Scalability**: Can handle 100s of concurrent users with proper deployment
- **Storage**: ~1-2KB per opportunity record

## Extension Points

The architecture supports easy extension for:

1. **API Layer**: Add RESTful API blueprint
2. **Admin Interface**: Create admin blueprint with permissions
3. **Email System**: Integrate Flask-Mail
4. **File Uploads**: Add file handling for opportunity images
5. **Search**: Integrate full-text search
6. **Caching**: Add Redis for session/data caching
7. **Background Jobs**: Integrate Celery for async tasks

## Monitoring & Logging

Recommended additions for production:

```mermaid
graph LR
    A[Application] --> B[Python Logging]
    B --> C[Log Files]
    B --> D[Syslog]
    B --> E[Error Tracking<br/>Sentry]
    A --> F[Metrics Collection]
    F --> G[Prometheus]
    G --> H[Grafana Dashboard]
```

## Backup Strategy

```mermaid
graph TD
    A[SQLite Database] -->|Daily| B[Automated Backup]
    B --> C[Compressed Archive]
    C --> D[Remote Storage]
    A -->|Before Updates| E[Manual Backup]
    E --> F[Version Control]
```

---

This architecture provides a solid foundation for a production-ready volunteer opportunity verification system while maintaining simplicity and ease of deployment.
