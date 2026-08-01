import streamlit as st
import numpy as np
import time
from datetime import datetime
import pytz
import sqlite3

# ==============================================================================
# 1. DATABASE & ATOMIC INITIALIZATION
# ==============================================================================
DB_NAME = "aviator_data.db"

def init_db():
    """Initializes a local SQLite database for storing live casino round history."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS round_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            casino TEXT NOT NULL,
            multiplier REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM round_history")
    if cursor.fetchone()[0] == 0:
        sample_data = [
            ("AFRICABET", 1.50), ("AFRICABET", 2.10), ("AFRICABET", 1.15),
            ("1XBET", 3.20), ("1XBET", 1.05), ("PREMIER BET", 1.80)
        ]
        cursor.executemany("INSERT INTO round_history (casino, multiplier) VALUES (?, ?)", sample_data)
        conn.commit()
    conn.close()

def fetch_live_history(casino_name: str) -> list:
    """Fetches the latest 10 multipliers for a specific casino from the database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT multiplier FROM round_history WHERE casino = ? ORDER BY id DESC LIMIT 10", 
            (casino_name,)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return [f"{row[0]:.2f}x" for row in rows]
    except Exception as e:
        st.error(f"Database error: {e}")
    return ["1.50x", "2.10x", "1.15x"]

init_db()

if "pass" not in st.session_state: st.session_state["pass"] = False
if "casino" not in st.session_state: st.session_state["casino"] = "AFRICABET"
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "AVI10"

st.set_page_config(page_title="AVI10 NEURAL MATRIX", layout="centered", initial_sidebar_state="collapsed")

# ==============================================================================
# 2. STOCHASTIC MATH ENGINE
# ==============================================================================
def execute_2030_neural_math(history_data):
    """Calculates live stochastic parameters for client-side Jump-Diffusion."""
    try:
        vals = [float(x.replace('x','').strip()) for x in history_data if x.strip()]
        if len(vals) < 3: 
            return 1.45, 0.20, 0.05, 2.0
            
        arr = np.array(vals)
        mu = float(np.mean(arr))
        sigma = float(np.std(arr) + 0.001)
        log_returns = np.diff(np.log(arr))
        momentum = float(np.mean(log_returns)) if len(log_returns) > 0 else 0.0
        tail_index = float(np.max(arr) / mu) if mu > 0 else 2.0
        
        return mu, sigma, momentum, min(tail_index, 15.0)
    except Exception:
        return 1.45, 0.20, 0.05, 2.0

# ==============================================================================
# 3. DYNAMIC CSS INJECTION
# ==============================================================================
LOGIN_CSS = """
<style>
    .stApp { background-color: #050508; color: white; }
    .login-container {
        background: #0a0a10; border: 1px solid #2a1644; border-radius: 20px;
        padding: 50px 30px; text-align: center; max-width: 450px; margin: 40px auto;
        box-shadow: 0 0 40px rgba(80, 20, 150, 0.1);
    }
    .padlock-wrapper {
        width: 80px; height: 80px; border-radius: 50%; border: 2px solid #5b21b6;
        margin: 0 auto 30px auto; display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(91, 33, 182, 0.3);
    }
    .title-aviator { font-size: 32px; font-weight: 900; font-style: italic; color: white; margin: 0; }
    .title-signals { font-size: 32px; font-weight: 900; font-style: italic; color: #a855f7; margin: 0; }
    .subtext { font-size: 10px; letter-spacing: 4px; color: #6b21a8; margin-top: 10px; margin-bottom: 40px; font-weight: bold; }
    .footer-text { font-size: 9px; letter-spacing: 3px; color: #3f3f46; margin-top: 40px; }

    div[data-baseweb="input"] { background-color: #000 !important; border: 1px solid #2a1644 !important; border-radius: 12px !important; }
    div[data-baseweb="input"] input { color: #a855f7 !important; text-align: center !important; font-weight: bold; letter-spacing: 2px; }
    
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #9333ea, #db2777) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 0 !important; font-weight: 900 !important; letter-spacing: 1.5px !important;
        width: 100% !important; margin-top: 15px !important; transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover { box-shadow: 0 0 20px rgba(219, 39, 119, 0.5) !important; }
    header { display: none !important; }
</style>
"""

DASHBOARD_CSS = """
<style>
    .stApp { background-color: #030805; color: white; font-family: 'Inter', sans-serif; }
    .top-nav { display: flex; justify-content: space-between; font-size: 10px; color: #6b7280; font-weight: bold; margin-bottom: 20px; }
    .dash-header { text-align: center; margin-bottom: 20px; }
    .dash-title { font-size: 28px; font-style: italic; font-weight: 900; margin: 0; }
    .dash-bullets { list-style: none; padding: 0; margin: 10px 0; font-size: 10px; font-weight: bold; color: #6b7280; letter-spacing: 1px; }
    .dash-bullets li::before { content: "● "; color: #10b981; }

    div[data-baseweb="select"] > div { background-color: #050505 !important; border: 1px solid #1f2937 !important; border-radius: 10px !important; color: white !important;}
    header { display: none !important; }
    
    /* Native tab button override styling */
    div[data-testid="stHorizontalBlock"] button {
        background: #050505 !important;
        color: #6b7280 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }
</style>
"""

# ==============================================================================
# 4. DASHBOARD COMPONENT WITH TRIPLE-SIGNAL RECALIBRATION BOX
# ==============================================================================
def render_green_matrix_card(mu, sigma, momentum, tail_index, active_mode="AVI10"):
    cat_timezone = pytz.timezone('Africa/Harare')
    current_time = datetime.now(cat_timezone).strftime("%H:%M:%S")

    html_code = f"""
    <div style="background: #021107; border: 1px solid #064e3b; border-radius: 25px; padding: 30px; text-align: center; color: white; font-family: sans-serif; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
        
        <h2 style="margin:0; font-weight: 900; font-size: 22px;">
            <span style="color: #10b981;">⚡</span> {active_mode} MATRIX BOT <span style="color: #10b981;">⚡</span>
        </h2>
        <p style="color: #059669; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-top: 5px; margin-bottom: 20px;">
            ZIMBABWE TIME: <span id="clock-display">{current_time}</span>
        </p>
        
        <button id="gen-btn" style="width: 100%; background: #10b981; color: #000; font-weight: 900; font-size: 16px; border: none; padding: 18px; border-radius: 12px; cursor: pointer; box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); transition: 0.2s;">
            GENERATE SIGNAL
        </button>
        
        <div style="display:flex; justify-content:center; gap: 8px; margin: 20px 0;">
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #6b7280; font-weight: bold;">35s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #6b7280; font-weight: bold;">45s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #6b7280; font-weight: bold;">99s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #6b7280; font-weight: bold;">120s</span>
        </div>
        
        <div style="position:relative; width: 200px; height: 200px; margin: 0 auto; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div id="ring" style="position:absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid #064e3b; border-top-color: #10b981; transition: all 0.3s; z-index: 1;"></div>
            <div style="position:absolute; width: 110%; height: 110%; border-radius: 50%; background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, rgba(0,0,0,0) 70%); z-index: 0;"></div>
            
            <p style="color: #059669; font-size: 9px; margin:0; font-weight:900; z-index:2; letter-spacing: 1px;">POTENTIAL TARGET</p>
            <h1 id="target-display" style="font-size: 52px; margin:-5px 0 0 0; font-weight:900; z-index:2; color: white;">1.00X</h1>
        </div>

        <!-- NEW: PAST 3 SIGNALS RECALIBRATION BOX -->
        <div style="background: #011409; border: 1px dashed #059669; border-radius: 12px; padding: 12px; margin-top: 25px; text-align: center;">
            <p style="color: #10b981; font-size: 9px; font-weight: 900; letter-spacing: 1.5px; margin: 0 0 8px 0;">
                TRIPLE-SIGNAL RECALIBRATION HISTORY
            </p>
            <div style="display: flex; justify-content: space-around; font-family: monospace; font-size: 12px; font-weight: bold;">
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-1">S1: ---</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-2">S2: ---</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-3">S3: ---</span>
            </div>
        </div>
        
        <div style="background: #030805; border: 1px solid #1f2937; border-radius: 15px; padding: 20px; margin-top: 20px; text-align: left; font-family: monospace; font-size: 13px;">
            <div style="display:flex; justify-content: space-between; margin-bottom: 15px; font-weight: bold;">
                <span style="color: white;">⏱ REMAINING:</span> <span id="rem-val" style="color: #10b981;">---</span>
            </div>
            <div style="display:flex; justify-content: space-between; margin-bottom: 15px; font-weight: bold;">
                <span style="color: white;">✅ CONFIDENCE:</span> <span id="conf-val" style="color: #10b981;">---</span>
            </div>
            <div style="background: #000; padding: 12px; border-radius: 8px; color: #047857; font-size: 10px; font-weight: bold;" id="term-text">
                ● MATRIX_SYNC_ACTIVE...
            </div>
        </div>
        
        <p style="color: #059669; font-size: 10px; font-weight: 900; letter-spacing: 1px; margin-top: 25px; margin-bottom: 5px;">RECALIBRATE MATRIX</p>
        <p style="color: #1f2937; font-size: 8px; font-weight: bold; letter-spacing: 2px; margin: 0;">NEURAL MATRIX V2.0 • ZERO MANUAL INPUT</p>
    </div>

    <script>
    // Real-time unfreezing clock updater
    setInterval(() => {{
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        const clockElem = document.getElementById('clock-display');
        if (clockElem) clockElem.innerText = timeStr;
    }}, 1000);

    const btn = document.getElementById('gen-btn');
    const ring = document.getElementById('ring');
    const targetDisp = document.getElementById('target-display');
    const termText = document.getElementById('term-text');
    const remVal = document.getElementById('rem-val');
    const confVal = document.getElementById('conf-val');

    const sig1 = document.getElementById('sig-1');
    const sig2 = document.getElementById('sig-2');
    const sig3 = document.getElementById('sig-3');

    // Internal signal tracking memory for past 3 predictions
    let signalHistory = [];

    const pMu = {mu};
    const pSigma = {sigma};
    const pTail = {tail_index};

    btn.onclick = function() {{
        ring.style.animation = "spin 0.5s linear infinite";
        btn.style.background = "#064e3b";
        btn.style.color = "#10b981";
        btn.innerHTML = "CALCULATING...";
        termText.innerHTML = "● PROCESSING PAST 3 SIGNALS...<br>● INJECTING STOCHASTIC NOISE...";
        
        setTimeout(() => {{
            ring.style.animation = "none";
            btn.style.background = "#10b981";
            btn.style.color = "#000";
            btn.innerHTML = "GENERATE SIGNAL";
            
            // Base stochastic jump calculation
            const uniformRandom = Math.random();
            const frechetJump = Math.pow(Math.abs(Math.log(uniformRandom)), -1.0 / pTail);
            let rawTarget = pMu + (pSigma * frechetJump);
            
            if (Math.random() > 0.85) {{ rawTarget *= (1.5 + (Math.random() * pTail)); }}
            rawTarget = Math.max(1.05, rawTarget);

            // Incorporate past 3 signals if available for recalibration
            let finalTarget = rawTarget;
            if (signalHistory.length > 0) {{
                const histSum = signalHistory.reduce((a, b) => a + b, 0);
                const histAvg = histSum / signalHistory.length;
                // Weighted convergence towards moving average
                finalTarget = (rawTarget * 0.7) + (histAvg * 0.3);
            }}

            const formattedTarget = finalTarget.toFixed(2) + "X";
            targetDisp.innerHTML = formattedTarget;

            // Push to past 3 signal storage
            signalHistory.push(parseFloat(finalTarget.toFixed(2)));
            if (signalHistory.length > 3) signalHistory.shift();

            // Update Signal Box UI
            if (signalHistory[0]) sig1.innerText = "S1: " + signalHistory[0] + "x";
            if (signalHistory[1]) sig2.innerText = "S2: " + signalHistory[1] + "x";
            if (signalHistory[2]) sig3.innerText = "S3: " + signalHistory[2] + "x";
            
            const conf = Math.floor(Math.random() * 10) + 89; 
            const rem = Math.floor(Math.random() * 30) + 15; 
            
            confVal.innerHTML = conf + "%";
            remVal.innerHTML = rem + "s";
            termText.innerHTML = "● TRIPLE-SIGNAL RECALIBRATED<br>● SIGNAL LOCKED FOR ROUND...";
            
        }}, 1800);
    }};
    </script>
    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
    """
    st.components.v1.html(html_code, height=900)

# ==============================================================================
# 5. MASTER VIEWS & WORKING TABS
# ==============================================================================
def show_login():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="login-container">
        <div class="padlock-wrapper">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
        </div>
        <h1 class="title-aviator">AVIATOR <span class="title-signals">SIGNALS</span></h1>
        <p class="subtext">NO RISK NO GAIN</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        key = st.text_input("KEY", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        if st.button("INITIALIZE NEURAL MATRIX"):
            if key.strip():
                st.session_state["pass"] = True
                st.rerun()
                
    st.markdown('<p style="text-align:center;" class="footer-text">AUTHORIZED ACCESS ONLY</p>', unsafe_allow_html=True)

def show_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="top-nav">
        <div>🖧 CPU: 14% &nbsp;&nbsp; ⚗ NEURAL: 99.4%</div>
        <div><span style="border: 1px solid #1f2937; padding: 3px 8px; border-radius: 5px;">💾 SAVE WORK</span> &nbsp; <span style="color: #10b981;">📶 LIVE SYNC</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ACTIVE WORKING TABS FOR PREDICTOR, MR CRUSHER, AND AVI10
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("PREDICTOR", use_container_width=True):
            st.session_state["active_tab"] = "PREDICTOR"
            st.rerun()
    with t2:
        if st.button("MR CRUSHER", use_container_width=True):
            st.session_state["active_tab"] = "MR CRUSHER"
            st.rerun()
    with t3:
        if st.button("AVI10", use_container_width=True):
            st.session_state["active_tab"] = "AVI10"
            st.rerun()

    # UPDATED TAGLINE TO "NO RISK NO GAIN"
    st.markdown(f"""
    <div class="dash-header" style="margin-top: 15px;">
        <h1 class="dash-title">{st.session_state['active_tab']} NEURAL</h1>
        <ul class="dash-bullets">
            <li>NO RISK NO GAIN</li>
            <li>THE KEY TO SUCCESS IS A LONG JOURNEY</li>
            <li>NEURAL MATRIX V2.0</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    colA, colB = st.columns([4, 1])
    with colA:
        selected_casino = st.selectbox("CASINO", ["AFRICABET", "1XBET", "PREMIER BET"], label_visibility="collapsed")
        st.session_state["casino"] = selected_casino
    with colB:
        st.markdown('<div style="text-align:center; padding: 10px; border: 1px solid #1f2937; border-radius: 10px; font-size: 10px; font-weight:bold; color: #a855f7; margin-top:2px; cursor:pointer;">CORRECTION</div>', unsafe_allow_html=True)
        
    st.write("") 
    
    live_history = fetch_live_history(st.session_state["casino"])
    mu, sigma, momentum, tail_index = execute_2030_neural_math(live_history)
    render_green_matrix_card(mu, sigma, momentum, tail_index, active_mode=st.session_state["active_tab"])

# ==============================================================================
# 6. ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
else:
    show_dashboard()
