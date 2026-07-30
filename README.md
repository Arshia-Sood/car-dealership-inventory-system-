# 🚗 Car Dealership Inventory System

A full-stack Car Dealership Inventory Management System built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. The application provides secure user authentication and inventory management for vehicles.

## Features

- User Registration & Login
- JWT Authentication
- Role-based User Management (User/Admin)
- Vehicle Inventory Management
- Search Vehicles
- Purchase Vehicles
- Restock Inventory
- Update Vehicle Details
- Delete Vehicles
- PostgreSQL Database
- Alembic Database Migrations
- Interactive Swagger API Documentation

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Passlib (Password Hashing)
- Python-Jose (JWT Authentication)
- Uvicorn

### Database
- PostgreSQL

---

## Project Structure

```
backend/
│
├── alembic/
│   └── versions/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── crud/
│   ├── models/
│   ├── schemas/
│   └── services/
│
├── .env
├── requirements.txt
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## PostgreSQL Setup

Create a PostgreSQL database.

Example:

```text
Database Name : car_dealership
Username      : postgres
Password      : your_password
```

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/car_dealership

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Database Migration

Run migrations using Alembic.

```bash
alembic upgrade head
```

---

## Run the Server

```bash
uvicorn app.main:app --reload
```

Server runs on

```
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

OpenAPI

```
http://127.0.0.1:8000/openapi.json
```

---

## Available Endpoints

### Authentication

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register` | Register User |
| POST | `/api/auth/login` | Login |

### Vehicles

| Method | Endpoint |
|---------|----------|
| GET | `/api/vehicles` |
| POST | `/api/vehicles` |
| GET | `/api/vehicles/search` |
| PUT | `/api/vehicles/{vehicle_id}` |
| DELETE | `/api/vehicles/{vehicle_id}` |
| POST | `/api/vehicles/{vehicle_id}/purchase` |
| POST | `/api/vehicles/{vehicle_id}/restock` |

---

## Authentication

The project uses JWT Authentication.

1. Register a user.
2. Login to obtain an access token.
3. Click **Authorize** in Swagger.
4. Enter

```
Bearer <your_access_token>
```

5. Access protected endpoints.

---

## Database

The project uses PostgreSQL with Alembic migrations.

Main Tables:

- users
- vehicles
- alembic_version

---

## Future Improvements

- Image upload for vehicles
- Pagination
- Filtering and sorting
- Dashboard analytics
- Docker support
- Unit testing
- CI/CD pipeline

---

## Author

**Arshia Sood**

B.Tech Computer Science Engineering