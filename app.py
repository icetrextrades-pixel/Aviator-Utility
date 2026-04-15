import streamlit as st
import time
import random
import hashlib

st.set_page_config(page_title="ICETREX PREDICT PRO", layout="centered")

# Custom CSS for the Large Predict Button
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 100px;
        font-size: 30px !important;
        font-weight: bold;
        background-color: #ff4b4b;
        color: white;
        border-radius: 15px;
        border: none;
        box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.4);
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
        color: white;
    }
    .reset-btn>div>button {
        height: 50px !important;
        font-size: 18px !important;
        background-color: #333 !important;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ICETREX Universal Predictor")

# --- SIDEBAR CONFIG ---
st.sidebar.header("Network Settings")
casino = st.sidebar.selectbox("Select Node:", ["LuckyBets", "AfricaBet", "MWOS", "SpinCity", "Betway", "Hollywoodbets"])
seed_input = st.sidebar.text_input("🔗 Server Seed:", placeholder="Paste Hash Here")

# --- ENGINE ---
def generate_prediction(seed):
    entropy = f"{seed}{time.time()}"
    d_hash = hashlib.sha256(entropy.encode()).hexdigest()
    random.seed(d_hash)
    
    chance = random.randint(1, 100)
    if chance > 94:
        return round(random.uniform(15.0, 80.0), 2), "🌌 GALAXY (PINK)", "magenta"
    elif chance > 70:
        return round(random.uniform(3.5, 10.0), 2), "🔥 HIGH MULTI", "red"
    elif chance > 40:
        return round(random.uniform(1.8, 3.2), 2), "✅ STABLE", "green"
    else:
        return round(random.uniform(1.1, 1.5), 2), "⚡ SCALP", "cyan"

# --- STATE MANAGEMENT ---
if 'status' not in st.session_state:
    st.session_state.status = "READY"

# --- MAIN UI ---
st.divider()

if st.session_state.status == "READY":
    st.write("### Wait for Plane Takeoff...")
    if st.button("🚀 PREDICT NEXT ROUND"):
        st.session_state.prediction = generate_prediction(seed_input)
        st.session_state.status = "ACTIVE"
        st.rerun()

elif st.session_state.status == "ACTIVE":
    val, label, color = st.session_state.prediction
    
    st.markdown(f"""
        <div style="padding:40px; border-radius:20px; background-color:#111; border: 5px solid {color}; text-align:center;">
            <h2 style="color:{color}; letter-spacing: 3px; margin: 0;">{label}</h2>
            <h1 style="font-size:100px; color:white; margin:10px 0;">{val}x</h1>
            <p style="color:gray;">Node: {casino} Locked</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Secondary button to reset
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🛑 RESET (Round Finished)"):
        st.session_state.status = "READY"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("ICETREX V8.0 | Mobile Optimized Utility")
