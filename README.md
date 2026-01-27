# 🎓 DA-IICT Faculty Data Engine

> **A fully automated data pipeline that scrapes, transforms, stores, and serves DA-IICT faculty information through a RESTful API.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)

---

## 🎯 Problem Statement

Manually collecting and maintaining information for hundreds of faculty members across multiple departments is:
- ⏰ **Time-consuming** (days of manual copy-pasting)
- ❌ **Error-prone** (typos, outdated information)
- 🔄 **Not scalable** (hard to update when changes occur)

**Our Solution:** An automated end-to-end data pipeline that eliminates manual work and ensures data consistency.

---

## 🏗️ Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DA-IICT FACULTY DATA PIPELINE                     │
└─────────────────────────────────────────────────────────────────────────┘

    📡 DATA SOURCE                🔧 PROCESSING              💾 STORAGE         🚀 SERVING
    ═════════════                ═════════════             ═════════         ═══════════
         
    ┌──────────┐                                                            
    │ DA-IICT  │                ┌──────────────┐          ┌──────────┐     ┌──────────┐
    │ Website  │───────────────>│   Scraper    │─────────>│  Clean   │────>│ SQLite   │
    │ (5 Pages)│                │   (Python)   │          │Transform │     │ Database │
    └──────────┘                └──────────────┘          └──────────┘     └────┬─────┘
         │                              │                      │                │
         │                              │                      │                │
    Faculty Lists              • BeautifulSoup        • Email fixing       Auto-created
    Adjunct Faculty            • HTTP Requests        • Phone standards    faculty.db
    International              • HTML Parsing         • Null handling           │
    Distinguished              • Data Filtering       • Deduplication           │
    Visiting                                                                    │
                                                                                ▼
                                                                          ┌──────────┐
                                                                          │ FastAPI  │
                                                                          │  Server  │
                                                                          └────┬─────┘
                                                                               │
                                                                               ▼
                                                                    ┌──────────────────┐
                                                                    │  REST API        │
                                                                    │  Endpoints       │
                                                                    │                  │
                                                                    │ • GET /faculty   │
                                                                    │ • GET /search    │
                                                                    │ • GET /stats     │
                                                                    └──────────────────┘
```

---

## 🔄 The 4-Phase Pipeline

### **Phase 1: 📥 Data Ingestion**
**Objective:** Extract raw faculty data from DA-IICT website

- **Target Sources:** 5 faculty category pages (Faculty, Adjunct, International, Distinguished, Visiting)
- **Technology:** Python with BeautifulSoup and Requests
- **Challenges Solved:**
  - Dynamic HTML structure navigation
  - Filtering non-faculty elements (navigation, footers, ads)
  - Handling missing or inconsistent page structures
  
**Output:** Raw faculty profile data (names, emails, phone numbers, departments, photos)

---

### **Phase 2: 🧹 Data Transformation**
**Objective:** Clean and standardize extracted data

**Data Quality Issues Fixed:**
- ✉️ Email formats: `user[at]daiict[dot]ac[dot]in` → `user@daiict.ac.in`
- 📞 Phone standardization: Various formats → Consistent format
- 🖼️ Missing photos: Handle null/placeholder images
- 🔤 Text normalization: Trim whitespace, fix encoding issues

**Validation Rules:**
- Email format verification
- Duplicate detection and removal
- Required field checks (name, department)

**Output:** Clean, validated, structured data ready for storage

---

### **Phase 3: 💾 Data Storage**
**Objective:** Persist data in a reliable, queryable format

**Database:** SQLite (`faculty.db`)

**Schema Design:**
```sql
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    department TEXT,
    category TEXT,
    photo_url TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Features:**
- ✅ UNIQUE constraint on email (prevents duplicates)
- 📅 Automatic timestamp tracking
- 🔍 Indexed fields for fast queries
- 💪 ACID compliance for data integrity

---

### **Phase 4: 🚀 Data Serving**
**Objective:** Expose data through a high-performance REST API

**Technology:** FastAPI (Python's fastest web framework)

**API Endpoints:**
```
GET  /faculty          → Retrieve all faculty members
GET  /faculty/{id}     → Get specific faculty by ID
GET  /search?q=name    → Search faculty by name/department
GET  /stats            → Get database statistics
```

**Response Format:** JSON (easily consumable by web/mobile apps)

**Benefits:**
- ⚡ Async support for high concurrency
- 📚 Auto-generated API documentation (Swagger UI)
- 🔒 Built-in validation and error handling

---

## 📂 Project Structure

```
da-iict-faculty-engine/
│
├── 📓 Scraping and transformation.ipynb    # Core ETL pipeline (Phases 1-3)
│   ├── Web scraping logic
│   ├── Data cleaning functions
│   └── Database insertion
│
├── 🐍 main.py                              # FastAPI server (Phase 4)
│   ├── Route definitions
│   ├── Database queries
│   └── Response formatting
│
├── 🗄️ faculty.db                           # SQLite database (auto-generated)
│   └── Stores all faculty records
│
├── 📋 requirements.txt                     # Python dependencies
│   ├── fastapi
│   ├── uvicorn
│   ├── beautifulsoup4
│   ├── requests
│   ├── pandas
│   └── sqlite3 (built-in)
│
└── 📄 README.md                            # This file
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd da-iict-faculty-engine
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the data pipeline**
```bash
jupyter notebook "Scraping and transformation.ipynb"
# Execute all cells to scrape and build the database
```

4. **Start the API server**
```bash
uvicorn main:app --reload
```

5. **Access the API**
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
- Raw API: http://localhost:8000/faculty

---

## 🎯 Use Cases

This data engine can power:

1. **🌐 Web Applications**
   - Faculty directory websites
   - Student portals
   - Department dashboards

2. **📱 Mobile Apps**
   - Campus navigation apps
   - Faculty contact apps
   - Event management systems

3. **📊 Data Analytics**
   - Department size analysis
   - Contact information audits
   - Faculty distribution reports

4. **🤖 Chatbots & AI Assistants**
   - "Who teaches Machine Learning?"
   - "How do I contact Prof. Gupta?"

---

## 🔧 Technical Highlights

### Performance Optimizations
- ⚡ Async database queries in FastAPI
- 🗂️ Database indexing on frequently queried fields
- 💾 In-memory caching for repeated requests

### Error Handling
- ❌ Graceful degradation when website structure changes
- 🔄 Retry logic for network failures
- 📝 Comprehensive logging for debugging

### Data Quality
- ✅ Email validation using regex
- 🔍 Duplicate detection algorithms
- 📊 Data completeness reports

---

## 📊 Sample API Response

```json
{
  "faculty": [
    {
      "id": 1,
      "name": "Dr. John Doe",
      "email": "john.doe@daiict.ac.in",
      "phone": "+91-79-12345678",
      "department": "Computer Science",
      "category": "Faculty",
      "photo_url": "https://example.com/photo.jpg",
      "last_updated": "2025-01-27T10:30:00Z"
    }
  ],
  "total": 150,
  "timestamp": "2025-01-27T12:00:00Z"
}
```

---

## 🛠️ Future Enhancements

- [ ] **Automated Scheduling:** Run scraper daily via cron jobs
- [ ] **Change Detection:** Alert when faculty info changes
- [ ] **Advanced Search:** Filter by department, research areas
- [ ] **Data Visualization:** Department distribution charts
- [ ] **Export Options:** CSV/Excel download endpoints
- [ ] **Authentication:** Secure API with JWT tokens
- [ ] **Rate Limiting:** Prevent API abuse
- [ ] **Cloud Deployment:** Host on AWS/GCP/Azure

---

## 📝 License

This project is for educational purposes. Ensure compliance with DA-IICT's website terms of service before scraping.

---


## 🙏 Acknowledgments

- DA-IICT for providing publicly accessible faculty information
- FastAPI team for the excellent web framework
- Python community for amazing libraries

---
