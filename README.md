# Toy Project Wallet

A FastAPI-based wallet application with a clean architecture.

## Board with ideas and tasks

https://miro.com/app/board/uXjVJS5d2Hw=/?share_link_id=190555757928

## Setup

   In case to start whole project you need to:
   1. Clone it
   2. Setup .env
   3. Go to infra dir
   4. Run docker-compose up --build

## Running the Application

### Backend Development Mode
!!! You need to start Postgres server first

```bash
# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
alembic upgrate head
```

## API Documentation

Once the application is running, you can access:

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/
