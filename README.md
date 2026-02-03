# GlobalD

A FastAPI application for searching and managing machine-centric data.

## Features

- Free-text search across machine data
- SQLite database backend
- RESTful API with FastAPI
- Input sanitization for security

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Populate database with sample data:
```bash
python populate_db.py
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Search Machines
**GET** `/api/search?q=<query>`

Search across machine fields including:
- Machine Model
- Machine Serial
- Maker
- NC Model
- Contract Number
- End User
- Install Country
- Service Base

#### Example Requests

Search by maker:
```bash
curl "http://localhost:8000/api/search?q=Makino"
```

Search by country:
```bash
curl "http://localhost:8000/api/search?q=Japan"
```

Search by serial number:
```bash
curl "http://localhost:8000/api/search?q=SN-2023-001"
```

Search by end user:
```bash
curl "http://localhost:8000/api/search?q=Toyota"
```

Search by contract number:
```bash
curl "http://localhost:8000/api/search?q=CT-2023"
```

#### Example Response
```json
[
  {
    "id": 1,
    "machine_model": "CNC-1000X",
    "machine_serial": "SN-2023-001",
    "maker": "Makino",
    "nc_model": "FANUC 31i-B5",
    "contract_number": "CT-2023-0045",
    "end_user": "Toyota Manufacturing",
    "install_country": "Japan",
    "service_base": "Tokyo Service Center"
  }
]
```

### Root Endpoint
**GET** `/`

Returns API information and available endpoints.

```bash
curl "http://localhost:8000/"
```

### Health Check
**GET** `/health`

Health check endpoint.

```bash
curl "http://localhost:8000/health"
```

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Security

The search endpoint includes:
- Input sanitization to remove potentially dangerous characters
- Query length limitation (max 100 characters)
- SQL injection protection via SQLAlchemy parameterized queries
- LIKE-based search with escaped wildcards