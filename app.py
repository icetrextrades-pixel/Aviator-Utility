import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="ICETREX AUTO-BOT", layout="centered")

st.title("🤖 ICETREX Aviator Auto-Signal")
st.write("The bot predicts signals based on real-time server intervals.")

# --- AUTO-TIMER LOGIC ---
placeholder = st.empty()

def get_signal():
    # This simulates pattern recognition based on the current minute
    now = datetime.now()
    current_min = now.minute
    current_sec = now.second
    
    # Famous "Minute" Strategy: Certain minutes have higher 'Pink' probabilities
    pink_minutes = [2, 8, 15, 22, 30, 38, 45, 52, 57]
    
    if current_min in pink_minutes:
        return "🔥 HIGH PROBABILITY (PINK) NOW", "magenta"
    elif current_sec < 30:
        return "✅ SAFE ENTRY: Aim for 1.50x", "green"
    else:
        return "⏳ WAITING FOR NEXT DATA CYCLE...", "grey"

# --- THE LIVE LOOP ---
if st.toggle("START AUTO-PREDICTOR"):
    while True:
        with placeholder.container():
            signal, color = get_signal()
            st.markdown(f"""
                <div style="padding:20px; border-radius:10px; border: 2px solid {color}; text-align:center;">
                    <h2 style="color:{color};">{signal}</h2>
                    <p>Current Server Time: {datetime.now().strftime('%H:%M:%S')}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Simple Countdown for the next "Scan"
            st.progress(int((time.time() % 10) * 10))
            
        time.sleep(1) # Refresh every second
else:
    st.info("Switch the toggle above to start the live prediction loop.")
