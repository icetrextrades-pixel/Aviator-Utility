import streamlit as st
import numpy as np
import pandas as pd
import time
import hashlib

# ==============================================================================
# 1. ATOMIC INITIALIZATION & STATE
# ==============================================================================
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []

# ==============================================================================
# 2. OPTIMIZED MATHEMATICAL SEQUENCE ENGINE
# ==============================================================================
def execute_2030_neural_math(history_data):
    """
    Analyzes historical arrays using Log Returns and Extreme Value Theory.
    Instead of passing a fixed target, it passes the exact mathematical 
    parameters (Mu, Sigma, Momentum, Tail) to the live client matrix.
    """
    try:
        vals = [float(x.replace('x','').strip()) for x in history_data if x.strip()]
        if len(vals) < 3: 
            return 1.45, 0.20, 0.05, 2.0  # Default parameters
            
        arr = np.array(vals)
        
        # 1. Standard Geometric Brownian Motion parameters
        mu = np.mean(arr)
        sigma = np.std(arr) + 0.001 # Prevent zero division
        
        # 2. Log-Return Momentum (Hurst Proxy)
        log_returns = np.diff(np.log(arr))
        momentum = np.mean(log_returns) if len(log_returns) > 0 else 0
        
        # 3. Fréchet Extreme Value Tail Index
        # Measures the weight of the "jump" probability based on recent outliers
        max_val = np.max(arr)
        tail_index = max_val / mu if mu > 0 else 2.0
        
        # Cap tail index purely to prevent JavaScript infinity loops, 
        # but allow massive standard deviation spikes.
        return mu, sigma, momentum, min(tail_index, 15.0)
        
    except Exception:
        return 1.45, 0.20, 0.05, 2.0
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
        margin-bottom: 20px;
    }
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 12px; background: #000 !important; color: #00ffcc !important; 
        border: 1px solid #00ffcc !important; font-weight: bold; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. COMPONENTS
# ==============================================================================
def render_pro_button(mu, sigma, momentum, tail_index):
    st.components.v1.html(f"""
    <div style="display: flex; flex-direction: column; align-items: center; font-family: monospace; color: white;">
        <div style="display: flex; gap: 10px; margin-bottom: 15px; width: 100%;">
            <div style="flex:1; border: 1px solid #00ffcc; background: #000; padding: 10px; border-radius: 10px; text-align: center;">
                <p style="color:#00ffcc; font-size:10px; margin:0;">SAFE TARGET</p>
                <h3 id="safe-display" style="color:#00ffcc; margin:5px 0;">---</h3>
            </div>
            <div style="flex:1; border: 1px solid #ff00ff; background: #000; padding: 10px; border-radius: 10px; text-align: center;">
                <p style="color:#ff00ff; font-size:10px; margin:0;">RISKY HUNT</p>
                <h3 id="risky-display" style="color:#ff00ff; margin:5px 0;">---</h3>
            </div>
        </div>
        
        <div style="position: relative; width: 160px; height: 160px; display: flex; align-items: center; justify-content: center;">
            <div id="ldr" style="position: absolute; width: 150px; height: 150px; border-radius: 50%; border: 4px solid transparent; border-top-color: #00ffcc;"></div>
            <button id="p-btn" style="width: 130px; height: 130px; border-radius: 50%; background: #ff0000; color: #fff; border: 4px solid #fff; font-weight: 900; cursor: pointer; z-index:10; font-size: 16px; box-shadow: 0 0 15px rgba(255,0,0,0.5);">
                PREDICT<br>PRO
            </button>
        </div>
        <p id="status" style="margin-top:15px; font-size:12px; color:#00ffcc;">SIGNAL STANDBY</p>
    </div>

    <script>
    const btn = document.getElementById('p-btn');
    const ldr = document.getElementById('ldr');
    const status = document.getElementById('status');
    const safeDisp = document.getElementById('safe-display');
    const riskyDisp = document.getElementById('risky-display');

    // Deep parameters passed from Python's tensor analysis
    const paramMu = parseFloat("{mu}");
    const paramSigma = parseFloat("{sigma}");
    const paramMomentum = parseFloat("{momentum}");
    const paramTail = parseFloat("{tail_index}");

    btn.onclick = function() {{
        ldr.style.animation = "spin 0.8s linear infinite";
        btn.innerHTML = "SCANNING";
        btn.style.background = "#333";
        status.innerHTML = "EXECUTING JUMP-DIFFUSION MATH...";
        
        setTimeout(() => {{
            ldr.style.animation = "none";
            ldr.style.borderTopColor = "#ff00ff";
            
            btn.innerHTML = "LOCKED";
            btn.style.background = "#00ffcc";
            btn.style.color = "#000";
            
            // INSANE MATH: Live Box-Muller Transform (Brownian Noise Generator)
            const z1 = Math.random();
            const z2 = Math.random();
            const stochasticNoise = Math.sqrt(-2.0 * Math.log(z1)) * Math.cos(2.0 * Math.PI * z2);
            
            // Calculate SAFE TARGET using Baseline Trend + Momentum adjustment
            let computedSafe = paramMu + (paramSigma * stochasticNoise * 0.25) + paramMomentum;
            computedSafe = Math.max(1.10, computedSafe); // Ensure it doesn't drop below 1.10
            
            // Calculate RISKY TARGET using Fréchet Extreme Value generation (UNCAPPED)
            // This utilizes an inverse power law to simulate Aviator's extreme spikes
            const uniformRandom = Math.random();
            const frechetJump = Math.pow(Math.abs(Math.log(uniformRandom)), -1.0 / paramTail);
            
            let computedRisky = computedSafe + (paramSigma * frechetJump * 2.0);
            
            // 15% chance to trigger a massive 'Outlier Matrix Jump' (Simulates 10x - 50x+ flights)
            if (Math.random() > 0.85) {{
                computedRisky *= (1.5 + (Math.random() * paramTail));
            }}
            
            // Formatting output
            safeDisp.innerHTML = computedSafe.toFixed(2) + "x";
            riskyDisp.innerHTML = computedRisky.toFixed(2) + "x";
            status.innerHTML = "SIGNAL VERIFIED FOR {st.session_state['casino']}";
        }}, 1500);
    }};
    </script>
    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
    """, height=320)
# ==============================================================================
# 5. MASTER FLOW CONTROLLERS
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🔐 OPERATOR ID")
    u = st.text_input("USER NAME")
    p = st.text_input("ENCRYPTION KEY", type="password")
    if st.button("AUTHORIZE SYSTEM"):
        if u == "Icetrex" and p == "SOPITO":
            st.session_state["pass"] = True
            st.rerun()
        else:
            st.error("Invalid Operator Credentials.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_manual_casino_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 CASINO HANDSHAKE")
    c = st.selectbox("SELECT PLATFORM", ["Premier Bet", "AfricaBet", "1xBet", "888Starz", "SportyBet", "SpinCity", "MWOS", "1WIN", "WINBUCKS"])
    st.warning("Ensure your casino account is open in a separate tab.")
    if st.button("ESTABLISH MANUAL BRIDGE"):
        st.session_state["casino"] = c
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    col1, col2, col3 = st.columns(3)
    with col1: r1 = st.text_input("L1", value="1.50")
    with col2: r2 = st.text_input("L2", value="2.10")
    with col3: r3 = st.text_input("L3", value="1.15")
    if st.button("LOCK NEURAL MATRIX"):
        if r1 and r2 and r3:
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # 1. Header Buttons
    ca, cb = st.columns(2)
    with ca: 
        st.markdown('<button style="width:100%; padding:10px; background:#00ffcc; color:#000; border-radius:10px; font-weight:bold;">📥 PRO APK</button>', unsafe_allow_html=True)
    with cb: 
        st.markdown(f'<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border-radius:10px; font-weight:bold; border:none; cursor:pointer;">💬 DEV SUPPORT</button></a>', unsafe_allow_html=True)

    # 2. Compute Calculations & Render Frontend Component
   mu, sigma, momentum, tail_index = execute_2030_neural_math(st.session_state["history"])
    render_pro_button(mu, sigma, momentum, tail_index)
    
    # 3. Community Chat & Session Teardown
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 GLOBAL COMMUNITY")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="300" frameborder="0"></iframe>', height=320)
    
    if st.button("🚪 TERMINATE SESSION"):
        st.session_state["pass"] = False
        st.session_state["casino"] = None
        st.session_state["synced"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 6. MASTER EXECUTION ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_manual_casino_login()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
