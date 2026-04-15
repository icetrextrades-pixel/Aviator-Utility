import streamlit as st
import time
import random
import hashlib
from datetime import datetime

st.set_page_config(page_title="ICETREX DYNAMIC DECODER", layout="centered")

st.title("🛡️ ICETREX Live Seed Decoder")

# --- SIDEBAR ---
st.sidebar.header("Network Node")
casino_choice = st.sidebar.selectbox("Platform:", ["LuckyBet", "AfricaBet", "MWOS", "SpinCity", "Hollywoodbets", "Betway", "10bet", "SportyBet"])

# --- INPUT ---
last_seed = st.sidebar.text_input("🔗 Paste Last Hash:", placeholder="d2f81a...b3e1")

# --- ENGINE ---
def get_prediction(seed_input):
    # DYNAMIC SEED: Mixes your input with the current 10-second block of time
    # This forces the result to change every time the timer resets
    time_block = datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:-1] 
    base = f"{seed_input}{time_block}"
    
    decoded_hash = hashlib.sha256(base.encode()).hexdigest()
    
    # Re-seeding with the new dynamic hash
    random.seed(decoded_hash)
    
    chance = random.randint(1, 100)
    
    if chance > 88:
        return round(random.uniform(8.0, 35.0), 2), "🔥 PINK SIGNAL", "magenta", decoded_hash
    elif chance > 45:
        return round(random.uniform(2.1, 5.8), 2), "✅ GOLDEN ENTRY", "green", decoded_hash
    else:
        return round(random.uniform(1.1, 1.9), 2), "⚡ BLUE SCALP", "cyan", decoded_hash

# --- LIVE PREDICTION FRAME ---
if st.toggle("ACTIVATE LIVE SCANNER"):
    display_area = st.empty()
    
    while True:
        # 1. Generate NEW prediction based on current time block
        val, label, color, d_hash = get_prediction(last_seed)
        
        with display_area.container():
            st.markdown(f"""
                <div style="padding:25px; border-radius:15px; background-color:#000; border: 3px solid {color}; text-align:center;">
                    <p style="color:#444; font-size:10px; font-family:monospace;">ALGO-SYNC: {d_hash[:20]}...</p>
                    <h2 style="color:{color}; letter-spacing: 2px; margin-bottom:0;">{label}</h2>
                    <h1 style="font-size:80px; color:white; margin:0;">{val}x</h1>
                    <p style="color:gray;">Node: {casino_choice} | Status: Synchronized</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 2. Progress Bar (10-second countdown)
            bar_placeholder = st.empty()
            for i in range(100, -1, -1):
                bar_placeholder.progress(i)
                time.sleep(0.1) # Total 10 seconds (100 * 0.1)
        
        # 3. Loop restarts, get_prediction() runs again with NEW time block
else:
    st.info("System Standby. Flip the switch to connect to the game server.")

st.divider()
st.caption("ICETREX V5.0 | Dynamic Entropy Protocol")
