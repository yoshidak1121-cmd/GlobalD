# Global Dolphin 🐬

A machine-centric management system prototype built with FastAPI, SQLite, and plain HTML/CSS/JS.

## Features

- **Machine-Centric UI**: All data is organized around machines
- **Free-Text Search**: Search across Machine, NC, Contract, Sales, Dealer, Ship, Install, End User, and Service Base data
- **Detailed Machine View**: Fixed machine header with tabs for different data sections
- **RESTful APIs**: Complete CRUD operations for machine data
- **Data Validation**: 
  - Date format: YYYY/MM/DD
  - Memo fields: max 300 characters
  - Country fields: full country names required

## Architecture

- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Frontend**: Plain HTML/CSS/JavaScript (no frameworks)

## Database Schema

The system manages the following entities:
- Machine (base information)
- NC (Numerical Control)
- Contract
- Sales
- Dealer
- Ship
- Install
- End User
- Service Base

## API Endpoints

### Search
- `GET /api/search?q=<query>` - Free-text search across all machine data

### Machine Operations
- `GET /api/machines/{id}` - Get detailed machine information
- `POST /api/machines` - Create a new machine
- `PUT /api/machines/{id}` - Update an existing machine

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yoshidak1121-cmd/GlobalD.git
cd GlobalD
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the server:
```bash
python main.py
```

Alternatively, you can use uvicorn directly:
```bash
uvicorn main:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

The application will:
- Initialize the SQLite database (`globald.db`) on first run
- Seed the database with 3 sample machines
- Serve the search page at the root URL
- Provide machine detail pages at `/detail/{machine_id}`

### Sample Data

The application comes pre-seeded with 3 sample machines:
- M-2024-001 (DMU 50)
- M-2024-002 (NHX 5000)
- M-2024-003 (DMC 80 U)

## Usage

### Search Page

1. Enter search terms in the search box (searches across all fields)
2. Press Enter or click "Search"
3. Click on any machine number to view details

### Detail Page

1. View fixed machine header with key information
2. Switch between tabs to see different data sections:
   - Machine: Basic machine information
   - NC: Numerical control data
   - Contract: Contract details
   - Sales: Sales information
   - Dealer: Dealer information
   - Ship: Shipping details
   - Install: Installation information
   - End User: End user company details
   - Service Base: Service center information

## Data Validation

The API enforces the following validation rules:

### Date Fields
- Format: `YYYY/MM/DD`
- Example: `2024/01/15`

### Memo Fields
- Maximum length: 300 characters

### Country Fields
- Must be full country names (e.g., "Japan", "United States")
- No abbreviations or codes

## API Usage Examples

### Search for machines
```bash
curl "http://localhost:8000/api/search?q=FANUC"
```

### Get machine details
```bash
curl "http://localhost:8000/api/machines/1"
```

### Create a new machine
```bash
curl -X POST "http://localhost:8000/api/machines" \
  -H "Content-Type: application/json" \
  -d '{
    "machine": {
      "machine_no": "M-2024-004",
      "model": "DMU 70",
      "serial_no": "SN004567"
    },
    "nc": {
      "nc_maker": "FANUC",
      "nc_model": "31i-B5",
      "nc_serial": "NC004"
    }
  }'
```

### Update a machine
```bash
curl -X PUT "http://localhost:8000/api/machines/1" \
  -H "Content-Type: application/json" \
  -d '{
    "machine": {
      "machine_no": "M-2024-001",
      "model": "DMU 50 Updated",
      "serial_no": "SN001234"
    }
  }'
```

## Development Notes

- The database file `globald.db` is created automatically on first run
- To reset the database, simply delete `globald.db` and restart the application
- All date fields accept the format YYYY/MM/DD
- Japanese field names and data are supported throughout the system

## License

MIT