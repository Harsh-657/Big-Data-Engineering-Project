import streamlit as st
import sqlite3
import pandas as pd
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="DA-IICT Faculty Finder",
    page_icon="🎓",
    layout="wide"
)

# --- PATH SETUP ---
# We use relative paths so it works on your laptop AND the cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "faculty.db")
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "faculty_embeddings.pkl")
CSV_PATH = os.path.join(BASE_DIR, "daiict_faculty_final.csv")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: white; }
    .stTextInput > div > div > input { background-color: #262730; color: white; }
    .profile-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #41444e;
    }
    .metric-score {
        color: #00ffa3;
        font-weight: bold;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# --- 🧠 LOAD THE BRAIN (Cached) ---
@st.cache_resource
def load_resources():
    """Loads the AI model and pre-computed embeddings."""
    if not os.path.exists(EMBEDDINGS_PATH) or not os.path.exists(CSV_PATH):
        return None, None, None
    
    # 1. Load Model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 2. Load Embeddings
    with open(EMBEDDINGS_PATH, 'rb') as f:
        vectors = pickle.load(f)
        
    # 3. Load Data Mapping
    df = pd.read_csv(CSV_PATH)
    
    return model, vectors, df

model, faculty_vectors, df_data = load_resources()

# --- 🔍 SEARCH LOGIC ---
def search_faculty(query, top_k=5):
    if not query or model is None:
        return []
    
    # 1. Vectorize Query
    query_vector = model.encode([query])
    
    # 2. Calculate Similarity
    similarities = cosine_similarity(query_vector, faculty_vectors).flatten()
    
    # 3. Get Top Results
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        score = similarities[idx]
        if score > 0.2: # Threshold to filter bad matches
            row = df_data.iloc[idx]
            results.append({
                "name": row['Name'],
                "designation": row['Designation'],
                "email": row.get('Email', 'N/A'),
                "phone": row.get('Phone', 'N/A'),
                "education": row.get('Education', ''),
                "interests": row.get('Area_of_Interest', ''),
                "image": row.get('Image_URL', ''),
                "link": row.get('Profile_Link', '#'),
                "score": round(score * 100, 1) # Convert to percentage
            })
    return results

# --- 🎨 UI LAYOUT ---

st.title("🎓 DA-IICT Faculty Finder")
st.caption("🚀 Powered by AI Semantic Search")

# Sidebar for controls
with st.sidebar:
    st.header("⚙️ Search Settings")
    top_k = st.slider("Number of Results", 1, 20, 5)
    st.markdown("---")
    st.info("This tool uses **Vector Embeddings** to find professors based on research meaning, not just keywords.")

# Main Search Bar
query = st.text_input("🔍 What are you looking for?", placeholder="e.g., 'Who works on sustainable energy and green computing?'")

if query:
    if model is None:
        st.error("⚠️ AI Models not found! Please run `generate_embeddings.py` first.")
    else:
        with st.spinner("🤖 Analyzing faculty profiles..."):
            results = search_faculty(query, top_k=top_k)
        
        if not results:
            st.warning("No relevant faculty found. Try broader terms.")
        else:
            st.success(f"Found {len(results)} relevant professors!")
            
            for person in results:
                # Create a card-like layout
                with st.container():
                    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        # Handle missing images with a default avatar
                        img_url = person['image'] if isinstance(person['image'], str) and person['image'].startswith('http') else "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                        st.image(img_url, width=120)
                        st.markdown(f"<div class='metric-score'>match: {person['score']}%</div>", unsafe_allow_html=True)
                    
                    with col2:
                        st.subheader(f"{person['name']}")
                        st.markdown(f"**{person['designation']}**")
                        
                        if person['interests']:
                            st.markdown(f"🔬 **Interests:** {person['interests']}")
                        
                        if person['education']:
                            st.markdown(f"🎓 **Education:** {person['education']}")
                            
                        st.markdown(f"📧 `{person['email']}`")
                        
                        st.markdown(f"[🌐 View Full Profile]({person['link']})")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown("---")

else:
    # Landing page content
    st.markdown("### 💡 Try searching for:")
    col1, col2 = st.columns(2)
    with col1:
        st.code("Machine Learning in Healthcare")
        st.code("VLSI and Embedded Systems")
    with col2:
        st.code("Graph Theory and Algorithms")
        st.code("Wireless Communication 5G")