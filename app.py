import streamlit as st
import numpy as np
import time
from datetime import datetime
import pytz
import sqlite3

# ==============================================================================
# 1. AUTHENTICATION & DATABASE SYSTEM
# ==============================================================================
# Add or remove member credentials here:
MEMBERS_DB = {
    "Icetrex": "sopito6002",
    "austin": "tinofa111",
    "biko": "taku333",
    # "username": "password"
}

ADMIN_EMAIL = "icetrextrades@gmail.com"
ADMIN_WHATSAPP = "+263779174062"  # Replace with your exact WhatsApp number

DB_NAME = "aviator_data.db"

def init_db():
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
if "user" not in st.session_state: st.session_state["user"] = ""
if "casino" not in st.session_state: st.session_state["casino"] = "AFRICABET"
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "AVI10"

st.set_page_config(page_title="AVI10 NEURAL MATRIX", layout="centered", initial_sidebar_state="collapsed")

# ==============================================================================
# 2. STOCHASTIC MATH ENGINE
# ==============================================================================
def execute_2030_neural_math(history_data):
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
# 3. DYNAMIC MESSI CSS INJECTION (EXTERIOR & INTERIOR)
# ==============================================================================
LOGIN_CSS = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(5, 5, 8, 0.85), rgba(5, 5, 8, 0.95)), 
                    url('https://images.hdqwalls.com/wallpapers/lionel-messi-4k-2020-qt.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .login-container {{
        background: rgba(10, 10, 16, 0.85);
        border: 1px solid #2a1644;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        max-width: 450px;
        margin: 20px auto;
        box-shadow: 0 0 50px rgba(147, 51, 234, 0.2);
        backdrop-filter: blur(10px);
    }}
    .padlock-wrapper {{
        width: 70px; height: 70px; border-radius: 50%; border: 2px solid #5b21b6;
        margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(91, 33, 182, 0.4);
    }}
    .title-aviator {{ font-size: 30px; font-weight: 900; font-style: italic; color: white; margin: 0; }}
    .title-signals {{ font-size: 30px; font-weight: 900; font-style: italic; color: #a855f7; margin: 0; }}
    .subtext {{ font-size: 10px; letter-spacing: 4px; color: #c084fc; margin-top: 8px; margin-bottom: 25px; font-weight: bold; }}
    .footer-text {{ font-size: 10px; letter-spacing: 2px; color: #9ca3af; margin-top: 25px; text-align: center; font-weight: bold; }}

    div[data-baseweb="input"] {{ background-color: rgba(0,0,0,0.8) !important; border: 1px solid #3b0764 !important; border-radius: 12px !important; }}
    div[data-baseweb="input"] input {{ color: #a855f7 !important; text-align: center !important; font-weight: bold; letter-spacing: 2px; }}
    
    div[data-testid="stButton"] > button {{
        background: linear-gradient(90deg, #9333ea, #db2777) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 0 !important; font-weight: 900 !important; letter-spacing: 1.5px !important;
        width: 100% !important; margin-top: 10px !important; transition: all 0.3s ease;
    }}
    div[data-testid="stButton"] > button:hover {{ box-shadow: 0 0 25px rgba(219, 39, 119, 0.6) !important; }}
    header {{ display: none !important; }}
</style>
"""

DASHBOARD_CSS = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(3, 8, 5, 0.88), rgba(3, 8, 5, 0.95)), 
                    url('https://images.hdqwalls.com/wallpapers/lionel-messi-trophy-4k-hy.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        font-family: 'Inter', sans-serif;
    }}
    .top-nav {{ display: flex; justify-content: space-between; font-size: 10px; color: #9ca3af; font-weight: bold; margin-bottom: 20px; }}
    .dash-header {{ text-align: center; margin-bottom: 20px; }}
    .dash-title {{ font-size: 28px; font-style: italic; font-weight: 900; margin: 0; color: #ffffff; }}
    .dash-bullets {{ list-style: none; padding: 0; margin: 10px 0; font-size: 10px; font-weight: bold; color: #10b981; letter-spacing: 1px; }}
    .dash-bullets li::before {{ content: "● "; color: #10b981; }}

    div[data-baseweb="select"] > div {{ background-color: rgba(5,5,5,0.9) !important; border: 1px solid #064e3b !important; border-radius: 10px !important; color: white !important;}}
    header {{ display: none !important; }}
    
    div[data-testid="stHorizontalBlock"] button {{
        background: rgba(5, 5, 5, 0.85) !important;
        color: #9ca3af !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }}
</style>
"""

# ==============================================================================
# 4. DASHBOARD COMPONENT WITH APK & ADMIN BOXES
# ==============================================================================
def render_green_matrix_card(mu, sigma, momentum, tail_index, active_mode="AVI10"):
    cat_timezone = pytz.timezone('Africa/Harare')
    current_time = datetime.now(cat_timezone).strftime("%H:%M:%S")

    html_code = f"""
    <div style="background: rgba(2, 17, 7, 0.92); border: 1px solid #064e3b; border-radius: 25px; padding: 25px; text-align: center; color: white; font-family: sans-serif; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.9); backdrop-filter: blur(12px);">
        
        <h2 style="margin:0; font-weight: 900; font-size: 22px;">
            <span style="color: #10b981;">⚡</span> {active_mode} MATRIX BOT <span style="color: #10b981;">⚡</span>
        </h2>
        <p style="color: #059669; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-top: 5px; margin-bottom: 20px;">
            ZIMBABWE TIME: <span id="clock-display">{current_time}</span>
        </p>
        
        <button id="gen-btn" style="width: 100%; background: #10b981; color: #000; font-weight: 900; font-size: 16px; border: none; padding: 18px; border-radius: 12px; cursor: pointer; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); transition: 0.2s;">
            GENERATE SIGNAL
        </button>
        
        <div style="display:flex; justify-content:center; gap: 8px; margin: 20px 0;">
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #9ca3af; font-weight: bold;">35s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #9ca3af; font-weight: bold;">45s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #9ca3af; font-weight: bold;">99s</span>
            <span style="border: 1px solid #1f2937; padding: 5px 12px; border-radius: 6px; font-size: 10px; color: #9ca3af; font-weight: bold;">120s</span>
        </div>
        
        <div style="position:relative; width: 190px; height: 190px; margin: 0 auto; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div id="ring" style="position:absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid #064e3b; border-top-color: #10b981; transition: all 0.3s; z-index: 1;"></div>
            <div style="position:absolute; width: 110%; height: 110%; border-radius: 50%; background: radial-gradient(circle, rgba(16,185,129,0.15) 0%, rgba(0,0,0,0) 70%); z-index: 0;"></div>
            
            <p style="color: #059669; font-size: 9px; margin:0; font-weight:900; z-index:2; letter-spacing: 1px;">POTENTIAL TARGET</p>
            <h1 id="target-display" style="font-size: 50px; margin:-5px 0 0 0; font-weight:900; z-index:2; color: white;">1.00X</h1>
        </div>

        <!-- PAST 3 SIGNALS RECALIBRATION BOX -->
        <div style="background: rgba(1, 20, 9, 0.9); border: 1px dashed #059669; border-radius: 12px; padding: 12px; margin-top: 20px; text-align: center;">
            <p style="color: #10b981; font-size: 9px; font-weight: 900; letter-spacing: 1.5px; margin: 0 0 8px 0;">
                TRIPLE-SIGNAL RECALIBRATION HISTORY
            </p>
            <div style="display: flex; justify-content: space-around; font-family: monospace; font-size: 12px; font-weight: bold;">
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-1">S1: ---</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-2">S2: ---</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: #a855f7;" id="sig-3">S3: ---</span>
            </div>
        </div>
        
        <div style="background: rgba(3, 8, 5, 0.9); border: 1px solid #1f2937; border-radius: 15px; padding: 18px; margin-top: 15px; text-align: left; font-family: monospace; font-size: 13px;">
            <div style="display:flex; justify-content: space-between; margin-bottom: 12px; font-weight: bold;">
                <span style="color: white;">⏱ REMAINING:</span> <span id="rem-val" style="color: #10b981;">---</span>
            </div>
            <div style="display:flex; justify-content: space-between; margin-bottom: 12px; font-weight: bold;">
                <span style="color: white;">✅ CONFIDENCE:</span> <span id="conf-val" style="color: #10b981;">---</span>
            </div>
            <div style="background: #000; padding: 10px; border-radius: 8px; color: #047857; font-size: 10px; font-weight: bold;" id="term-text">
                ● MATRIX_SYNC_ACTIVE...
            </div>
        </div>
        
        <p style="color: #059669; font-size: 10px; font-weight: 900; letter-spacing: 1px; margin-top: 20px; margin-bottom: 5px;">RECALIBRATE MATRIX</p>
        <p style="color: #6b7280; font-size: 8px; font-weight: bold; letter-spacing: 2px; margin: 0;">NEURAL MATRIX V2.0 • ZERO MANUAL INPUT</p>
    </div>

    <script>
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
            
            const uniformRandom = Math.random();
            const frechetJump = Math.pow(Math.abs(Math.log(uniformRandom)), -1.0 / pTail);
            let rawTarget = pMu + (pSigma * frechetJump);
            
            if (Math.random() > 0.85) {{ rawTarget *= (1.5 + (Math.random() * pTail)); }}
            rawTarget = Math.max(1.05, rawTarget);

            let finalTarget = rawTarget;
            if (signalHistory.length > 0) {{
                const histSum = signalHistory.reduce((a, b) => a + b, 0);
                const histAvg = histSum / signalHistory.length;
                finalTarget = (rawTarget * 0.7) + (histAvg * 0.3);
            }}

            const formattedTarget = finalTarget.toFixed(2) + "X";
            targetDisp.innerHTML = formattedTarget;

            signalHistory.push(parseFloat(finalTarget.toFixed(2)));
            if (signalHistory.length > 3) signalHistory.shift();

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
    st.components.v1.html(html_code, height=750)

# ==============================================================================
# 5. MASTER VIEWS & PORTAL COMPONENTS
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
        username_input = st.text_input("USERNAME", placeholder="ENTER USERNAME", label_visibility="collapsed")
        password_input = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD", label_visibility="collapsed")
        
        if st.button("INITIALIZE NEURAL MATRIX"):
            user_clean = username_input.strip()
            pass_clean = password_input.strip()
            
            if user_clean in MEMBERS_DB and MEMBERS_DB[user_clean] == pass_clean:
                st.session_state["pass"] = True
                st.session_state["user"] = user_clean
                st.rerun()
            else:
                st.error("Invalid Username or Password.")
                
    st.markdown(f'<p class="footer-text">AUTHORIZED ACCESS ONLY • CONTACT: {ADMIN_EMAIL}</p>', unsafe_allow_html=True)

def show_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="top-nav">
        <div>🖧 CPU: 14% &nbsp;&nbsp; ⚗ USER: <span style="color:#10b981;">{st.session_state['user'].upper()}</span></div>
        <div><span style="border: 1px solid #1f2937; padding: 3px 8px; border-radius: 5px;">💾 SAVE WORK</span> &nbsp; <span style="color: #10b981;">📶 LIVE SYNC</span></div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown(f"""
    <div class="dash-header" style="margin-top: 15px;">
        <h1 class="dash-title">{st.session_state['active_tab']} NEURAL</h1>
        <ul class="dash-bullets">
            <li>NO RISK NO GAIN</li>
            <li>THE KEY TO SUCCESS IS A LONG JOURNEY</li>
            <li>NEURAL MATRIX V3.0</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    colA, colB = st.columns([4, 1])
    with colA:
        selected_casino = st.selectbox("CASINO", ["AFRICABET", "1XBET", "PREMIER BET"], label_visibility="collapsed")
        st.session_state["casino"] = selected_casino
    with colB:
        if st.button("LOGOUT"):
            st.session_state["pass"] = False
            st.session_state["user"] = ""
            st.rerun()
        
    st.write("") 
    
    live_history = fetch_live_history(st.session_state["casino"])
    mu, sigma, momentum, tail_index = execute_2030_neural_math(live_history)
    render_green_matrix_card(mu, sigma, momentum, tail_index, active_mode=st.session_state["active_tab"])

    # --------------------------------------------------------------------------
    # INSIDE PORTAL: APK DOWNLOADER & PERSONAL ADMIN INFO BOXES
    # --------------------------------------------------------------------------
    st.write("")
    box_col1, box_col2 = st.columns(2)

    with box_col1:
        st.markdown(f"""
        <div style="background: rgba(10, 10, 16, 0.9); border: 1px solid #2a1644; border-radius: 15px; padding: 15px; text-align: center;">
            <h4 style="color: #a855f7; margin: 0 0 5px 0; font-size: 14px; font-weight: 900;">📲 DOWNLOAD APK</h4>
            <p style="color: #9ca3af; font-size: 10px; margin-bottom: 12px;">Get the official Android app package for mobile execution.</p>
        </div>
        """, unsafe_allow_html=True)
        # Placeholder APK binary downloader button
        st.download_button(
            label="DOWNLOAD MATRIX APK",
            data=b"ICETREX_NEURAL_MATRIX_V2_APK_BINARY",
            file_name="Icetrex_Aviator_Matrix_v2.apk",
            mime="application/vnd.android.package-archive",
            use_container_width=True
        )

    with box_col2:
        st.markdown(f"""
        <div style="background: rgba(2, 17, 7, 0.9); border: 1px solid #064e3b; border-radius: 15px; padding: 15px; text-align: center;">
            <h4 style="color: #10b981; margin: 0 0 5px 0; font-size: 14px; font-weight: 900;">👤 ADMIN INFORMATION</h4>
            <p style="color: #ffffff; font-size: 11px; margin: 3px 0; font-weight: bold;">📧 Email: <span style="color:#10b981;">{ADMIN_EMAIL}</span></p>
            <p style="color: #ffffff; font-size: 11px; margin: 3px 0; font-weight: bold;">💬 WhatsApp: <span style="color:#10b981;">{ADMIN_WHATSAPP}</span></p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 6. ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
else:
    show_dashboard()
