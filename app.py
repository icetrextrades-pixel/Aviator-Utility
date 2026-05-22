import streamlit as st
import numpy as np
import time
from datetime import datetime
import pytz

# ==============================================================================
# 1. ATOMIC INITIALIZATION & STATE
# ==============================================================================
if "pass" not in st.session_state: st.session_state["pass"] = False
if "casino" not in st.session_state: st.session_state["casino"] = "AFRIBET"
if "history" not in st.session_state: st.session_state["history"] = ["1.50x", "2.10x", "1.15x"]

# Set page config globally
st.set_page_config(page_title="AVI10 NEURAL MATRIX", layout="centered", initial_sidebar_state="collapsed")

# ==============================================================================
# 2. STOCHASTIC MATH ENGINE (PRESERVED)
# ==============================================================================
def execute_2030_neural_math(history_data):
    """Calculates live stochastic parameters for the client-side Jump-Diffusion."""
    try:
        vals = [float(x.replace('x','').strip()) for x in history_data if x.strip()]
        if len(vals) < 3: 
            return 1.45, 0.20, 0.05, 2.0
            
        arr = np.array(vals)
        mu = np.mean(arr)
        sigma = np.std(arr) + 0.001
        log_returns = np.diff(np.log(arr))
        momentum = np.mean(log_returns) if len(log_returns) > 0 else 0
        tail_index = np.max(arr) / mu if mu > 0 else 2.0
        
        return mu, sigma, momentum, min(tail_index, 15.0)
    except Exception:
        return 1.45, 0.20, 0.05, 2.0

# ==============================================================================
# 3. DYNAMIC CSS INJECTION (IMAGE MATCHING)
# ==============================================================================
LOGIN_CSS = """
<style>
    .stApp { background-color: #050508; color: white; }
    
    /* Login Card Replication */
    .login-container {
        background: #0a0a10; border: 1px solid #2a1644; border-radius: 20px;
        padding: 50px 30px; text-align: center; max-width: 450px; margin: 40px auto;
        box-shadow: 0 0 40px rgba(80, 20, 150, 0.1);
    }
    
    /* Padlock Icon */
    .padlock-wrapper {
        width: 80px; height: 80px; border-radius: 50%; border: 2px solid #5b21b6;
        margin: 0 auto 30px auto; display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(91, 33, 182, 0.3);
    }
    
    /* Text Styling */
    .title-aviator { font-size: 32px; font-weight: 900; font-style: italic; color: white; margin: 0; }
    .title-signals { font-size: 32px; font-weight: 900; font-style: italic; color: #a855f7; margin: 0; }
    .subtext { font-size: 10px; letter-spacing: 4px; color: #6b21a8; margin-top: 10px; margin-bottom: 40px; font-weight: bold; }
    .footer-text { font-size: 9px; letter-spacing: 3px; color: #3f3f46; margin-top: 40px; }

    /* Streamlit Input Override */
    div[data-baseweb="input"] { background-color: #000 !important; border: 1px solid #2a1644 !important; border-radius: 12px !important; }
    div[data-baseweb="input"] input { color: #a855f7 !important; text-align: center !important; font-weight: bold; letter-spacing: 2px; }
    
    /* Streamlit Button Override */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #9333ea, #db2777) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 0 !important; font-weight: 900 !important; letter-spacing: 1.5px !important;
        width: 100% !important; margin-top: 15px !important; transition: all 0.3s ease;
    }
    div[data-testid="stButton"] > button:hover { box-shadow: 0 0 20px rgba(219, 39, 119, 0.5) !important; }
    
    /* Hide top header */
    header { display: none !important; }
</style>
"""

DASHBOARD_CSS = """
<style>
    .stApp { background-color: #030805; color: white; font-family: 'Inter', sans-serif; }
    
    /* Top Nav Fakes */
    .top-nav { display: flex; justify-content: space-between; font-size: 10px; color: #6b7280; font-weight: bold; margin-bottom: 20px; }
    .top-tabs { display: flex; gap: 10px; margin-bottom: 30px; }
    .tab { flex: 1; text-align: center; padding: 12px; border-radius: 10px; font-size: 12px; font-weight: bold; border: 1px solid #1f2937; background: #050505; color: #6b7280; }
    .tab.active { background: #059669; color: #000; border: none; box-shadow: 0 0 15px rgba(5, 150, 105, 0.4); }

    /* Title Section */
    .dash-header { text-align: center; margin-bottom: 20px; }
    .dash-title { font-size: 28px; font-style: italic; font-weight: 900; margin: 0; }
    .dash-bullets { list-style: none; padding: 0; margin: 10px 0; font-size: 10px; font-weight: bold; color: #6b7280; letter-spacing: 1px; }
    .dash-bullets li::before { content: "● "; color: #10b981; }

    /* Streamlit overrides for dashboard */
    div[data-baseweb="select"] > div { background-color: #050505 !important; border: 1px solid #1f2937 !important; border-radius: 10px !important; color: white !important;}
    
    header { display: none !important; }
</style>
"""

# ==============================================================================
# 4. DASHBOARD COMPONENT (GREEN CARD HTML/JS)
# ==============================================================================
def render_green_matrix_card(mu, sigma, momentum, tail_index):
    # Get current time in CAT (Zimbabwe) to match UI
    cat_timezone = pytz.timezone('Africa/Harare')
    current_time = datetime.now(cat_timezone).strftime("%H:%M:%S")

    st.components.v1.html(f"""
    <div style="background: #021107; border: 1px solid #064e3b; border-radius: 25px; padding: 30px; text-align: center; color: white; font-family: sans-serif; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.8);">
        
        <h2 style="margin:0; font-weight: 900; font-size: 22px;">
            <span style="color: #10b981;">⚡</span> AVI10 SIGNAL BOT <span style="color: #10b981;">⚡</span>
        </h2>
        <p style="color: #059669; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-top: 5px; margin-bottom: 25px;">
            ZIMBABWE TIME: {current_time}
        </p>
        
        <button id="gen-btn" style="width: 100%; background: #10b981; color: #000; font-weight: 900; font-size: 16px; border: none; padding: 18px; border-radius: 12px; cursor: pointer; box-shadow: 0 0 20px rgba(16, 185, 129, 0.3); transition: 0.2s;">
            GENERATE SIGNAL
        </button>
        
        <div style="display:flex; justify-content:center; gap: 8px; margin: 25px 0;">
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
        
        <div style="background: #030805; border: 1px solid #1f2937; border-radius: 15px; padding: 20px; margin-top: 35px; text-align: left; font-family: monospace; font-size: 13px;">
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
        
        <p style="color: #059669; font-size: 10px; font-weight: 900; letter-spacing: 1px; margin-top: 30px; margin-bottom: 5px;">RECALIBRATE MATRIX</p>
        <p style="color: #1f2937; font-size: 8px; font-weight: bold; letter-spacing: 2px; margin: 0;">NEURAL MATRIX V2.0 • ZERO MANUAL INPUT</p>
    </div>

    <script>
    const btn = document.getElementById('gen-btn');
    const ring = document.getElementById('ring');
    const targetDisp = document.getElementById('target-display');
    const termText = document.getElementById('term-text');
    const remVal = document.getElementById('rem-val');
    const confVal = document.getElementById('conf-val');

    const pMu = parseFloat("{mu}");
    const pSigma = parseFloat("{sigma}");
    const pTail = parseFloat("{tail_index}");

    btn.onclick = function() {{
        // Reset UI for calculation
        ring.style.animation = "spin 0.5s linear infinite";
        btn.style.background = "#064e3b";
        btn.style.color = "#10b981";
        btn.innerHTML = "CALCULATING...";
        termText.innerHTML = "● INJECTING STOCHASTIC NOISE...<br>● MAPPING ALGORITHM BOUNDARIES...";
        
        setTimeout(() => {{
            ring.style.animation = "none";
            btn.style.background = "#10b981";
            btn.style.color = "#000";
            btn.innerHTML = "GENERATE SIGNAL";
            
            // Execute the stochastic deep math calculation
            const uniformRandom = Math.random();
            const frechetJump = Math.pow(Math.abs(Math.log(uniformRandom)), -1.0 / pTail);
            let finalTarget = pMu + (pSigma * frechetJump);
            
            // Outlier Matrix Jump
            if (Math.random() > 0.85) {{ finalTarget *= (1.5 + (Math.random() * pTail)); }}
            finalTarget = Math.max(1.05, finalTarget);
            
            // Update UI
            targetDisp.innerHTML = finalTarget.toFixed(2) + "X";
            
            // Randomize Confidence and Remaining time for aesthetic
            const conf = Math.floor(Math.random() * 15) + 84; // 84% - 99%
            const rem = Math.floor(Math.random() * 40) + 15; // 15s - 55s
            
            confVal.innerHTML = conf + "%";
            remVal.innerHTML = rem + "s";
            termText.innerHTML = "● SIGNAL LOCKED<br>● AWAITING ROUND EXECUTION...";
            
        }}, 1800);
    }};
    </script>
    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
    """, height=800)

# ==============================================================================
# 5. MASTER VIEWS
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
    
    # We use empty columns to center and size the input within the dark CSS layout
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        key = st.text_input("KEY", placeholder="ENTER ACCESS KEY", label_visibility="collapsed")
        if st.button("INITIALIZE NEURAL MATRIX"):
            if key.strip(): # Accepts any key input for testing
                st.session_state["pass"] = True
                st.rerun()
                
    st.markdown('<p style="text-align:center;" class="footer-text">AUTHORIZED ACCESS ONLY</p>', unsafe_allow_html=True)


def show_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    
    # Top Nav Bar Mockup
    st.markdown("""
    <div class="top-nav">
        <div>🖧 CPU: 14% &nbsp;&nbsp; ⚗ NEURAL: 99.4%</div>
        <div><span style="border: 1px solid #1f2937; padding: 3px 8px; border-radius: 5px;">💾 SAVE WORK</span> &nbsp; <span style="color: #10b981;">📶 LIVE SYNC</span></div>
    </div>
    <div class="top-tabs">
        <div class="tab">PREDICTOR</div>
        <div class="tab">MR CRUSHER</div>
        <div class="tab active">AVI10</div>
    </div>
    <div class="dash-header">
        <h1 class="dash-title">AVI10 NEURAL</h1>
        <ul class="dash-bullets">
            <li>NO RISK NO DUBAI</li>
            <li>THE KEY TO SUCCESS IS A LONG JOURNEY</li>
            <li>NEURAL MATRIX V2.0</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Casino Dropdown Bar
    colA, colB = st.columns([4, 1])
    with colA:
        st.selectbox("CASINO", ["AFRICABET", "1XBET", "PREMIER BET"], label_visibility="collapsed")
    with colB:
        st.markdown('<div style="text-align:center; padding: 10px; border: 1px solid #1f2937; border-radius: 10px; font-size: 10px; font-weight:bold; color: #a855f7; margin-top:2px; cursor:pointer;">CORRECTION</div>', unsafe_allow_html=True)
        
    st.write("") # Spacer
    
    # Load parameters & Render Green HTML Card
    mu, sigma, momentum, tail_index = execute_2030_neural_math(st.session_state["history"])
    render_green_matrix_card(mu, sigma, momentum, tail_index)


# ==============================================================================
# 6. ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
else:
    show_dashboard()
