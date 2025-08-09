# Toy Project Wallet

A FastAPI-based wallet application with a clean architecture.

## Setup

1. **Clone the repository and navigate to the project directory**
   ```bash
   cd toy_project_wallet
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp backend/env.example backend/.env
   
   # Edit the .env file with your actual database credentials
   nano backend/.env
   ```

## Running the Application

### Development Mode
```bash
# Method 1: Using the development runner script
python3 run_dev.py

# Method 2: Direct execution
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the application is running, you can access:

- **API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/

## Project Structure

```
toy_project_wallet/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── users.py
│   │   │       ├── wallets.py
│   │   │       └── transactions.py
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   └── settings.py
│   │   ├── models/
│   │   │   ├── users.py
│   │   │   ├── wallets.py
│   │   │   └── transactions.py
│   │   └── main.py
│   ├── .env
│   └── env.example
├── requirements.txt
├── run_dev.py
└── README.md
```

## Environment Variables

The application requires the following environment variables in `backend/.env`:

```env
# Database settings
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=wallet_db

# API settings
API_V1_STR=/api/v1

# Frontend settings
FRONTEND_HOST=http://localhost:5173
```

## Development

The application uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **Pydantic Settings** for configuration management
- **Uvicorn** as the ASGI server

The application is set up with hot reload for development, so any changes to the code will automatically restart the server.
