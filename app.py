import streamlit as st
import time
import random
import hashlib

# --- APP CONFIG & THEME ---
st.set_page_config(page_title="ICETREX PRO + VAULT", layout="centered")

# CSS for Darker Background and centered UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
    }
    .main-box {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 30px;
        border-radius: 20px;
        color: white;
        border: 1px solid #333;
        text-align: center;
    }
    .prediction-text {
        font-size: 80px;
        font-weight: bold;
        color: #00ff00;
        text-shadow: 0 0 20px #00ff00;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%; height: 70px; font-size: 20px !important;
        font-weight: bold; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PREDICTION ENGINE ---
def get_live_signal():
    # Honest probability logic
    chance = random.randint(1, 100)
    if chance > 92: # Pink
        return round(random.uniform(10.0, 50.0), 2), "🔥 PINK SIGNAL", "magenta"
    elif chance > 60: # Purple/Blue High
        return round(random.uniform(2.1, 4.5), 2), "✅ GOLDEN ENTRY", "#00ff00"
    else: # Low/Blue
        return round(random.uniform(1.2, 1.8), 2), "⚡ BLUE SCALP", "cyan"

# --- MAIN INTERFACE ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("🌿 ICETREX Stealth Sync")

# --- STATE MANAGEMENT ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = "READY"
    st.session_state.current_val = None

# --- UI CONTROLS ---
if st.session_state.app_state == "READY":
    st.write("### Awaiting Next Round...")
    if st.button("🚀 START TAKEOFF (PREDICT)"):
        # Generate the prediction exactly when the button is pressed
        st.session_state.current_val, st.session_state.label, st.session_state.color = get_live_signal()
        st.session_state.app_state = "FLYING"
        st.rerun()

elif st.session_state.app_state == "FLYING":
    # Show the prediction immediately
    st.markdown(f"""
        <div style="border: 2px solid {st.session_state.color}; border-radius: 15px; padding: 20px;">
            <p style="color: {st.session_state.color}; letter-spacing: 2px;">{st.session_state.label}</p>
            <div class="prediction-text">{st.session_state.current_val}x</div>
            <p style="color: gray;">SIGNAL LOCKED TO SERVER SEED</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Spacer
    
    if st.button("💥 FLEW AWAY (RESET)"):
        st.session_state.app_state = "READY"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# --- VIDEO VAULT ---
st.write("---")
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.header("📂 Video Evidence Vault")
uploaded_file = st.file_uploader("Upload winning rounds", type=["mp4", "webm"])
if uploaded_file:
    st.video(uploaded_file)
st.markdown('</div>', unsafe_allow_html=True)
