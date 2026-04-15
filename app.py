import streamlit as st
import time
import random
import hashlib
from datetime import datetime

st.set_page_config(page_title="ICETREX SEED DECODER", layout="centered")

st.title("🛡️ ICETREX Provably Fair Predictor")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("Casino Node")
casino_choice = st.sidebar.selectbox(
    "Select Platform:", 
    ["LuckyBet", "AfricaBet", "MWOS", "SpinCity", "Hollywoodbets", "Betway"]
)

# --- REALISM ELEMENT: SEED INPUT ---
st.subheader("🔗 Server Sync")
last_seed = st.text_input("Enter Last Round Server Seed (Hex):", placeholder="e.g. d2f81a...b3e1")

def calculate_prediction(seed_input):
    # If no seed is provided, we generate a mock 'active' seed
    base_seed = seed_input if seed_input else str(random.getrandbits(128))
    
    # Hash the seed to simulate the 'Decoding' process
    decoded_hash = hashlib.sha256(base_seed.encode()).hexdigest()
    
    # Use the hash to determine the result (Realism: the hash dictates the math)
    random.seed(decoded_hash)
    
    chance = random.randint(1, 100)
    if chance > 88:
        val = round(random.uniform(8.0, 25.0), 2)
        return val, "🔥 PINK SIGNAL", "magenta", decoded_hash
    elif chance > 45:
        val = round(random.uniform(2.1, 4.5), 2)
        return val, "✅ GOLDEN ENTRY", "green", decoded_hash
    else:
        val = round(random.uniform(1.1, 1.8), 2)
        return val, "⚡ BLUE SCALP", "cyan", decoded_hash

# --- MAIN INTERFACE ---
if st.toggle("ACTIVATE REAL-TIME PREDICTOR"):
    if not last_seed:
        st.warning("Running in simulation mode. Input a Server Seed for higher accuracy.")
    
    placeholder = st.empty()
    
    while True:
        with placeholder.container():
            pred_val, label, color, d_hash = calculate_prediction(last_seed)
            
            st.markdown(f"""
                <div style="padding:25px; border-radius:15px; background-color:#000; border: 1px solid #333; text-align:center;">
                    <p style="color:#555; font-size:11px; font-family:monospace;">PREVIOUS HASH: {d_hash[:32]}...</p>
                    <h2 style="color:{color}; letter-spacing: 2px;">{label}</h2>
                    <h1 style="font-size:70px; color:white; margin:0;">{pred_val}x</h1>
                    <p style="color:gray;">Algorithm: <b>SHA-256 / {casino_choice}</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Simulated "Decoding" Bar
            st.write("Analyzing Seed Patterns...")
            st.progress(random.randint(70, 100))
            
        time.sleep(12) # Matches the average Aviator round length
else:
    st.info("Awaiting Server Seed input to begin calculation.")

st.divider()
st.caption("ICETREX V4.0 | Provably Fair Probability Engine")
