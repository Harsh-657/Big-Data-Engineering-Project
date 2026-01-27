# Big-Data-Engineering-Project

Welcome to the **DA-IICT Faculty Data Engine**.

Imagine you need to build a digital directory of every professor at DA-IICT (Faculty, Adjuncts, Distinguished Professors, etc.). Doing this manually, copy-pasting names, emails, and bios one by one, would take days and be prone to errors.

**This project automates that entire process.** It is a "Digital Pipeline" that:
1.  **Reads** the college website (Ingestion).
2.  **Cleans** the messy data (Transformation).
3.  **Organizes** it into a secure database (Storage).
4.  **Serves** it to other applications via a high-speed API (Serving).

---

##  The 4-Step Journey (How it Works)

We approached this problem by breaking it down into four distinct stages. Think of it like a manufacturing assembly line for data.

### **Phase 1: Ingestion (The Scraper)**
* **The Task:** We needed to visit 5 specific pages on the DA-IICT website (Faculty, Adjunct, International, etc.) and download the raw profile cards.
* **The Challenge:** Websites are designed for humans, not robots. They have buttons, images, and navigation menus that get in the way.
* **Our Solution:** We used Python code inside a Jupyter Notebook to navigate these pages, identify faculty profile cards, and filter out noise like "Contact Us" links.

### **Phase 2: Transformation (The Cleaner)**
* **The Task:** Raw data is messy. Phone numbers have weird dashes, emails are hidden (e.g., `user[at]daiict[dot]ac[dot]in`), and some profiles are missing photos.
* **The Challenge:** We can't put "bad data" into a database. It needs to be standardized.
* **Our Solution:** In the same Notebook, we wrote logic that:
    * Fixes email formats (converts `[at]` to `@`).
    * Standardizes phone numbers.
    * Handles "null" values (filling in blanks gracefully so the system doesn't crash).

### **Phase 3: Storage (The Structured Home)**
* **The Task:** We need a safe place to keep this data so it persists even after we turn off the computer.
* **Our Solution:** We stored the clean data into a **SQLite Database** (`faculty.db`). Think of this as a highly organized digital filing cabinet.
    * It ensures no two professors have the same email (no duplicates).
    * It keeps a record of when the data was last updated.

### **Phase 4: Serving (The Hand-off)**
* **The Task:** Finally, we need to give this clean data to Data Scientists or Mobile Apps so they can use it.
* **Our Solution:** We built a **FastAPI Server** (`main.py`).
    * This acts like a receptionist. You ask it for "All Faculty" or "Search for Gupta", and it instantly hands you the exact data in a computer-readable format (JSON).

---
## Dataset Structure

The dataset contains 110 records and 6 columns with no missing values.

| Column | Description | Type |
|-------|------------|------|
| Unnamed: 0 | Index column | Integer |
| Name | Faculty name | Text |
| Education | Qualification | Text |
| Contact Number | Phone number | Text |
| Mail-Id | Email address | Text |
| Area of Research | Specialization | Text |

All columns contain complete data. The dataset occupies approximately 5.3 KB of memory.

---
## 📂 Project Files

Here is a map of the files in this repository:

* **`Scraping and transformation.ipynb`** 
    The Jupyter Notebook that runs the "Engine" (Steps 1, 2, and 3). It scrapes the website, cleans the data, and saves it into the database.
* **`main.py`** 
    The API server. This is the code you run to access the final data in your web browser.
* **`faculty.db`** 
    The database file where all the information lives (this is created automatically by the notebook).
* **`requirements.txt`** 
    A list of tools this project needs (like `fastapi` and `pandas`).

```mermaid
flowchart LR
    A[📥 Ingestion<br/>(Scraper)] --> B[🔧 Transformation<br/>(Cleaner)]
    B --> C[🗄️ Storage<br/>(SQLite DB)]
    C --> D[🚀 Serving<br/>(FastAPI)]

    click A href "#phase-1-ingestion-the-scraper" "Go to Ingestion"
    click B href "#phase-2-transformation-the-cleaner" "Go to Transformation"
    click C href "#phase-3-storage-the-database" "Go to Storage"
    click D href "#phase-5-serving-the-api" "Go to Serving"

    style A fill:#e3f2fd,stroke:#1e88e5,stroke-width:2px
    style B fill:#e8f5e9,stroke:#43a047,stroke-width:2px
    style C fill:#fff3e0,stroke:#fb8c00,stroke-width:2px
    style D fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px
```
