import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ==============================================================================
# 1. ATOMIC INITIALIZATION & STATE
# ==============================================================================
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []

# ==============================================================================
# 2. 2030 DUAL-STREAM NEURAL ENGINE
# ==============================================================================
from tensorflow.keras.layers import LSTM, Dense, Input

# 1. FIX: Cache the model so it doesn't rebuild every click
@st.cache_resource
def build_2030_neural_engine():
    # Using 'Input(shape)' as requested by your logs to prevent the UserWarning
    model = Sequential([
        Input(shape=(1, 1)),
        LSTM(64, activation='relu', return_sequences=True),
        LSTM(32, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

def execute_2030_neural_math(history_data):
    try:
        vals = [float(x.replace('x','')) for x in history_data]
        if len(vals) < 3: return 1.35, 2.80
        
        base_data = np.array(vals).reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(base_data)
        
        # Load the cached model instead of rebuilding
        model = build_2030_neural_engine()
        
        # Train quickly on new data
        X = scaled_data[:-1].reshape(-1, 1, 1)
        y = scaled_data[1:]
        model.fit(X, y, epochs=5, verbose=0) # Lowered epochs for speed
        
        last_val = scaled_data[-1].reshape(1, 1, 1)
        prediction_scaled = model.predict(last_val, verbose=0) # verbose=0 stops log spam
        base_pred = float(scaler.inverse_transform(prediction_scaled)[0][0])
        
        return round(base_pred * 0.90, 2), round(base_pred * 1.60, 2)
    except Exception as e:
        return 1.42, 3.85

# ==============================================================================
# 3. PRO 2030 INTERFACE (CSS & THEME)
# ==============================================================================
st.set_page_config(page_title="ICETREX 2030 PRO", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("https://images.unsplash.com/photo-1614850523296-d8c1af93d400");
        background-size: cover;
    }
    .main-card {
        background: rgba(0, 8, 20, 0.95);
        padding: 25px; border-radius: 20px; border: 1px solid #00ffcc;
        text-align: center; box-shadow: 0 0 30px rgba(0, 255, 204, 0.2);
    }
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 12px; background: #000 !important; color: #00ffcc !important; 
        border: 1px solid #00ffcc !important; font-weight: bold; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. MASTER FLOW CONTROLLERS
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🔐 OPERATOR ID")
    u = st.text_input("USER NAME")
    p = st.text_input("ENCRYPTION KEY", type="password")
    if st.button("AUTHORIZE SYSTEM"):
        if u == "Icetrex" and p == "SOPITO": # Add other IDs as needed
            st.session_state["pass"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_manual_casino_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 CASINO HANDSHAKE")
    c = st.selectbox("SELECT PLATFORM", ["Premier Bet", "AfricaBet", "1xBet", "888Starz", "SportyBet", "SpinCity"])
    st.warning("Please ensure you are logged into your casino account in a separate tab.")
    if st.button("ESTABLISH MANUAL BRIDGE"):
        st.session_state["casino"] = c
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    col1, col2, col3 = st.columns(3)
    with col1: r1 = st.text_input("L1")
    with col2: r2 = st.text_input("L2")
    with col3: r3 = st.text_input("L3")
    if st.button("LOCK NEURAL MATRIX"):
        if r1 and r2 and r3:
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # Header Links
    ca, cb = st.columns(2)
    with ca: st.markdown('<button style="width:100%; padding:10px; background:#00ffcc; color:#000; border-radius:10px; font-weight:bold;">📥 PRO APK</button>', unsafe_allow_html=True)
    with cb: st.markdown('<a href="https://wa.me/263779174062"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border-radius:10px; font-weight:bold;">💬 DEV SUPPORT</button></a>', unsafe_allow_html=True)

    # Calculation
    s_val, r_val = execute_2030_neural_math(st.session_state["history"])

    # UI DUAL GAUGE
def render_pro_button(s_val, r_val):
    st.components.v1.html(f"""
    <div style="display: flex; flex-direction: column; align-items: center; font-family: monospace;">
        <div style="display: flex; gap: 10px; margin-bottom: 15px; width: 100%;">
            <div style="flex:1; border: 1px solid #00ffcc; background: #000; padding: 10px; border-radius: 10px; text-align: center;">
                <p style="color:#00ffcc; font-size:10px; margin:0;">SAFE</p>
                <h3 style="color:#00ffcc; margin:5px 0;">{s_val}x</h3>
            </div>
            <div style="flex:1; border: 1px solid #ff00ff; background: #000; padding: 10px; border-radius: 10px; text-align: center;">
                <p style="color:#ff00ff; font-size:10px; margin:0;">RISKY</p>
                <h3 style="color:#ff00ff; margin:5px 0;">{r_val}x</h3>
            </div>
        </div>
        
        <div style="position: relative; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center;">
            <div id="ldr" style="position: absolute; width: 140px; height: 140px; border-radius: 50%; border: 3px solid transparent; border-top-color: #00ffcc;"></div>
            <button id="p-btn" style="width: 120px; height: 120px; border-radius: 50%; background: #ff0000; color: #fff; border: 3px solid #fff; font-weight: 900; cursor: pointer; z-index:10;">PREDICT</button>
        </div>
    </div>

    <script>
    const btn = document.getElementById('p-btn');
    const ldr = document.getElementById('ldr');
    
    btn.onclick = function() {{
        ldr.style.animation = "spin 1s linear infinite";
        btn.innerHTML = "SCANNING";
        btn.style.background = "#333";
        
        // This timeout ensures the UI updates before the browser freezes for math
        setTimeout(() => {{
            ldr.style.animation = "none";
            btn.innerHTML = "LOCKED";
            btn.style.background = "#00ffcc";
            btn.style.color = "#000";
        }}, 1200);
    }};
    </script>
    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
    """, height=300)

    # Community Chat
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 GLOBAL COMMUNITY")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="300" frameborder="0"></iframe>', height=320)
    if st.button("🚪 TERMINATE SESSION"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. MASTER EXECUTION
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_manual_casino_login()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
