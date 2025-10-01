# Task Management System (TMS) - Backend

A RESTful API for a task management system built with FastAPI and PostgreSQL, featuring role-based access control, JWT authentication, and comprehensive task management capabilities.

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0.23
- **Migration**: Alembic 1.13.1
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Bcrypt
- **Server**: Uvicorn

## Features

- User authentication with JWT tokens
- Role-based access control (Admin/User roles)
- Task creation, update, and deletion
- Task assignment to users
- Pagination and filtering for tasks and users
- Soft delete for tasks
- Search functionality
- RESTful API design

## Project Structure

```
TMS_be/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py          # Authentication endpoints
│   │       ├── users.py         # User management endpoints
│   │       └── tasks.py         # Task management endpoints
│   ├── core/
│   │   ├── config.py           # Configuration settings
│   │   └── security.py         # Security utilities (hashing, JWT)
│   ├── db/
│   │   └── database.py         # Database connection setup
│   ├── models/
│   │   ├── user.py             # User model
│   │   └── task.py             # Task model
│   ├── schemas/
│   │   ├── auth.py             # Auth schemas (Token)
│   │   ├── user.py             # User schemas (Request/Response)
│   │   └── task.py             # Task schemas (Request/Response)
│   └── main.py                 # FastAPI application entry point
├── alembic/                    # Database migration files
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md
```

## Database Models

### User Model
- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `username` (String, Unique)
- `hashed_password` (String)
- `full_name` (String)
- `is_active` (Boolean, default: True)
- `is_admin` (Boolean, default: False)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Task Model
- `id` (UUID, Primary Key)
- `title` (String)
- `description` (String)
- `status` (Enum: pending, in_progress, completed, cancelled)
- `priority` (Enum: low, medium, high, urgent)
- `assignee_id` (UUID, Foreign Key to User)
- `created_by` (UUID, Foreign Key to User)
- `is_active` (Boolean, default: True)
- `due_date` (DateTime, nullable)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## API Routes

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | Login and get access token | No |

**Login Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Login Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user_id": "uuid",
  "username": "string",
  "is_admin": boolean
}
```

### Users (`/api/v1/users`)

| Method | Endpoint | Description | Auth Required | Admin Only |
|--------|----------|-------------|---------------|------------|
| POST | `/admin` | Create first admin user | No | No |
| POST | `/` | Create new user | Yes | Yes |
| GET | `/` | List users with pagination & search | Yes | No |
| GET | `/me` | Get current user info | Yes | No |
| GET | `/{user_id}` | Get user by ID | Yes | No |
| PUT | `/{user_id}` | Update user | Yes | Partial* |

*Users can update their own profile; only admins can update other users.

**Create Admin Request:**
```json
{
  "email": "admin@example.com",
  "username": "admin",
  "password": "password",
  "full_name": "Admin User"
}
```

**Create User Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password",
  "full_name": "Full Name",
  "is_active": true
}
```

**List Users Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 10, max: 100): Number of records to return
- `search` (string, optional): Search by username, email, or full name

### Tasks (`/api/v1/tasks`)

| Method | Endpoint | Description | Auth Required | Admin Only |
|--------|----------|-------------|---------------|------------|
| POST | `/` | Create new task | Yes | No |
| GET | `/` | List tasks with filters & pagination | Yes | No |
| GET | `/my/tasks` | Get current user's assigned tasks | Yes | No |
| GET | `/{task_id}` | Get task by ID | Yes | No |
| PUT | `/{task_id}` | Update task | Yes | Partial* |
| DELETE | `/{task_id}` | Delete task (soft delete) | Yes | Partial** |

*Task creators, assignees, and admins can update tasks.
**Only task creators and admins can delete tasks.

**Create Task Request:**
```json
{
  "title": "Task title",
  "description": "Task description",
  "status": "pending",
  "priority": "medium",
  "assignee_id": "uuid (optional)",
  "due_date": "2024-12-31T23:59:59Z (optional)"
}
```

**List Tasks Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 10, max: 100): Number of records to return
- `status` (enum, optional): Filter by status (pending, in_progress, completed, cancelled)
- `priority` (enum, optional): Filter by priority (low, medium, high, urgent)
- `assignee_id` (UUID, optional): Filter by assignee
- `search` (string, optional): Search by title or description

**Note:** Non-admin users can only see tasks they created or are assigned to.

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API welcome message | No |
| GET | `/health` | Health check endpoint | No |

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 15

### Installation & Setup

1. **Clone the repository:**
   ```bash
   cd /path/to/TMS_be
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**

   Install PostgreSQL 15 if not already installed:
   ```bash
   # macOS (using Homebrew)
   brew install postgresql@15
   brew services start postgresql@15

   # Ubuntu/Debian
   sudo apt-get install postgresql-15
   sudo systemctl start postgresql

   # Windows
   # Download and install from https://www.postgresql.org/download/windows/
   ```

5. **Create database:**
   ```bash
   # Access PostgreSQL
   psql postgres

   # Create database and user
   CREATE DATABASE tms_db;
   CREATE USER your_db_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE tms_db TO your_db_user;
   \q
   ```

6. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and update the values:
   ```env
   DB_USER=your_db_user
   DB_PASS=your_secure_password
   DB_ENV=localhost
   DB_NAME=tms_db

   SECRET_KEY=your-secret-key-here-generate-a-secure-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

7. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

8. **Start the server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

9. **Create the first admin user:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/users/admin" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "username": "admin",
       "password": "admin123",
       "full_name": "Admin User"
     }'
   ```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Authentication Flow

1. Create an admin user using `POST /api/v1/users/admin` (only works once)
2. Login using `POST /api/v1/auth/login` to get an access token
3. Include the token in subsequent requests:
   ```
   Authorization: Bearer <your_access_token>
   ```

## Example Usage

### 1. Create Admin User
```bash
curl -X POST "http://localhost:8000/api/v1/users/admin" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "admin123",
    "full_name": "Admin User"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

### 3. Create a Task
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README",
    "status": "pending",
    "priority": "high"
  }'
```

### 4. List Tasks
```bash
curl -X GET "http://localhost:8000/api/v1/tasks/?skip=0&limit=10" \
  -H "Authorization: Bearer <your_token>"
```

## Role-Based Access Control

### Admin Users Can:
- Create new users
- View all tasks
- Update any task
- Delete any task
- Update any user profile

### Regular Users Can:
- View tasks they created or are assigned to
- Create new tasks
- Update tasks they created or are assigned to
- Delete tasks they created
- Update their own profile
- View other users' profiles

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## Testing

The project includes `pytest` and `httpx` for testing. Run tests with:
```bash
pytest
```

## Stopping the Application

Press `Ctrl+C` in the terminal running uvicorn

To stop PostgreSQL:
```bash
# macOS
brew services stop postgresql@15

# Ubuntu/Debian
sudo systemctl stop postgresql
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DB_USER | Database username | - |
| DB_PASS | Database password | - |
| DB_ENV | Database host | localhost |
| DB_NAME | Database name | - |
| SECRET_KEY | JWT secret key | - |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time | 30 |

## Requirements

Key dependencies:
- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- sqlalchemy==2.0.23
- psycopg2-binary==2.9.9
- alembic==1.13.1
- python-jose[cryptography]==3.3.0
- passlib[bcrypt]==1.7.4
- pydantic==2.5.2
- python-dotenv==1.0.0

## License

This project is for assignment purposes.

## Support

For issues or questions, please create an issue in the repository.
