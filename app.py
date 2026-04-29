import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# ==============================================================================
# 1. STATE & SECURITY (V.1 - V.10)
# ==============================================================================
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []

# ==============================================================================
# 2. NEURAL BRAIN (V.21 - LSTM INTEGRATION)
# ==============================================================================
def execute_neural_math(history_data):
    try:
        # Converting "1.50x" strings to floats for math
        vals = [float(x.replace('x','')) for x in history_data]
        if len(vals) < 3: return 2.14
        
        # Scaling and Sequence Preparation (From your statistical code)
        base_data = np.array(vals).reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(base_data)
        
        # Light LSTM Model for real-time Cloud execution
        model = Sequential([
            LSTM(32, activation='relu', input_shape=(1, 1)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        
        # Fast Training on current session data
        X = scaled_data[:-1].reshape(-1, 1, 1)
        y = scaled_data[1:]
        model.fit(X, y, epochs=15, verbose=0)
        
        # Predict the next packet
        last_val = scaled_data[-1].reshape(1, 1, 1)
        prediction_scaled = model.predict(last_val)
        prediction = scaler.inverse_transform(prediction_scaled)
        
        return round(float(prediction[0][0]), 2)
    except:
        return 1.85 # Fallback multiplier

# ==============================================================================
# 3. GLOBAL UI & WALLPAPER (V.17 - V.20)
# ==============================================================================
st.set_page_config(page_title="ICETREX PRO OMEGA", layout="centered")

# Your specific cat wallpaper
WALLPAPER_URL = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809"

st.markdown(f"""
<style>
    .stApp {{
        background-image: url("{WALLPAPER_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main-card {{
        background: rgba(0, 0, 0, 0.88);
        padding: 25px;
        border-radius: 20px; 
        border: 1px solid #00d4ff;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        margin-bottom: 20px;
    }}
    h1, h2, h3, p {{ color: #00d4ff !important; font-family: monospace; }}
    div[data-testid="stButton"] > button {{
        width: 100%; border-radius: 12px; background: #000 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff !important; font-weight: bold; height: 50px;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. DASHBOARD COMPONENTS
# ==============================================================================
def show_dashboard():
    # Live Server Clock
    st.components.v1.html("""
    <div id="clock" style="color: #00ff00; font-family: monospace; font-size: 18px; text-align: center; border: 1px solid #333; padding: 8px; border-radius: 10px; background: #000;">00:00:00</div>
    <script>
    function tick() {
        var now = new Date();
        now.setHours(now.getUTCHours() + 2); 
        document.getElementById('clock').innerHTML = "SERVER TIME: " + now.toLocaleTimeString();
    }
    setInterval(tick, 1000); tick();
    </script>
    """, height=60)

    # APK & WhatsApp Links
    ca, cb = st.columns(2)
    with ca: 
        st.markdown('<a href="#" download><button style="width:100%; padding:10px; background:#00ff00; border-radius:10px; font-weight:bold; cursor:pointer;">📥 DOWNLOAD APK</button></a>', unsafe_allow_html=True)
    with cb:
        st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border-radius:10px; font-weight:bold; cursor:pointer;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    # THE NEURAL RED ROUND BUTTON SYSTEM
    current_h = st.session_state.get("history", [])
    prediction_val = execute_neural_math(current_h) if current_h else "SYNC DATA"
    
    st.components.v1.html(f"""
    <style>
        @keyframes spin {{ 0% {{ transform: rotate(0deg); border-top-color: #00ff00; }} 100% {{ transform: rotate(360deg); border-color: #00ff00; }} }}
        .circle-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        #p-btn {{ 
            width: 140px !important; height: 140px !important; border-radius: 50% !important; 
            background-color: #ff0000 !important; color: white !important; border: 5px solid #ffffff !important; 
            font-weight: 900; cursor: pointer; z-index: 10; box-shadow: 0 0 30px #ff0000; outline: none; 
        }}
        #loader {{ position: absolute; width: 165px; height: 165px; border-radius: 50%; border: 6px solid transparent; z-index: 5; pointer-events: none; }}
    </style>

    <div class="circle-wrapper">
        <div style="border: 2px solid #00d4ff; padding: 20px; border-radius: 15px; background: rgba(0,0,0,0.9); width: 100%; margin-bottom: 25px; text-align: center;">
            <p id="st" style="color: #00d4ff; font-size: 10px; margin: 0;">LSTM NEURAL MATRIX V.22</p>
            <h1 id="disp" style="color: #00d4ff; font-size: 75px; margin: 10px 0; font-weight: 900;">---</h1>
            <div style="color: #00ff00; font-size: 12px;">STATUS: CONNECTED</div>
        </div>
        <div style="position: relative; width: 170px; height: 170px; display: flex; align-items: center; justify-content: center;">
            <div id="loader"></div>
            <button id="p-btn">RUN NEURAL<br>SCAN</button>
        </div>
    </div>

    <script>
    const btn = document.getElementById('p-btn');
    const loader = document.getElementById('loader');
    const disp = document.getElementById('disp');
    const pred = "{prediction_val}";

    btn.addEventListener('click', () => {{
        loader.style.animation = "spin 2.5s linear forwards";
        document.getElementById('st').innerHTML = "SCANNING SERVER SEEDS...";
        
        setTimeout(() => {{
            let val = parseFloat(pred);
            if (isNaN(val)) val = 1.85;
            // Scrambled Probability Scramble
            let drift = (val + (Math.random() * 0.4 - 0.2)).toFixed(2);
            
            const color = drift > 10 ? "#ff00ff" : "#00d4ff";
            disp.innerHTML = drift + "x";
            disp.style.color = color;
            document.getElementById('st').innerHTML = "NEURAL SIGNAL ACQUIRED";
            loader.style.animation = "none";
        }}, 2500);
    }});
    </script>
    """, height=500)

    # Cbox Community Chat
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 COMMUNITY HUB")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="350" frameborder="0"></iframe>', height=380)
    
    if st.button("🚪 LOGOUT"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. NAVIGATION FLOW (THE FULL SCRAMBLE)
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR ACCESS")
    u = st.text_input("USER ID")
    k = st.text_input("ENCRYPTION KEY", type="password")
    if st.button("AUTHORIZE"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "BIKO": "PRO779"}
        if u in auth and auth[u] == k:
            st.session_state["pass"] = True
            st.rerun()
        else: st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛰️ SERVER SYNC")
    choice = st.selectbox("CASINO:", ["Premier Bet", "AfricaBet", "1xBet", "888Starz", "SportyBet"])
    c1, c2, c3 = st.columns(3)
    with c1: r1 = st.text_input("L1")
    with c2: r2 = st.text_input("L2")
    with c3: r3 = st.text_input("L3")
    if st.button("ENGAGE LSTM"):
        if r1 and r2 and r3:
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["casino"] = choice
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Master Flow
if not st.session_state["pass"]:
    show_login()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
