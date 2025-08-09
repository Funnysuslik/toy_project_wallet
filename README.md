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
