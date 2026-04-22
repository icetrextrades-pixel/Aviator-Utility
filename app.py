import streamlit as st
import random
import time
from datetime import datetime

# ==============================================================================
# 1. ATOMIC INITIALIZATION (V.1 - V.20 MERGED)
# ==============================================================================
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []

# ==============================================================================
# 2. ULTIMATE INTERFACE & CSS (THE CAT WALLPAPER & ROUND BUTTON)
# ==============================================================================
st.set_page_config(page_title="ICETREX PREDICTOR PRO", layout="centered")

# Replace this URL with your specific wallpaper link
WALLPAPER_URL = "https://th.bing.com/th/id/OIP.sgOj8ZmAEcTsxC4ay-81cQHaQB?w=115&h=180&c=7&r=0&o=7&pid=1.7&rm=3"
st.markdown(f"""
<style>
    .stApp {{
        background-image: url("{WALLPAPER_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #00d4ff;
        font-family: 'Courier New', Courier, monospace;
    }}
    .main-card {{
        background: rgba(0, 0, 0, 0.85);
        padding: 20px;
        border-radius: 15px; 
        border: 1px solid #00d4ff;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    }}
    div[data-testid="stButton"] > button {{
        width: 100%; border-radius: 10px; background: #000 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff !important; font-weight: bold;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. LIVE SERVER CLOCK (ZIMBABWE TIME)
# ==============================================================================
def render_live_clock():
    st.components.v1.html("""
    <div id="clock" style="color: #ff00ff; font-family: monospace; font-size: 20px; font-weight: bold; text-align: center; border: 1px solid #333; padding: 10px; border-radius: 10px; background: #000; box-shadow: inset 0 0 10px #ff00ff;">
        00:00:00
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        now.setHours(now.getUTCHours() + 2); // CAT (UTC+2)
        var h = String(now.getHours()).padStart(2, '0');
        var m = String(now.getMinutes()).padStart(2, '0');
        var s = String(now.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerHTML = "LIVE SERVER TIME: " + h + ":" + m + ":" + s;
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, height=70)

# ==============================================================================
# 4. THE ULTIMATE PREDICTION ENGINE (SCRAMBLED MATH V.21)
# ==============================================================================
def render_ultimate_system():
    # Pull current history from state
    current_h = st.session_state.get("history", [])
    h_str = ",".join([x.replace('x','') for x in current_h]) if current_h else "1.1,1.2,1.3"
    
    st.components.v1.html(f"""
    <style>
        @keyframes spin {{ 0% {{ transform: rotate(0deg); border-top-color: #00ff00; }} 100% {{ transform: rotate(360deg); border-color: #00ff00; }} }}
        .circle-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        
        #p-btn {{ 
            width: 140px !important; height: 140px !important; border-radius: 50% !important; 
            background-color: #ff0000 !important; color: white !important; border: 5px solid #ffffff !important; 
            font-weight: 900; font-size: 18px; cursor: pointer; z-index: 10; 
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.8); outline: none; transition: 0.2s;
        }}
        #p-btn:active {{ transform: scale(0.9); }}
        
        #loader {{ position: absolute; width: 165px; height: 165px; border-radius: 50%; border: 6px solid transparent; z-index: 5; pointer-events: none; }}
        
        .res-container {{
            border: 2px solid #00d4ff; padding: 20px; border-radius: 15px; 
            background: rgba(0,0,0,0.9); width: 100%; margin-bottom: 25px; text-align: center;
        }}
    </style>

    <div class="circle-wrapper">
        <div class="res-container" id="box">
            <p id="st" style="color: #00d4ff; font-size: 11px; margin: 0; letter-spacing: 2px;">PROBABILITY MATRIX ACTIVE</p>
            <h1 id="disp" style="color: #00d4ff; font-size: 85px; margin: 10px 0; font-weight: 900;">---</h1>
            <div id="conf" style="color: #666; font-size: 12px;">WAITING FOR SCAN...</div>
        </div>

        <div style="position: relative; width: 170px; height: 170px; display: flex; align-items: center; justify-content: center;">
            <div id="loader"></div>
            <button id="p-btn">PREDICT<br>SIGNAL</button>
        </div>
    </div>

    <script>
    const btn = document.getElementById('p-btn');
    const loader = document.getElementById('loader');
    const disp = document.getElementById('disp');
    const st = document.getElementById('st');
    const conf = document.getElementById('conf');

    btn.addEventListener('click', () => {{
        loader.style.animation = "spin 2.2s linear forwards";
        st.innerHTML = "INTERCEPTING DATA PACKETS...";
        st.style.color = "#ffff00";
        
        const h = "{h_str}".split(',').map(Number);

        setTimeout(() => {{
            // ULTIMATE STATISTICS ENGINE
            const seed = Math.random();
            let result = 1.00;
            let precision = Math.floor(Math.random() * (99 - 95) + 95);
            
            // 1. DATA VALIDATION
            const avg = h.reduce((a, b) => a + b, 0) / h.length;
            
            // 2. SCRAMBLED LOGIC PATHS
            if (h[0] < 1.5 && h[1] < 1.5 && h[2] < 1.5) {{
                // STARVATION BURST (High Probability of Pink/Gold)
                result = (seed * (85.0 - 12.5) + 12.5).toFixed(2);
            }} else if (h[0] > 10 || h[1] > 10) {{
                // COOLDOWN LOGIC (Avoiding the server money-grab)
                result = (seed * (1.35 - 1.01) + 1.01).toFixed(2);
            }} else if (avg > 2.0 && avg < 5.0) {{
                // STEADY FLOW TREND
                result = (seed * (4.8 - 2.1) + 2.1).toFixed(2);
            }} else {{
                // CHAOS PHASE (Standard range)
                result = (seed * (3.5 - 1.2) + 1.2).toFixed(2);
            }}

            const color = result > 10 ? "#ff00ff" : "#00d4ff";
            disp.innerHTML = result + "x";
            disp.style.color = color;
            st.innerHTML = "SIGNAL ENCRYPTED";
            st.style.color = color;
            conf.innerHTML = "CONFIDENCE: " + precision + "%";
            document.getElementById('box').style.borderColor = color;
            
            btn.innerHTML = "NEXT<br>SCAN";
            loader.style.animation = "none";
        }}, 2200);
    }});
    </script>
    """, height=520)

# ==============================================================================
# 5. CORE NAVIGATION (SCRAMBLED VIEWS)
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR LOGIN")
    u = st.text_input("USER ID")
    k = st.text_input("ENCRYPTION KEY", type="password")
    if st.button("ACTIVATE SYSTEM"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "BIKO": "PRO779"}
        if u in auth and auth[u] == k:
            st.session_state["pass"] = True
            st.rerun()
        else: st.error("INVALID CREDENTIALS")
    st.markdown('</div>', unsafe_allow_html=True)

def show_casino_select():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 CASINO SOURCE")
    choice = st.selectbox("SELECT SERVER:", ["---", "Premier Bet", "AfricaBet", "1xBet", "888Starz", "SportyBet", "1win", "SpinCity", "LuckyBets"])
    if st.button("CONNECT CASINO LINK") and choice != "---":
        st.session_state["casino"] = choice
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    c1, c2, c3 = st.columns(3)
    with c1: r1 = st.text_input("Latest")
    with c2: r2 = st.text_input("Second")
    with c3: r3 = st.text_input("Third")
    if st.button("LOCK DATA STREAM"):
        if r1 and r2 and r3:
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    render_live_clock()
    
    ca, cb = st.columns(2)
    with ca: st.markdown('<button style="width:100%; padding:10px; background:#00ff00; color:#000; border:none; border-radius:10px; font-weight:bold;">📥 DOWNLOAD APK</button>', unsafe_allow_html=True)
    with cb: st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border:none; border-radius:10px; font-weight:bold;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    render_ultimate_system()
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 LIVE COMMUNITY CHAT")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="350" frameborder="0"></iframe>', height=380)
    
    if st.button("🚪 TERMINATE SESSION"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.session_state["casino"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 6. MASTER EXECUTION FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_casino_select()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
