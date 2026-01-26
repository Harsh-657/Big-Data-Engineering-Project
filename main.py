from fastapi import FastAPI, HTTPException, Query
import sqlite3
from pydantic import BaseModel
from typing import List, Optional
import os

# CONFIGURATION
DB_FILE = "faculty.db"

app = FastAPI(
    title="DA-IICT Faculty API",
    description="Local API serving scraped faculty data.",
    version="1.0"
)

# 1. Data Model
class FacultyModel(BaseModel):
    id: int
    name: str
    designation: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    education: Optional[str] = None
    bio_interest: Optional[str] = None
    profile_link: Optional[str] = None
    image_url: Optional[str] = None
    last_updated: Optional[str] = None

# 2. Database Helper
def get_db_connection():
    if not os.path.exists(DB_FILE):
        # Friendly error if you forgot to run the scraper first
        raise HTTPException(status_code=500, detail="Database 'faculty.db' not found. Please run your scraper script first.")
    
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

# 3. API Endpoints

@app.get("/")
def home():
    return {"status": "Running locally on VS Code", "docs_url": "http://127.0.0.1:8000/docs"}

@app.get("/faculty", response_model=List[FacultyModel])
def get_all_faculty(limit: int = 100):
    """Get all faculty members (limited to 100 by default)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/faculty/search")
def search_faculty(q: str):
    """Search for a faculty member by name."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Case-insensitive search using SQL wildcard %
    cursor.execute("SELECT * FROM faculty WHERE name LIKE ?", (f"%{q}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]