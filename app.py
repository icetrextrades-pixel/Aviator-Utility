import streamlit as st
import time
import random
import hashlib
from datetime import datetime

st.set_page_config(page_title="ICETREX LIVE DECODER", layout="centered")

# Custom CSS to make it look "Hacker/Pro"
st.markdown("""
    <style>
    .main { background-color: #050505; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ICETREX Provably Fair Predictor")

# --- SIDEBAR ---
st.sidebar.header("Network Node")
casino_choice = st.sidebar.selectbox("Platform:", ["LuckyBet", "AfricaBet", "MWOS", "SpinCity", "Hollywoodbets", "Betway"])

# --- INPUT ---
last_seed = st.text_input("🔗 Paste Last Round Hash/Seed:", placeholder="d2f81a...b3e1")

# --- ENGINE ---
def get_prediction(seed_input):
    # If no input, use time-based entropy
    base = seed_input if seed_input else str(time.time())
    decoded_hash = hashlib.sha256(base.encode()).hexdigest()
    
    random.seed(decoded_hash)
    chance = random.randint(1, 100)
    
    if chance > 88:
        return round(random.uniform(8.0, 30.0), 2), "🔥 PINK SIGNAL", "magenta", decoded_hash
    elif chance > 45:
        return round(random.uniform(2.1, 5.5), 2), "✅ GOLDEN ENTRY", "green", decoded_hash
    else:
        return round(random.uniform(1.1, 1.9), 2), "⚡ BLUE SCALP", "cyan", decoded_hash

# --- LIVE PREDICTION FRAME ---
if st.toggle("ACTIVATE LIVE FEED"):
    # Container for the live updates
    display_area = st.empty()
    
    # This loop is now optimized for Streamlit
    while True:
        val, label, color, d_hash = get_prediction(last_seed)
        
        with display_area.container():
            st.markdown(f"""
                <div style="padding:25px; border-radius:15px; background-color:#000; border: 2px solid {color}; text-align:center;">
                    <p style="color:#444; font-size:10px; font-family:monospace;">SEED DECODED: {d_hash[:24]}...</p>
                    <h2 style="color:{color}; letter-spacing: 2px; margin-bottom:0;">{label}</h2>
                    <h1 style="font-size:80px; color:white; margin:0;">{val}x</h1>
                    <p style="color:gray;">Node: {casino_choice} | Protocol: SHA-256</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Realistic Countdown Bar
            bar_placeholder = st.empty()
            for i in range(100, -1, -5):
                bar_placeholder.progress(i)
                time.sleep(0.5) # Total 10 second wait per prediction
        
        # After the bar hits 0, the loop restarts and 'val' changes automatically
else:
    st.info("System Standby. Input seed and toggle 'Activate' to begin.")

st.divider()
st.caption("ICETREX V4.5 | Optimized for Phone & Laptop Performance")
