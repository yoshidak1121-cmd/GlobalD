"""Main FastAPI application for GlobalD."""
import re
from typing import List
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Machine, init_db, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for app startup and shutdown."""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed (currently none)


app = FastAPI(title="GlobalD API", version="1.0.0", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def sanitize_search_query(query: str) -> str:
    """
    Sanitize search query to prevent SQL injection.
    
    Args:
        query: Raw search query string
        
    Returns:
        Sanitized query string safe for SQL LIKE
    """
    # Remove potentially dangerous characters
    # Keep alphanumeric, spaces, hyphens, underscores, and basic punctuation
    sanitized = re.sub(r'[^\w\s\-.,@#]', '', query)
    # Trim whitespace
    sanitized = sanitized.strip()
    # Limit length
    sanitized = sanitized[:100]
    return sanitized


@app.get("/api/search")
async def search_machines(
    q: str = Query(..., description="Search query string", min_length=1),
    db: Session = Depends(get_db)
) -> List[dict]:
    """
    Search machines by free-text query across multiple fields.
    
    Searches across: machine_model, machine_serial, maker, nc_model,
    contract_number, end_user, install_country, service_base
    
    Args:
        q: Search query string
        db: Database session
        
    Returns:
        List of machines matching the search query with flattened fields
    """
    # Sanitize input
    sanitized_query = sanitize_search_query(q)
    
    if not sanitized_query:
        raise HTTPException(status_code=400, detail="Invalid search query")
    
    # Build LIKE pattern for SQL
    search_pattern = f"%{sanitized_query}%"
    
    # Search across all relevant fields using OR
    results = db.query(Machine).filter(
        or_(
            Machine.machine_model.like(search_pattern),
            Machine.machine_serial.like(search_pattern),
            Machine.maker.like(search_pattern),
            Machine.nc_model.like(search_pattern),
            Machine.contract_number.like(search_pattern),
            Machine.end_user.like(search_pattern),
            Machine.install_country.like(search_pattern),
            Machine.service_base.like(search_pattern),
        )
    ).all()
    
    # Return flattened results for table display
    return [machine.to_dict() for machine in results]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "GlobalD API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search?q=<query>"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
