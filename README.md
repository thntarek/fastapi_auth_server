# auth_server fastapi Application

Production-ready FastAPI application with JWT authentication and PostgreSQL database.

## Features

- ✅ JWT Authentication
- ✅ User Registration & Login
- ✅ Protected Routes
- ✅ PostgreSQL with AsyncPG
- ✅ SQLAlchemy ORM
- ✅ Password Hashing (bcrypt)
- ✅ Input Validation with Pydantic
- ✅ Production-optimized Database Connection Pool
- ✅ CORS Middleware
- ✅ Auto-generated API Documentation

## Project Structure

```
web_eng/
├── auth_server/
│   ├── database/
│   │   ├── db_config.py      # Database configuration
│   │   └── __init__.py
│   ├── router/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── user.py            # User endpoints
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main.py                # FastAPI application
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   └── security.py            # JWT and password utilities
├── .env                       # Environment variables
└── requirements.txt           # Python dependencies
```

## Installation

### 1. Clone and Setup

```bash
cd fastapi_auth_server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. PostgreSQL Setup

```sql
CREATE DATABASE auth_server_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE auth_server_db TO your_user;
```

### 3. Environment Variables

Create `.env` file in the root directory:

```env
# Database
PG_DB_NAME=auth_server_db
PG_DB_USER=postgres
PG_DB_PASSWD=your_password_here
PG_DB_HOST=localhost
PG_DB_PORT=5432
SQL_ECHO=false

# Database Pool
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600

# JWT (Generate with: openssl rand -hex 32)
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Application

```bash
uvicorn auth_server.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

#### Register User

```http
POST /auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

**Response:**

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "is_active": true,
    "created_at": "2024-02-15T10:30:00",
    "updated_at": "2024-02-15T10:30:00"
}
```

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "username_or_email": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### Protected Routes

#### Get User Info (Home)

```http
GET /user/home
Authorization: Bearer <your_access_token>
```

**Response:**

```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890",
    "is_active": true,
    "created_at": "2024-02-15T10:30:00",
    "updated_at": "2024-02-15T10:30:00"
}
```

## Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&\*(),.?":{}|<>)

## API Documentation

Once running, access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Production Deployment

### Environment Variables

- Set strong `SECRET_KEY` (use `openssl rand -hex 32`)
- Configure proper CORS origins in `main.py`
- Set `SQL_ECHO=false`
- Use environment-specific database credentials

### Security Recommendations

- Use HTTPS in production
- Set proper CORS origins (not \*)
- Use strong passwords for database
- Rotate JWT secret keys periodically
- Implement rate limiting
- Enable database SSL connections

### Performance Tuning

Adjust in `.env`:

```env
DB_POOL_SIZE=50
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=3600
```

### Run with Gunicorn (Production)

```bash
gunicorn auth_server.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Testing with cURL

### Register

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test123!@#",
    "first_name": "Test",
    "last_name": "User",
    "phone_number": "1234567890"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "testuser",
    "password": "Test123!@#"
  }'
```

### Access Protected Route

```bash
curl -X GET http://localhost:8000/user/home \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
