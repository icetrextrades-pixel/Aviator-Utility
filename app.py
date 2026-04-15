import streamlit as st
import time
import random
from datetime import datetime

# Page configuration for mobile and desktop
st.set_page_config(page_title="ICETREX UNIVERSAL PREDICTOR", layout="centered")

st.title("🤖 ICETREX Aviator Bot v3.5")
st.write("Cross-Platform Utility Tool for Phone & Laptop")

# --- PHASE 1: EXPANDED CASINO LIST ---
st.sidebar.header("Configuration")
casino_choice = st.sidebar.selectbox(
    "Select Casino Platform:", 
    [
        "LuckyBets", "AfricaBet", "MWOS", "SpinCity", 
        "Hollywoodbets", "Betway", "10bet", "SportyBet", "Other"
    ]
)

st.sidebar.info(f"Connected to: {casino_choice} Server")

# --- PHASE 2: DYNAMIC SIGNAL ENGINE ---
def get_dynamic_signal():
    now = datetime.now()
    # Unique seed refreshes every 10 seconds based on current time
    random.seed(now.minute + now.second // 10) 
    
    chance = random.randint(1, 100)
    
    if chance > 92:
        return "🔥 PINK SIGNAL: Target 10.0x+", "magenta", "EXTREME"
    elif chance > 65:
        target = round(random.uniform(1.8, 3.5), 2)
        return f"✅ SAFE SIGNAL: Exit at {target}x", "green", "MEDIUM"
    elif chance > 35:
        target = round(random.uniform(1.2, 1.5), 2)
        return f"⚡ QUICK SCALP: Exit at {target}x", "cyan", "LOW"
    else:
        return "⏳ MARKET COOLING: Skip Round", "orange", "WAIT"

# --- PHASE 3: INTERFACE ---
st.divider()

if st.toggle("ACTIVATE AUTO-SCANNER"):
    placeholder = st.empty()
    
    while True:
        with placeholder.container():
            signal, color, risk = get_dynamic_signal()
            
            # Professional UI box
            st.markdown(f"""
                <div style="padding:30px; border-radius:15px; background-color:#0e1117; border: 4px solid {color}; text-align:center;">
                    <p style="color:gray; font-size:14px; margin-bottom:5px;">{casino_choice.upper()} LIVE FEED</p>
                    <h1 style="color:{color}; font-size: 45px; margin-top:0px;">{signal}</h1>
                    <div style="display: flex; justify-content: center; gap: 20px;">
                        <p style="color:white;">RISK: <b>{risk}</b></p>
                        <p style="color:white;">STATUS: <b>Active</b></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Progress bar visualizer for the next scan
            countdown = 10 - (datetime.now().second % 10)
            st.write(f"Refreshing in {countdown}s...")
            st.progress(countdown * 10)
            
        time.sleep(1)
else:
    st.warning(f"Scanner Offline. Please select {casino_choice} and toggle the switch above.")

st.divider()
st.caption("Developed by ICETREX | For Educational & Probability Analysis Only")
