import pandas as pd
from sentence_transformers import SentenceTransformer
import pickle
import os

# CONFIGURATION
CSV_FILE = "daiict_faculty_final.csv"
OUTPUT_FILE = "faculty_embeddings.pkl"

def generate_embeddings():
    print("Starting AI Embedding Generator...")

    # 1. Check if CSV exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: '{CSV_FILE}' not found. Please run 'scrape_faculty.py' first.")
        return

    # 2. Load Data
    print("Loading faculty data...")
    df = pd.read_csv(CSV_FILE)
    print(f"   -> Loaded {len(df)} records.")

    # 3. Create 'Search Text'
    # We combine name, designation, and bio into one big string for the AI to read
    print("Preparing text for analysis...")
    df['search_text'] = df.apply(
        lambda x: f"{x['Name']} {x['Designation']} {x['Area_of_Interest']} {x['Education']}", 
        axis=1
    )

    # 4. Load AI Model
    # 'all-MiniLM-L6-v2' is a small, fast model perfect for laptops
    print("Loading AI Model (sentence-transformers)...")
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Error loading model: {e}")
        print("(Try running: pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu)")
        return

    # 5. Generate Embeddings
    print("Converting text to vectors (This might take a minute)...")
    embeddings = model.encode(df['search_text'].tolist(), show_progress_bar=True)

    # 6. Save to File
    print(f"Saving embeddings to '{OUTPUT_FILE}'...")
    with open(OUTPUT_FILE, 'wb') as f:
        pickle.dump(embeddings, f)

    print("Success! You can now run the API server.")

if __name__ == "__main__":
    generate_embeddings()