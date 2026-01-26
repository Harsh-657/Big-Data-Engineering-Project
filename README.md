# Big-Data-Engineering-Project

## Welcome! What is this?
Welcome to the **DA-IICT Faculty Data Engine**.

Imagine you need to create a digital directory of every professor at DA-IICT (Faculty, Adjuncts, Distinguished Professors, etc.). Doing this manually—copy-pasting names, emails, and bios one by one—would take days and be prone to errors.

**This project automates that entire process.** It is a "Digital Pipeline" that:
1.  **Reads** the college website (Ingestion).
2.  **Cleans** the messy data (Transformation).
3.  **Organizes** it into a secure database (Storage).
4.  **Serves** it to other applications via a high-speed API (Serving).

---

## 🚀 The 4-Step Journey (How it Works)

We approached this problem by breaking it down into four distinct stages. Think of it like a manufacturing assembly line for data.

### **Phase 1: Ingestion (The Scraper)**
* **The Task:** We needed to visit 5 specific pages on the DA-IICT website and download the raw profile cards.
* **The Challenge:** Websites are designed for humans, not robots. They have buttons, images, and navigation menus that get in the way.
* **Our Solution:** We built a "Scout" script (`scrape_faculty.py`) that navigates these pages, identifies faculty profile cards, and filters out noise like "Contact Us" links.

### **Phase 2: Transformation (The Cleaner)**
* **The Task:** Raw data is messy. Phone numbers have weird dashes, emails are hidden (e.g., `user[at]daiict[dot]ac[dot]in`), and some profiles are missing photos.
* **The Challenge:** We can't put "bad data" into a database. It needs to be standardized.
* **Our Solution:** We built a "Cleaner" script (`store_data.py`) that:
    * Fixes email formats (converts `[at]` to `@`).
    * Standardizes phone numbers.
    * Handles "null" values (filling in blanks gracefully so the system doesn't crash).

### **Phase 3: Storage (The Structured Home)**
* **The Task:** We need a safe place to keep this data so it persists even after we turn off the computer.
* **Our Solution:** We designed a **SQLite Database** (`faculty.db`). Think of this as a highly organized digital filing cabinet.
    * It ensures no two professors have the same email (no duplicates).
    * It keeps a record of when the data was last updated.

### **Phase 4: Serving (The Hand-off)**
* **The Task:** Finally, we need to give this clean data to Data Scientists or Mobile Apps so they can use it.
* **Our Solution:** We built a **FastAPI Server** (`main.py`).
    * This acts like a receptionist. You ask it for "All Faculty" or "Search for Gupta", and it instantly hands you the exact data in a computer-readable format (JSON).

---

## 📂 Project Files

Here is a map of the files in this repository:

* **`scrape_faculty.py`** 🕵️  
    The script that goes out to the internet and fetches the raw data into a CSV file.
* **`store_data.py`** 🧹  
    The script that reads the CSV, cleans the data, and saves it into the SQLite database.
* **`main.py`** 💁  
    The API server. This is the code you run to access the data in your browser.
* **`faculty.db`** 🗄️  
    The database file where all the final information lives (this is created automatically).
* **`requirements.txt`** 📋  
    A list of tools this project needs (like `fastapi` and `pandas`).

