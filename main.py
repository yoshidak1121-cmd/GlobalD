from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from typing import Optional
import sqlite3
import re
from datetime import datetime
app = FastAPI(title="Global Dolphin")

# Database initialization
DB_PATH = "globald.db"

def init_db():
    """Initialize database with schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Machine table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_no TEXT UNIQUE NOT NULL,
            model TEXT,
            serial_no TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    # NC (Numerical Control) table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            nc_maker TEXT,
            nc_model TEXT,
            nc_serial TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Contract table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            contract_no TEXT,
            contract_date TEXT,
            contract_type TEXT,
            memo TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            sales_date TEXT,
            sales_person TEXT,
            sales_amount REAL,
            memo TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Dealer table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dealers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            dealer_name TEXT,
            dealer_country TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Ship table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            ship_date TEXT,
            ship_method TEXT,
            tracking_no TEXT,
            destination TEXT,
            memo TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Install table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS installs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            install_date TEXT,
            installer TEXT,
            location TEXT,
            memo TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # End User table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS end_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            company_name TEXT,
            country TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    # Service Base table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_bases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id INTEGER,
            base_name TEXT,
            country TEXT,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            FOREIGN KEY (machine_id) REFERENCES machines(id)
        )
    """)
    
    conn.commit()
    conn.close()

def seed_data():
    """Seed database with 3 sample machines"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM machines")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Sample data for 3 machines
    machines_data = [
        {
            "machine_no": "M-2024-001",
            "model": "DMU 50",
            "serial_no": "SN001234",
            "nc": {"nc_maker": "FANUC", "nc_model": "31i-B5", "nc_serial": "NC001"},
            "contract": {"contract_no": "C-2024-001", "contract_date": "2024/01/15", "contract_type": "新規", "memo": "標準契約"},
            "sales": {"sales_date": "2024/01/10", "sales_person": "田中太郎", "sales_amount": 15000000, "memo": "初回取引"},
            "dealer": {"dealer_name": "Tokyo Machine Sales", "dealer_country": "Japan", "contact_person": "佐藤次郎", "phone": "03-1234-5678", "email": "sato@tokyo-machine.jp"},
            "ship": {"ship_date": "2024/02/01", "ship_method": "海上輸送", "tracking_no": "TRK001", "destination": "東京港", "memo": "通常配送"},
            "install": {"install_date": "2024/02/15", "installer": "山田設置", "location": "東京工場A棟", "memo": "設置完了"},
            "end_user": {"company_name": "ABC製造株式会社", "country": "Japan", "contact_person": "鈴木一郎", "phone": "03-9876-5432", "email": "suzuki@abc-mfg.jp", "address": "東京都千代田区1-1-1"},
            "service_base": {"base_name": "東京サービスセンター", "country": "Japan", "contact_person": "高橋サービス", "phone": "03-5555-1234", "email": "service@tokyo-center.jp"}
        },
        {
            "machine_no": "M-2024-002",
            "model": "NHX 5000",
            "serial_no": "SN002345",
            "nc": {"nc_maker": "Siemens", "nc_model": "840D sl", "nc_serial": "NC002"},
            "contract": {"contract_no": "C-2024-002", "contract_date": "2024/03/20", "contract_type": "リース", "memo": "3年契約"},
            "sales": {"sales_date": "2024/03/15", "sales_person": "伊藤花子", "sales_amount": 22000000, "memo": "リピート顧客"},
            "dealer": {"dealer_name": "Osaka Machinery", "dealer_country": "Japan", "contact_person": "中村三郎", "phone": "06-1234-5678", "email": "nakamura@osaka-mach.jp"},
            "ship": {"ship_date": "2024/04/01", "ship_method": "陸上輸送", "tracking_no": "TRK002", "destination": "大阪工場", "memo": "急行便"},
            "install": {"install_date": "2024/04/10", "installer": "関西設置サービス", "location": "大阪工場B棟", "memo": "設置完了"},
            "end_user": {"company_name": "XYZ工業株式会社", "country": "Japan", "contact_person": "小林美咲", "phone": "06-9876-5432", "email": "kobayashi@xyz-ind.jp", "address": "大阪府大阪市北区2-2-2"},
            "service_base": {"base_name": "大阪サービスセンター", "country": "Japan", "contact_person": "松本サービス", "phone": "06-5555-1234", "email": "service@osaka-center.jp"}
        },
        {
            "machine_no": "M-2024-003",
            "model": "DMC 80 U",
            "serial_no": "SN003456",
            "nc": {"nc_maker": "FANUC", "nc_model": "31i-B5", "nc_serial": "NC003"},
            "contract": {"contract_no": "C-2024-003", "contract_date": "2024/05/10", "contract_type": "新規", "memo": "特別仕様"},
            "sales": {"sales_date": "2024/05/05", "sales_person": "渡辺健一", "sales_amount": 18500000, "memo": "展示会経由"},
            "dealer": {"dealer_name": "Nagoya Machine Trading", "dealer_country": "Japan", "contact_person": "加藤五郎", "phone": "052-1234-5678", "email": "kato@nagoya-trade.jp"},
            "ship": {"ship_date": "2024/06/01", "ship_method": "陸上輸送", "tracking_no": "TRK003", "destination": "名古屋工場", "memo": "標準配送"},
            "install": {"install_date": "2024/06/20", "installer": "中部設置", "location": "名古屋工場C棟", "memo": "設置とトレーニング完了"},
            "end_user": {"company_name": "DEF精密株式会社", "country": "Japan", "contact_person": "斎藤美香", "phone": "052-9876-5432", "email": "saito@def-precision.jp", "address": "愛知県名古屋市中区3-3-3"},
            "service_base": {"base_name": "名古屋サービスセンター", "country": "Japan", "contact_person": "木村サービス", "phone": "052-5555-1234", "email": "service@nagoya-center.jp"}
        }
    ]
    
    for machine_data in machines_data:
        # Insert machine
        cursor.execute(
            "INSERT INTO machines (machine_no, model, serial_no, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
            (machine_data["machine_no"], machine_data["model"], machine_data["serial_no"])
        )
        machine_id = cursor.lastrowid
        
        # Insert related data
        if "nc" in machine_data:
            cursor.execute(
                "INSERT INTO nc (machine_id, nc_maker, nc_model, nc_serial) VALUES (?, ?, ?, ?)",
                (machine_id, machine_data["nc"]["nc_maker"], machine_data["nc"]["nc_model"], machine_data["nc"]["nc_serial"])
            )
        
        if "contract" in machine_data:
            cursor.execute(
                "INSERT INTO contracts (machine_id, contract_no, contract_date, contract_type, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data["contract"]["contract_no"], machine_data["contract"]["contract_date"], 
                 machine_data["contract"]["contract_type"], machine_data["contract"]["memo"])
            )
        
        if "sales" in machine_data:
            cursor.execute(
                "INSERT INTO sales (machine_id, sales_date, sales_person, sales_amount, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data["sales"]["sales_date"], machine_data["sales"]["sales_person"],
                 machine_data["sales"]["sales_amount"], machine_data["sales"]["memo"])
            )
        
        if "dealer" in machine_data:
            cursor.execute(
                "INSERT INTO dealers (machine_id, dealer_name, dealer_country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data["dealer"]["dealer_name"], machine_data["dealer"]["dealer_country"],
                 machine_data["dealer"]["contact_person"], machine_data["dealer"]["phone"], machine_data["dealer"]["email"])
            )
        
        if "ship" in machine_data:
            cursor.execute(
                "INSERT INTO ships (machine_id, ship_date, ship_method, tracking_no, destination, memo) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data["ship"]["ship_date"], machine_data["ship"]["ship_method"],
                 machine_data["ship"]["tracking_no"], machine_data["ship"]["destination"], machine_data["ship"]["memo"])
            )
        
        if "install" in machine_data:
            cursor.execute(
                "INSERT INTO installs (machine_id, install_date, installer, location, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data["install"]["install_date"], machine_data["install"]["installer"],
                 machine_data["install"]["location"], machine_data["install"]["memo"])
            )
        
        if "end_user" in machine_data:
            cursor.execute(
                "INSERT INTO end_users (machine_id, company_name, country, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data["end_user"]["company_name"], machine_data["end_user"]["country"],
                 machine_data["end_user"]["contact_person"], machine_data["end_user"]["phone"], 
                 machine_data["end_user"]["email"], machine_data["end_user"]["address"])
            )
        
        if "service_base" in machine_data:
            cursor.execute(
                "INSERT INTO service_bases (machine_id, base_name, country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data["service_base"]["base_name"], machine_data["service_base"]["country"],
                 machine_data["service_base"]["contact_person"], machine_data["service_base"]["phone"], 
                 machine_data["service_base"]["email"])
            )
    
    conn.commit()
    conn.close()

# Pydantic models for validation
class MachineBase(BaseModel):
    machine_no: str
    model: Optional[str] = None
    serial_no: Optional[str] = None

class NCData(BaseModel):
    nc_maker: Optional[str] = None
    nc_model: Optional[str] = None
    nc_serial: Optional[str] = None

class ContractData(BaseModel):
    contract_no: Optional[str] = None
    contract_date: Optional[str] = None
    contract_type: Optional[str] = None
    memo: Optional[str] = None
    
    @field_validator('contract_date')
    @classmethod
    def validate_date(cls, v):
        if v is not None and v != "":
            if not re.match(r'^\d{4}/\d{2}/\d{2}$', v):
                raise ValueError('Date must be in YYYY/MM/DD format')
            try:
                datetime.strptime(v, '%Y/%m/%d')
            except ValueError:
                raise ValueError('Invalid date')
        return v
    
    @field_validator('memo')
    @classmethod
    def validate_memo(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('Memo must be 300 characters or less')
        return v

class SalesData(BaseModel):
    sales_date: Optional[str] = None
    sales_person: Optional[str] = None
    sales_amount: Optional[float] = None
    memo: Optional[str] = None
    
    @field_validator('sales_date')
    @classmethod
    def validate_date(cls, v):
        if v is not None and v != "":
            if not re.match(r'^\d{4}/\d{2}/\d{2}$', v):
                raise ValueError('Date must be in YYYY/MM/DD format')
            try:
                datetime.strptime(v, '%Y/%m/%d')
            except ValueError:
                raise ValueError('Invalid date')
        return v
    
    @field_validator('memo')
    @classmethod
    def validate_memo(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('Memo must be 300 characters or less')
        return v

class DealerData(BaseModel):
    dealer_name: Optional[str] = None
    dealer_country: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    @field_validator('dealer_country')
    @classmethod
    def validate_country(cls, v):
        if v is not None and v != "":
            # Check if it's a full country name (at least 3 chars, no numbers)
            if len(v) < 3 or any(char.isdigit() for char in v):
                raise ValueError('Country must be a full country name')
        return v

class ShipData(BaseModel):
    ship_date: Optional[str] = None
    ship_method: Optional[str] = None
    tracking_no: Optional[str] = None
    destination: Optional[str] = None
    memo: Optional[str] = None
    
    @field_validator('ship_date')
    @classmethod
    def validate_date(cls, v):
        if v is not None and v != "":
            if not re.match(r'^\d{4}/\d{2}/\d{2}$', v):
                raise ValueError('Date must be in YYYY/MM/DD format')
            try:
                datetime.strptime(v, '%Y/%m/%d')
            except ValueError:
                raise ValueError('Invalid date')
        return v
    
    @field_validator('memo')
    @classmethod
    def validate_memo(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('Memo must be 300 characters or less')
        return v

class InstallData(BaseModel):
    install_date: Optional[str] = None
    installer: Optional[str] = None
    location: Optional[str] = None
    memo: Optional[str] = None
    
    @field_validator('install_date')
    @classmethod
    def validate_date(cls, v):
        if v is not None and v != "":
            if not re.match(r'^\d{4}/\d{2}/\d{2}$', v):
                raise ValueError('Date must be in YYYY/MM/DD format')
            try:
                datetime.strptime(v, '%Y/%m/%d')
            except ValueError:
                raise ValueError('Invalid date')
        return v
    
    @field_validator('memo')
    @classmethod
    def validate_memo(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('Memo must be 300 characters or less')
        return v

class EndUserData(BaseModel):
    company_name: Optional[str] = None
    country: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    
    @field_validator('country')
    @classmethod
    def validate_country(cls, v):
        if v is not None and v != "":
            # Check if it's a full country name (at least 3 chars, no numbers)
            if len(v) < 3 or any(char.isdigit() for char in v):
                raise ValueError('Country must be a full country name')
        return v

class ServiceBaseData(BaseModel):
    base_name: Optional[str] = None
    country: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    @field_validator('country')
    @classmethod
    def validate_country(cls, v):
        if v is not None and v != "":
            # Check if it's a full country name (at least 3 chars, no numbers)
            if len(v) < 3 or any(char.isdigit() for char in v):
                raise ValueError('Country must be a full country name')
        return v

class MachineCreate(BaseModel):
    machine: MachineBase
    nc: Optional[NCData] = None
    contract: Optional[ContractData] = None
    sales: Optional[SalesData] = None
    dealer: Optional[DealerData] = None
    ship: Optional[ShipData] = None
    install: Optional[InstallData] = None
    end_user: Optional[EndUserData] = None
    service_base: Optional[ServiceBaseData] = None

# API Endpoints
@app.get("/api/search")
async def search_machines(q: str = Query("")):
    """Free-text search across all machine-related tables"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    search_term = f"%{q}%"
    
    # Search across all tables
    query = """
        SELECT DISTINCT m.id, m.machine_no, m.model, m.serial_no,
               nc.nc_maker, nc.nc_model,
               c.contract_no, c.contract_date,
               s.sales_person,
               d.dealer_name, d.dealer_country,
               sh.ship_date, sh.destination,
               i.install_date, i.location,
               eu.company_name as end_user_company, eu.country as end_user_country,
               sb.base_name, sb.country as service_country
        FROM machines m
        LEFT JOIN nc ON m.id = nc.machine_id
        LEFT JOIN contracts c ON m.id = c.machine_id
        LEFT JOIN sales s ON m.id = s.machine_id
        LEFT JOIN dealers d ON m.id = d.machine_id
        LEFT JOIN ships sh ON m.id = sh.machine_id
        LEFT JOIN installs i ON m.id = i.machine_id
        LEFT JOIN end_users eu ON m.id = eu.machine_id
        LEFT JOIN service_bases sb ON m.id = sb.machine_id
        WHERE m.machine_no LIKE ? OR m.model LIKE ? OR m.serial_no LIKE ?
           OR nc.nc_maker LIKE ? OR nc.nc_model LIKE ?
           OR c.contract_no LIKE ? OR c.contract_type LIKE ?
           OR s.sales_person LIKE ?
           OR d.dealer_name LIKE ? OR d.dealer_country LIKE ?
           OR sh.destination LIKE ?
           OR i.location LIKE ?
           OR eu.company_name LIKE ? OR eu.country LIKE ?
           OR sb.base_name LIKE ? OR sb.country LIKE ?
    """
    
    cursor.execute(query, [search_term] * 16)
    results = cursor.fetchall()
    
    machines = []
    for row in results:
        machines.append(dict(row))
    
    conn.close()
    return {"machines": machines}

@app.get("/api/machines/{machine_id}")
async def get_machine(machine_id: int):
    """Get detailed machine information"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get machine
    cursor.execute("SELECT * FROM machines WHERE id = ?", (machine_id,))
    machine = cursor.fetchone()
    
    if not machine:
        conn.close()
        raise HTTPException(status_code=404, detail="Machine not found")
    
    machine_dict = dict(machine)
    
    # Get related data
    cursor.execute("SELECT * FROM nc WHERE machine_id = ?", (machine_id,))
    nc = cursor.fetchone()
    machine_dict["nc"] = dict(nc) if nc else None
    
    cursor.execute("SELECT * FROM contracts WHERE machine_id = ?", (machine_id,))
    contract = cursor.fetchone()
    machine_dict["contract"] = dict(contract) if contract else None
    
    cursor.execute("SELECT * FROM sales WHERE machine_id = ?", (machine_id,))
    sales = cursor.fetchone()
    machine_dict["sales"] = dict(sales) if sales else None
    
    cursor.execute("SELECT * FROM dealers WHERE machine_id = ?", (machine_id,))
    dealer = cursor.fetchone()
    machine_dict["dealer"] = dict(dealer) if dealer else None
    
    cursor.execute("SELECT * FROM ships WHERE machine_id = ?", (machine_id,))
    ship = cursor.fetchone()
    machine_dict["ship"] = dict(ship) if ship else None
    
    cursor.execute("SELECT * FROM installs WHERE machine_id = ?", (machine_id,))
    install = cursor.fetchone()
    machine_dict["install"] = dict(install) if install else None
    
    cursor.execute("SELECT * FROM end_users WHERE machine_id = ?", (machine_id,))
    end_user = cursor.fetchone()
    machine_dict["end_user"] = dict(end_user) if end_user else None
    
    cursor.execute("SELECT * FROM service_bases WHERE machine_id = ?", (machine_id,))
    service_base = cursor.fetchone()
    machine_dict["service_base"] = dict(service_base) if service_base else None
    
    conn.close()
    return machine_dict

@app.post("/api/machines")
async def create_machine(machine_data: MachineCreate):
    """Create a new machine with related data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert machine
        cursor.execute(
            "INSERT INTO machines (machine_no, model, serial_no, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
            (machine_data.machine.machine_no, machine_data.machine.model, machine_data.machine.serial_no)
        )
        machine_id = cursor.lastrowid
        
        # Insert related data
        if machine_data.nc:
            cursor.execute(
                "INSERT INTO nc (machine_id, nc_maker, nc_model, nc_serial) VALUES (?, ?, ?, ?)",
                (machine_id, machine_data.nc.nc_maker, machine_data.nc.nc_model, machine_data.nc.nc_serial)
            )
        
        if machine_data.contract:
            cursor.execute(
                "INSERT INTO contracts (machine_id, contract_no, contract_date, contract_type, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data.contract.contract_no, machine_data.contract.contract_date,
                 machine_data.contract.contract_type, machine_data.contract.memo)
            )
        
        if machine_data.sales:
            cursor.execute(
                "INSERT INTO sales (machine_id, sales_date, sales_person, sales_amount, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data.sales.sales_date, machine_data.sales.sales_person,
                 machine_data.sales.sales_amount, machine_data.sales.memo)
            )
        
        if machine_data.dealer:
            cursor.execute(
                "INSERT INTO dealers (machine_id, dealer_name, dealer_country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data.dealer.dealer_name, machine_data.dealer.dealer_country,
                 machine_data.dealer.contact_person, machine_data.dealer.phone, machine_data.dealer.email)
            )
        
        if machine_data.ship:
            cursor.execute(
                "INSERT INTO ships (machine_id, ship_date, ship_method, tracking_no, destination, memo) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data.ship.ship_date, machine_data.ship.ship_method,
                 machine_data.ship.tracking_no, machine_data.ship.destination, machine_data.ship.memo)
            )
        
        if machine_data.install:
            cursor.execute(
                "INSERT INTO installs (machine_id, install_date, installer, location, memo) VALUES (?, ?, ?, ?, ?)",
                (machine_id, machine_data.install.install_date, machine_data.install.installer,
                 machine_data.install.location, machine_data.install.memo)
            )
        
        if machine_data.end_user:
            cursor.execute(
                "INSERT INTO end_users (machine_id, company_name, country, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data.end_user.company_name, machine_data.end_user.country,
                 machine_data.end_user.contact_person, machine_data.end_user.phone,
                 machine_data.end_user.email, machine_data.end_user.address)
            )
        
        if machine_data.service_base:
            cursor.execute(
                "INSERT INTO service_bases (machine_id, base_name, country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                (machine_id, machine_data.service_base.base_name, machine_data.service_base.country,
                 machine_data.service_base.contact_person, machine_data.service_base.phone,
                 machine_data.service_base.email)
            )
        
        conn.commit()
        conn.close()
        return {"id": machine_id, "message": "Machine created successfully"}
    
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

@app.put("/api/machines/{machine_id}")
async def update_machine(machine_id: int, machine_data: MachineCreate):
    """Update an existing machine"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if machine exists
    cursor.execute("SELECT id FROM machines WHERE id = ?", (machine_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Machine not found")
    
    try:
        # Update machine
        cursor.execute(
            "UPDATE machines SET machine_no = ?, model = ?, serial_no = ?, updated_at = datetime('now') WHERE id = ?",
            (machine_data.machine.machine_no, machine_data.machine.model, machine_data.machine.serial_no, machine_id)
        )
        
        # Update or insert related data
        if machine_data.nc:
            cursor.execute("SELECT id FROM nc WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE nc SET nc_maker = ?, nc_model = ?, nc_serial = ? WHERE machine_id = ?",
                    (machine_data.nc.nc_maker, machine_data.nc.nc_model, machine_data.nc.nc_serial, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO nc (machine_id, nc_maker, nc_model, nc_serial) VALUES (?, ?, ?, ?)",
                    (machine_id, machine_data.nc.nc_maker, machine_data.nc.nc_model, machine_data.nc.nc_serial)
                )
        
        if machine_data.contract:
            cursor.execute("SELECT id FROM contracts WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE contracts SET contract_no = ?, contract_date = ?, contract_type = ?, memo = ? WHERE machine_id = ?",
                    (machine_data.contract.contract_no, machine_data.contract.contract_date,
                     machine_data.contract.contract_type, machine_data.contract.memo, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO contracts (machine_id, contract_no, contract_date, contract_type, memo) VALUES (?, ?, ?, ?, ?)",
                    (machine_id, machine_data.contract.contract_no, machine_data.contract.contract_date,
                     machine_data.contract.contract_type, machine_data.contract.memo)
                )
        
        if machine_data.sales:
            cursor.execute("SELECT id FROM sales WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE sales SET sales_date = ?, sales_person = ?, sales_amount = ?, memo = ? WHERE machine_id = ?",
                    (machine_data.sales.sales_date, machine_data.sales.sales_person,
                     machine_data.sales.sales_amount, machine_data.sales.memo, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO sales (machine_id, sales_date, sales_person, sales_amount, memo) VALUES (?, ?, ?, ?, ?)",
                    (machine_id, machine_data.sales.sales_date, machine_data.sales.sales_person,
                     machine_data.sales.sales_amount, machine_data.sales.memo)
                )
        
        if machine_data.dealer:
            cursor.execute("SELECT id FROM dealers WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE dealers SET dealer_name = ?, dealer_country = ?, contact_person = ?, phone = ?, email = ? WHERE machine_id = ?",
                    (machine_data.dealer.dealer_name, machine_data.dealer.dealer_country,
                     machine_data.dealer.contact_person, machine_data.dealer.phone,
                     machine_data.dealer.email, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO dealers (machine_id, dealer_name, dealer_country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                    (machine_id, machine_data.dealer.dealer_name, machine_data.dealer.dealer_country,
                     machine_data.dealer.contact_person, machine_data.dealer.phone, machine_data.dealer.email)
                )
        
        if machine_data.ship:
            cursor.execute("SELECT id FROM ships WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE ships SET ship_date = ?, ship_method = ?, tracking_no = ?, destination = ?, memo = ? WHERE machine_id = ?",
                    (machine_data.ship.ship_date, machine_data.ship.ship_method,
                     machine_data.ship.tracking_no, machine_data.ship.destination,
                     machine_data.ship.memo, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO ships (machine_id, ship_date, ship_method, tracking_no, destination, memo) VALUES (?, ?, ?, ?, ?, ?)",
                    (machine_id, machine_data.ship.ship_date, machine_data.ship.ship_method,
                     machine_data.ship.tracking_no, machine_data.ship.destination, machine_data.ship.memo)
                )
        
        if machine_data.install:
            cursor.execute("SELECT id FROM installs WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE installs SET install_date = ?, installer = ?, location = ?, memo = ? WHERE machine_id = ?",
                    (machine_data.install.install_date, machine_data.install.installer,
                     machine_data.install.location, machine_data.install.memo, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO installs (machine_id, install_date, installer, location, memo) VALUES (?, ?, ?, ?, ?)",
                    (machine_id, machine_data.install.install_date, machine_data.install.installer,
                     machine_data.install.location, machine_data.install.memo)
                )
        
        if machine_data.end_user:
            cursor.execute("SELECT id FROM end_users WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE end_users SET company_name = ?, country = ?, contact_person = ?, phone = ?, email = ?, address = ? WHERE machine_id = ?",
                    (machine_data.end_user.company_name, machine_data.end_user.country,
                     machine_data.end_user.contact_person, machine_data.end_user.phone,
                     machine_data.end_user.email, machine_data.end_user.address, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO end_users (machine_id, company_name, country, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (machine_id, machine_data.end_user.company_name, machine_data.end_user.country,
                     machine_data.end_user.contact_person, machine_data.end_user.phone,
                     machine_data.end_user.email, machine_data.end_user.address)
                )
        
        if machine_data.service_base:
            cursor.execute("SELECT id FROM service_bases WHERE machine_id = ?", (machine_id,))
            if cursor.fetchone():
                cursor.execute(
                    "UPDATE service_bases SET base_name = ?, country = ?, contact_person = ?, phone = ?, email = ? WHERE machine_id = ?",
                    (machine_data.service_base.base_name, machine_data.service_base.country,
                     machine_data.service_base.contact_person, machine_data.service_base.phone,
                     machine_data.service_base.email, machine_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO service_bases (machine_id, base_name, country, contact_person, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
                    (machine_id, machine_data.service_base.base_name, machine_data.service_base.country,
                     machine_data.service_base.contact_person, machine_data.service_base.phone,
                     machine_data.service_base.email)
                )
        
        conn.commit()
        conn.close()
        return {"id": machine_id, "message": "Machine updated successfully"}
    
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the main search page"""
    return FileResponse("static/index.html")

@app.get("/detail/{machine_id}")
async def detail_page(machine_id: int):
    """Serve the detail page"""
    return FileResponse("static/detail.html")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    seed_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
