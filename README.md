# 🎓 DA-IICT Faculty Data Engine

> **A fully automated, AI-powered data pipeline that scrapes, transforms, stores, and intelligently serves DA-IICT faculty information through an interactive web interface.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![AI](https://img.shields.io/badge/AI-Sentence--BERT-orange.svg)](https://www.sbert.net/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)]()

## 🌟 Live Demo

**🚀 Try it yourself:** [faculty-finder.streamlit.app](https://faculty-finder.streamlit.app) *(Replace with your actual deployment URL)*

**Features:**
- 🔍 **Smart Search:** Find faculty by name, department, or research interests
- 🧠 **AI-Powered:** Semantic search understands context, not just keywords
- ⚡ **Lightning Fast:** Pre-computed embeddings for instant results
- 📱 **Mobile-Friendly:** Responsive design works on all devices

---

## ✨ Key Features

### 🎯 Intelligent Search
- **Natural Language Queries:** Search "professors working on AI" instead of exact keywords
- **Context-Aware Results:** Finds "machine learning expert" when you search "neural networks"
- **Ranked by Relevance:** AI-powered similarity scoring puts best matches first

### 📊 Comprehensive Data
- **150+ Faculty Profiles:** Complete database of DA-IICT faculty
- **5 Categories:** Faculty, Adjunct, International, Distinguished, Visiting
- **Rich Information:** Name, email, phone, department, research areas, photos

### 🛠️ Developer-Friendly
- **Modular Architecture:** Separate scripts for each pipeline phase
- **REST API Option:** JSON endpoints for integration with other apps
- **Well-Documented Code:** Clear comments and function docstrings
- **Easy Deployment:** One-click hosting on Streamlit Cloud

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
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        DA-IICT FACULTY DATA PIPELINE (5 PHASES)                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    📡 INGESTION        🔧 TRANSFORM         💾 STORAGE         🧠 AI BRAIN        🚀 SERVING
    ════════════        ═══════════         ═══════════        ═══════════        ══════════
         
    ┌──────────┐                                                                            
    │ DA-IICT  │       ┌──────────┐        ┌──────────┐      ┌───────────┐     ┌──────────┐
    │ Website  │──────>│  Scraper │───────>│  Clean   │─────>│  SQLite   │────>│Embeddings│
    │(5 Pages) │       │  (Py)    │        │Transform │      │ Database  │     │Generator │
    └──────────┘       └──────────┘        └──────────┘      └──────────┘     └────┬─────┘
         │                   │                    │                │                 │
         │                   │                    │                │                 │
    Faculty Lists    BeautifulSoup      Email fixing        faculty.db        Vector AI
    Adjunct          HTTP Requests      Phone standards     ACID DB          Sentence-T
    International    HTML Parsing       Null handling                             │
    Distinguished    Filtering          Deduplication                             │
    Visiting                                                                       ▼
         │                   │                    │                          ┌──────────┐
         ▼                   ▼                    ▼                          │ .pkl     │
    scrape_faculty.py    store_data.py      faculty.db                      │Embeddings│
         │                                                                   └────┬─────┘
         ▼                                                                        │
    daiict_faculty_final.csv                                                     │
                                                                                  ▼
                                                                          ┌──────────────┐
                                                                          │  Streamlit   │
                                                                          │   Web App    │
                                                                          │  (app.py)    │
                                                                          └──────┬───────┘
                                                                                 │
                                                                                 ▼
                                                                      ┌─────────────────────┐
                                                                      │  🌐 Web Interface   │
                                                                      │  • Semantic Search  │
                                                                      │  • Faculty Profiles │
                                                                      │  • Filters          │
                                                                      └─────────────────────┘
                                                                      
                                                         ALTERNATIVE: FastAPI (main.py)
                                                                      ↓
                                                              REST API Endpoints
                                                              /faculty, /search, /stats
```

---

## 🔄 The 5-Phase Pipeline

### **Phase 1: 📥 Data Ingestion**
**Objective:** Extract raw faculty data from DA-IICT website

- **Target Sources:** 5 faculty category pages (Faculty, Adjunct, International, Distinguished, Visiting)
- **Technology:** Python with BeautifulSoup and Requests
- **Implementation:** `scrape_faculty.py`
- **Challenges Solved:**
  - Dynamic HTML structure navigation
  - Filtering non-faculty elements (navigation, footers, ads)
  - Handling missing or inconsistent page structures
  
**Output:** `daiict_faculty_final.csv` - Raw faculty profile data (names, emails, phone numbers, departments, photos)

---

### **Phase 2: 🧹 Data Transformation**
**Objective:** Clean and standardize extracted data

**Implementation:** `store_data.py`

**Initial Data Quality Assessment:**

Our scraping process identified several data quality issues that needed to be addressed before storage:

| Column Name | Missing Values | Data Type |
|-------------|----------------|-----------|
| Name | 0 | object |
| Education | 2 | object |
| Contact Number | 27 | object |
| Mail-Id | 1 | object |
| Area of Research | 3 | object |

*Table: Missing value analysis from scraped faculty data*

**Data Quality Issues Fixed:**
- ✉️ Email formats: `user[at]daiict[dot]ac[dot]in` → `user@daiict.ac.in`
- 📞 Phone standardization: Various formats → Consistent format (27 missing values handled)
- 🎓 Education field: 2 missing entries populated with "N/A"
- 🔬 Area of Research: 3 missing entries handled appropriately
- 🖼️ Missing photos: Handle null/placeholder images
- 🔤 Text normalization: Trim whitespace, fix encoding issues

**Validation Rules:**
- Email format verification (1 invalid email corrected)
- Duplicate detection and removal
- Required field checks (name, department)
- Missing value imputation strategies

**Output:** Clean, validated, structured data ready for storage

---

### **Phase 3: 💾 Data Storage**
**Objective:** Persist data in a reliable, queryable format

**Implementation:** `store_data.py` (same module as Phase 2)

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

### **Phase 4: 🧠 AI Enhancement (Semantic Search)**
**Objective:** Enable intelligent, context-aware faculty search

**Implementation:** `generate_embeddings.py`

**Technology:** 
- **Sentence Transformers** (all-MiniLM-L6-v2 model)
- **Vector Embeddings** for semantic similarity
- **scikit-learn** for cosine similarity calculations

**How It Works:**
1. Converts faculty data (names, research areas, departments) into vector embeddings
2. Stores embeddings in `faculty_embeddings.pkl`
3. Enables natural language queries like "machine learning professor" to find relevant faculty
4. Returns results ranked by semantic similarity (not just keyword matching)

**Benefits:**
- 🎯 **Smart Search:** Understands intent, not just keywords
- 🔍 **Contextual Results:** Finds "AI researcher" when you search "neural networks"
- ⚡ **Fast Retrieval:** Pre-computed embeddings for instant results

**Output:** `faculty_embeddings.pkl` - Vector representations of faculty data

---

### **Phase 5: 🚀 User Interface & Serving**
**Objective:** Provide accessible interfaces for end users

#### **Option A: Streamlit Web App (Primary)**
**Implementation:** `app.py`

**Features:**
- 🎨 Clean, modern interface
- 🔍 Semantic search integration
- 📊 Real-time results display
- 📱 Mobile-responsive design
- 🌐 One-click deployment to Streamlit Cloud

**Endpoints (via UI):**
- Search faculty by name/department/research area
- View detailed faculty profiles
- Filter by category (Faculty, Adjunct, etc.)

#### **Option B: FastAPI REST API (Alternative)**
**Implementation:** `main.py`

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
├── 🔍 scrape_faculty.py                    # Phase 1: Web scraping module
│   └── Extracts faculty data from DA-IICT website
│
├── 💾 store_data.py                        # Phase 2 & 3: Data cleaning & storage
│   ├── Cleans and transforms scraped data
│   └── Creates SQLite database
│
├── 🧠 generate_embeddings.py               # AI Enhancement: Semantic search
│   └── Creates vector embeddings for intelligent search
│
├── 🎨 app.py                               # Phase 4: Streamlit web interface
│   ├── Interactive faculty search UI
│   ├── Semantic search integration
│   └── Real-time query results
│
├── 🐍 main.py                              # Alternative: FastAPI REST API
│   ├── RESTful endpoints
│   └── JSON response formatting
│
├── 📊 daiict_faculty_final.csv             # Intermediate: Scraped raw data
│
├── 🗄️ faculty.db                           # Database: Cleaned faculty records
│
├── 🧮 faculty_embeddings.pkl               # AI Model: Vector embeddings
│
├── 📋 requirements.txt                     # Python dependencies
│   ├── streamlit
│   ├── sentence-transformers
│   ├── pandas
│   ├── scikit-learn
│   └── torch (CPU version)
│
├── 📊 Assets/                              # Documentation assets
│   ├── pipeline-architecture.svg          # Visual pipeline diagram
│   └── data-quality-analysis.jpg          # Missing values report
│
└── 📄 README.md                            # This file
```

---

## 📊 Project Documentation Assets

This repository includes visual documentation to help understand the data pipeline:

1. **Pipeline Architecture Diagram** (`pipeline-architecture.svg`)
   - Complete visual representation of all 4 phases
   - Shows data flow from web scraping to API serving
   - Includes technology stack and component details

2. **Data Quality Analysis** (`data-quality-analysis.jpg`)
   - Missing value analysis from initial scraping
   - Helps understand the cleaning challenges we faced
   - Referenced in Phase 2 documentation above

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/Harsh-657/Faculty-Finder.git
cd Faculty-Finder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the Pipeline (Execute in Order)

**Step 1: 📡 Data Ingestion (Scraping)**
```bash
python scrape_faculty.py
```
- **Output:** `daiict_faculty_final.csv`
- **Purpose:** Extracts faculty data from 5 DA-IICT web pages
- **Duration:** ~30-60 seconds

**Step 2: 🧹 Data Transformation & Storage**
```bash
python store_data.py
```
- **Output:** `faculty.db` (SQLite database)
- **Purpose:** Cleans data and stores in structured format
- **Duration:** ~5-10 seconds

**Step 3: 🧠 AI Enhancement (Semantic Search)**
```bash
python generate_embeddings.py
```
- **Output:** `faculty_embeddings.pkl`
- **Purpose:** Creates vector embeddings for intelligent search
- **Duration:** ~30 seconds (first run, downloads AI model)

**Step 4: 🎨 Launch the Web Interface**
```bash
streamlit run app.py
```
- **Access:** Opens automatically at `http://localhost:8501`
- **Features:** 
  - Interactive search interface
  - Semantic search powered by AI
  - Real-time faculty information display

### Alternative: REST API Server

If you prefer a REST API instead of the web interface:

```bash
python main.py
```
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`
- Endpoints: `/faculty`, `/search`, `/stats`

---

## 🌐 Deployment (Public Hosting)

### Deploy to Streamlit Community Cloud (Free)

**Step 1: Prepare Repository**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Important:** Ensure these files are in your repository:
- `app.py`
- `requirements.txt`
- `daiict_faculty_final.csv`
- `faculty_embeddings.pkl`

**Note:** If `faculty_embeddings.pkl` exceeds 100MB, use Git LFS:
```bash
git lfs install
git lfs track "*.pkl"
git add .gitattributes
```

**Step 2: Deploy**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New App"**
4. Select your repository (`Harsh-657/Faculty-Finder`)
5. Set main file: `app.py`
6. Click **"Deploy"**

**Step 3: Share**

Your app will be live at: `https://faculty-finder.streamlit.app`

Streamlit automatically:
- ✅ Installs dependencies from `requirements.txt`
- ✅ Loads your data files
- ✅ Provides free HTTPS hosting
- ✅ Auto-updates on git push

### Deploy to Other Platforms

<details>
<summary><b>Heroku Deployment</b></summary>

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create faculty-finder-app
git push heroku main
```
</details>

<details>
<summary><b>AWS/GCP/Azure Deployment</b></summary>

Use Docker for containerized deployment:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```
</details>

---

## 🎯 Use Cases

This data engine can power:

1. **🌐 Interactive Web Applications**
   - **Faculty Finder (Streamlit)** - Primary use case
   - Student portals with semantic search
   - Department dashboards
   - Academic advisor lookup tools

2. **📱 Mobile Apps**
   - Campus navigation apps
   - Faculty contact apps (via API)
   - Event management systems

3. **📊 Data Analytics & Research**
   - Department size analysis
   - Research area clustering
   - Contact information audits
   - Faculty distribution reports
   - Publication co-authorship networks

4. **🤖 AI-Powered Applications**
   - **Semantic Search** - "Find professors working on climate change"
   - Chatbots & virtual assistants
   - Recommendation engines
   - Smart course-faculty matching

---

## 🔧 Technical Highlights

### AI/ML Capabilities
- 🧠 **Semantic Search:** Sentence-BERT embeddings for context-aware search
- 🎯 **Smart Ranking:** Cosine similarity for relevance scoring
- 📊 **Vector Storage:** Efficient pickle serialization for fast loading
- 🔄 **Model Caching:** One-time download, persistent usage

### Performance Optimizations
- ⚡ Async database queries in FastAPI
- 🗂️ Database indexing on frequently queried fields
- 💾 Pre-computed embeddings for instant search
- 🚀 Streamlit caching for faster page loads

### Error Handling
- ❌ Graceful degradation when website structure changes
- 🔄 Retry logic for network failures
- 📝 Comprehensive logging for debugging
- ⚠️ User-friendly error messages in UI

### Data Quality
- ✅ Email validation using regex
- 🔍 Duplicate detection algorithms
- 📊 Data completeness reports
- 🧹 Automated data cleaning pipelines

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

### Automation & Monitoring
- [ ] **Automated Scheduling:** Run scraper daily via cron jobs or GitHub Actions
- [ ] **Change Detection:** Email alerts when faculty info changes
- [ ] **Health Monitoring:** Track scraper success rates and API uptime
- [ ] **Version Control:** Historical tracking of faculty data changes

### Enhanced Search & Discovery
- [x] ✅ **Semantic Search** (Already implemented!)
- [ ] **Advanced Filters:** Multi-select department, research area, designation
- [ ] **Fuzzy Search:** Handle typos and partial names
- [ ] **Related Faculty:** "People also viewed" recommendations
- [ ] **Research Collaboration Graph:** Visualize co-authorship networks

### Data Enrichment
- [ ] **Publication Integration:** Fetch papers from Google Scholar
- [ ] **Citation Metrics:** H-index, total citations display
- [ ] **Course Mappings:** Link faculty to courses they teach
- [ ] **Office Hours:** Scrape and display availability

### User Experience
- [ ] **Dark Mode:** Toggle for Streamlit interface
- [ ] **Export Options:** Download search results as CSV/PDF
- [ ] **Bookmarking:** Save favorite faculty profiles
- [ ] **Share Links:** Direct URLs to specific faculty profiles

### Security & Scalability
- [ ] **Authentication:** User login for personalized features
- [ ] **Rate Limiting:** Prevent API abuse
- [ ] **CDN Integration:** Faster image loading
- [ ] **Database Migration:** Move to PostgreSQL for production scale
- [ ] **Cloud Deployment:** Host on AWS/GCP/Azure with auto-scaling

---

## 🐛 Troubleshooting

### Common Issues

**Q: `ModuleNotFoundError: No module named 'sentence_transformers'`**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Q: `generate_embeddings.py` is slow on first run**
- **Expected behavior:** The AI model (~80MB) downloads on first run
- Takes 30-60 seconds depending on internet speed
- Subsequent runs are instant (model is cached)

**Q: Streamlit app shows "File not found: faculty_embeddings.pkl"**
```bash
# Solution: Run embeddings generation first
python generate_embeddings.py
# Then run the app
streamlit run app.py
```

**Q: Web scraping fails with connection errors**
- **Possible causes:** DA-IICT website is down or structure changed
- Check internet connection
- Verify website is accessible: https://www.daiict.ac.in
- If structure changed, update selectors in `scrape_faculty.py`

**Q: `faculty.db` file is locked**
- Close any database browser tools (DB Browser for SQLite)
- Make sure no other scripts are accessing the database
- Restart your terminal/IDE

**Q: Streamlit app doesn't show on `localhost:8501`**
```bash
# Check if port is in use
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Mac/Linux

# Use a different port
streamlit run app.py --server.port 8502
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is for educational purposes. Ensure compliance with DA-IICT's website terms of service before scraping.

---

## 👤 Author

**Harsh Jethwani (Harsh-657)**  
🔗 GitHub: [@Harsh-657](https://github.com/Harsh-657)  
📦 Repository: [Faculty-Finder](https://github.com/Harsh-657/Faculty-Finder)

---

## 🙏 Acknowledgments

- DA-IICT for providing publicly accessible faculty information
- FastAPI team for the excellent web framework
- Python community for amazing libraries
