import streamlit as st
import time
import random
import hashlib

st.set_page_config(page_title="ICETREX CIRCLE SYNC", layout="centered")

# --- ADVANCED CIRCULAR UI ---
st.markdown("""
    <style>
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .circle-container {
        display: flex; justify-content: center; align-items: center;
        height: 300px; position: relative;
    }
    .outer-circle {
        width: 250px; height: 250px;
        border-radius: 50%;
        border: 10px solid #222;
        border-top: 10px solid #00ff00;
        animation: rotate 2s linear infinite;
    }
    .inner-val {
        position: absolute; font-size: 50px; font-weight: bold; color: white;
    }
    .stButton>button {
        width: 100%; height: 80px; font-size: 22px !important;
        background-color: #ff4b4b; color: white; border-radius: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ICETREX Circle Sync v10.0")

# --- SETTINGS ---
casino = st.sidebar.selectbox("Active Node:", ["LuckyBets", "AfricaBet", "MWOS", "SpinCity", "Betway", "Hollywoodbets"])
risk_level = st.sidebar.select_slider("Risk Profile:", options=["LOW", "MEDIUM", "HIGH"])

def generate_logic(risk):
    # Logic adjusted to be more "honest" with actual game rhythms
    chance = random.randint(1, 100)
    if risk == "HIGH" and chance > 80:
        return round(random.uniform(5.0, 20.0), 2)
    elif risk == "MEDIUM" and chance > 50:
        return round(random.uniform(2.0, 4.5), 2)
    else:
        return round(random.uniform(1.2, 1.8), 2)

# --- STATE CONTROL ---
if 'mode' not in st.session_state:
    st.session_state.mode = "WAITING"

if st.session_state.mode == "WAITING":
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 PREDICT NEXT ROUND"):
        st.session_state.target = generate_logic(risk_level)
        st.session_state.mode = "FLYING"
        st.rerun()

elif st.session_state.mode == "FLYING":
    placeholder = st.empty()
    
    # --- ANIMATION LOOP ---
    # The "Circle" stays active while we count up to the predicted value
    current_val = 1.00
    step = 0.05
    
    while current_val <= st.session_state.target:
        with placeholder.container():
            st.markdown(f"""
                <div class="circle-container">
                    <div class="outer-circle"></div>
                    <div class="inner-val">{current_val:.2f}x</div>
                </div>
                <p style="text-align:center; color:gray;">{casino} SEED DECODING IN PROGRESS...</p>
            """, unsafe_allow_html=True)
        
        # Speed of the count-up (Faster for lower numbers, slower for high)
        time.sleep(0.1) 
        current_val += (st.session_state.target / 50) 
        
    # --- FLIGHT ENDED ---
    st.session_state.mode = "FINISHED"
    st.rerun()

elif st.session_state.mode == "FINISHED":
    st.markdown(f"""
        <div style="text-align:center; padding:50px; border: 2px solid red; border-radius:20px;">
            <h1 style="color:red; font-size:60px;">FLEW AWAY!</h1>
            <h2 style="color:white;">At {st.session_state.target}x</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 PREPARE NEXT ROUND"):
        st.session_state.mode = "WAITING"
        st.rerun()

st.divider()
st.caption(f"Sync Protocol: {casino} / {risk_level}")
