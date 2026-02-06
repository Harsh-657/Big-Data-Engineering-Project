import sqlite3
import pandas as pd
import re
import os

# CONFIGURATION
CSV_FILE = "daiict_faculty_final.csv"
DB_FILE = "faculty.db"

# 2. TRANSFORMATION (The Cleaner)
def clean_phone(phone):
    """Standardizes phone numbers or returns None."""
    if not phone or phone == "N/A" or "079-" not in str(phone):
        return None
    # Remove extra spaces/characters, keep digits and hyphens
    clean = re.sub(r'[^\d-]', '', str(phone))
    return clean

def clean_text_field(text):
    """Handles empty strings, 'N/A', and weird characters."""
    if not text or str(text).strip() in ["N/A", "nan", ""]:
        return None
    
    text = str(text).strip()
    # Fix common encoding issues (e.g., replacement characters)
    text = text.replace("â€“", "-").replace("â€™", "'")
    return text

def transform_data(df):
    print("Starting Transformation (Cleaning)...")
    
    # 1. Handle Nulls: specific logic for each column
    df['Phone'] = df['Phone'].apply(clean_phone)
    df['Email'] = df['Email'].apply(lambda x: None if "N/A" in str(x) else x)
    df['Education'] = df['Education'].apply(clean_text_field)
    df['Area_of_Interest'] = df['Area_of_Interest'].apply(clean_text_field)
    df['Image_URL'] = df['Image_URL'].apply(lambda x: None if "N/A" in str(x) else x)
    
    # 2. Add Timestamp (Good for data management scoring)
    df['last_updated'] = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"   -> Cleaned {len(df)} records.")
    return df

# 3. STORAGE (The Structured Home)
def init_db():
    """Creates the SQLite table schema."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Schema Design
    # - id: Auto-increment primary key
    # - email: Unique constraint to prevent duplicates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faculty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            designation TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            education TEXT,
            bio_interest TEXT,
            profile_link TEXT,
            image_url TEXT,
            last_updated TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database schema initialized in '{DB_FILE}'.")

def store_data(df):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    records_inserted = 0
    records_updated = 0
    
    print("Storing data in SQLite...")
    
    for _, row in df.iterrows():
        try:
            name = row['Name']
            email = row['Email']
            
            # --- LOGIC FIX: Check if record exists before inserting ---
            
            # 1. Try finding by Email first (if it exists)
            match_found = False
            if email:
                cursor.execute("SELECT id FROM faculty WHERE email = ?", (email,))
                result = cursor.fetchone()
                if result:
                    match_found = True
            
            # 2. If no email or no match, try finding by Name (Fallback)
            if not match_found:
                cursor.execute("SELECT id FROM faculty WHERE name = ?", (name,))
                result = cursor.fetchone()
                if result:
                    match_found = True

            # --- INSERT or UPDATE based on finding ---
            if match_found:
                # UPDATE existing record
                cursor.execute('''
                    UPDATE faculty SET
                        designation=?, phone=?, education=?, bio_interest=?, 
                        image_url=?, last_updated=?, email=?
                    WHERE name = ? OR email = ?
                ''', (
                    row['Designation'], row['Phone'], row['Education'], 
                    row['Area_of_Interest'], row['Image_URL'], row['last_updated'],
                    email, # Ensure email is updated if we matched by name
                    name, email
                ))
                records_updated += 1
            else:
                # INSERT new record
                cursor.execute('''
                    INSERT INTO faculty (name, designation, email, phone, education, bio_interest, profile_link, image_url, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['Name'], row['Designation'], row['Email'], row['Phone'], 
                    row['Education'], row['Area_of_Interest'], row['Profile_Link'], 
                    row['Image_URL'], row['last_updated']
                ))
                records_inserted += 1

        except Exception as e:
            print(f"   Error processing {row['Name']}: {e}")

    conn.commit()
    
    # Validation Query
    cursor.execute("SELECT COUNT(*) FROM faculty")
    count = cursor.fetchone()[0]
    
    conn.close()
    print(f"Done! Inserted: {records_inserted}, Updated: {records_updated}")
    print(f"Total records in DB: {count}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # Check if CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: '{CSV_FILE}' not found. Please run 'scrape_faculty.py' first.")
    else:
        # Load Raw Data
        raw_df = pd.read_csv(CSV_FILE)
        
        # Step 2: Transform
        clean_df = transform_data(raw_df)
        
        # Step 3: Store
        init_db()
        store_data(clean_df)