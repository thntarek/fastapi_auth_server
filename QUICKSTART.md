# 🚀 Quick Start Guide

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Create PostgreSQL Database

```sql
CREATE DATABASE auth_server_db;
```

## 3. Create .env File

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Generate a secure SECRET_KEY:

```bash
openssl rand -hex 32
```

## 4. Run the Application

```bash
uvicorn auth_server.main:app --reload
```

## 5. Test the API

### Register a User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username_or_email": "johndoe",
    "password": "SecurePass123!"
  }'
```

Copy the `access_token` from the response.

### Access Protected Route

```bash
curl -X GET http://localhost:8000/user/home \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 6. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
fastapi_auth_server/
├── auth_server/
│   ├── database/
│   │   ├── db_config.py          # Production-ready database config
│   │   └── __init__.py
│   ├── router/
│   │   ├── auth.py                # Register & Login endpoints
│   │   ├── user.py                # Protected home endpoint
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main.py                    # FastAPI application
│   ├── models.py                  # User database model
│   ├── schemas.py                 # Pydantic validation schemas
│   └── security.py                # JWT & password hashing
├── .env                           # Your environment variables
├── .env.example                   # Example environment file
├── requirements.txt               # Python dependencies
└── README.md                      # Full documentation
```

## API Endpoints

| Method | Endpoint       | Description       | Auth Required |
| ------ | -------------- | ----------------- | ------------- |
| GET    | /              | Root endpoint     | No            |
| GET    | /health        | Health check      | No            |
| POST   | /auth/register | Register new user | No            |
| POST   | /auth/login    | Login user        | No            |
| GET    | /user/home     | Get user info     | Yes (JWT)     |

## Production Deployment Checklist

- [ ] Generate strong SECRET_KEY
- [ ] Update database credentials
- [ ] Set SQL_ECHO=false
- [ ] Configure CORS origins (not \*)
- [ ] Use HTTPS
- [ ] Set up SSL for database connection
- [ ] Configure proper pool sizes
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Use environment variables (never hardcode secrets)

## Troubleshooting

### Database Connection Error

- Check PostgreSQL is running
- Verify credentials in .env
- Ensure database exists

### JWT Token Error

- Ensure SECRET_KEY is set
- Check token hasn't expired
- Verify Authorization header format: `Bearer <token>`

### Import Errors

- Ensure all __init__.py files exist
- Check Python path includes project root
- Verify requirements are installed

## Support

For issues, check the full README.md for detailed documentation.
