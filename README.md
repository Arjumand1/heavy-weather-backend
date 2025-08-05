# Heavy Weather Backend

A TodoMVC application backend built with Python Flask and the rococo framework.

## Features

- **Complete TodoMVC Backend API** - Full CRUD operations for tasks
- **User Authentication** - Signup, login, logout, password reset
- **Email Integration** - Mailjet-powered email verification and password reset
- **User Profile Management** - Edit user first/last name
- **Task Management** - Add, edit, complete, delete tasks with descriptions
- **Advanced Filtering** - Filter by completed/active status
- **Docker Containerized** - PostgreSQL, RabbitMQ, Flask API, Email service

## Tech Stack

- **Framework:** Python Flask + rococo framework
- **Database:** PostgreSQL with migrations
- **Queue:** RabbitMQ for email processing
- **Email:** Mailjet integration
- **Authentication:** JWT-based auth system
- **Containerization:** Docker & Docker Compose

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone and Setup
```bash
git clone https://github.com/Arjumand1/heavy-weather-backend.git
cd heavy-weather-backend
```

### 2. Configure Environment
Copy and configure your environment files:
```bash
cp .env.secrets.example .env.secrets
# Edit .env.secrets with your actual Mailjet credentials
```

### 3. Launch Backend
```bash
./run.sh
```

The backend will be available at: `http://localhost:5000`
- API Documentation: `http://localhost:5000/api-doc`

## API Endpoints

### Authentication
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login  
- `POST /auth/logout` - User logout
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password/{token}/{uidb64}` - Reset password

### User Profile
- `GET /person/me` - Get current user profile
- `PUT /person/me` - Update user profile

### Tasks
- `GET /tasks` - Get all user tasks (with optional `completed` filter)
- `POST /tasks` - Create new task
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Environment Variables

### Required in `.env.secrets`:
- `POSTGRES_PASSWORD` - Database password
- `RABBITMQ_PASSWORD` - Message queue password  
- `SECRET_KEY` - Flask secret key
- `SECURITY_PASSWORD_SALT` - Password hashing salt
- `AUTH_JWT_SECRET` - JWT signing secret
- `MAILJET_API_KEY` - Mailjet API key
- `MAILJET_API_SECRET` - Mailjet API secret

### Pre-configured in `local.env`:
- Database connection settings
- RabbitMQ configuration
- Email provider settings
- Token expiration times

## Architecture

Built using the rococo framework patterns:
- **Models** - VersionedModel with audit trails
- **Repositories** - Data access layer with factory pattern  
- **Services** - Business logic layer
- **Views** - Flask-RESTX API endpoints
- **Migrations** - Database schema versioning

## Database Schema

- **Person** - User profiles
- **Email** - User email addresses  
- **LoginMethod** - Authentication credentials
- **Task** - Todo items with descriptions
- **Organization** - User organizations
- **PersonOrganizationRole** - User-organization relationships

All tables include audit fields (entity_id, version, active, changed_by, changed_on).

## Development

### Running Migrations
Migrations run automatically on startup. Manual migration:
```bash
docker-compose exec api python -m flask db upgrade
```

### Viewing Logs
```bash
docker-compose logs api --tail=50
```

### Debugging
Set `FLASK_DEBUG=true` in `local.env` for detailed error messages.

## Email Templates

Uses Mailjet templates:
- **Verify Email** (Template ID: 6410451) - Account verification
- **Reset Password** (Template ID: 6410454) - Password reset

## Production Deployment

1. Update environment variables for production
2. Configure proper CORS origins
3. Set up SSL/TLS certificates
4. Use production-grade database
5. Configure monitoring and logging

## Contributing

This is a TodoMVC demonstration project. For questions or issues, please contact the development team.

## License

This project is built as a demonstration of the rococo framework capabilities.
