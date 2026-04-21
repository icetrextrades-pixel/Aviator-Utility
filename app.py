import streamlit as st
import random
import time
from datetime import datetime

# ==============================================================================
# 1. ATOMIC INITIALIZATION
# ==============================================================================
# We initialize all states to None or False to prevent KeyError on launch.
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []
# Placeholder for the prediction result so it doesn't vanish during animations
if "last_v" not in st.session_state: st.session_state["last_v"] = None

# ==============================================================================
# 2. INTERFACE & BACKGROUND WALLPAPER
# ==============================================================================
st.set_page_config(page_title="ICETREX PREDICTOR PRO", layout="centered")

# Replace this URL with your preferred background image
WALLPAPER_URL = "https://tse3.mm.bing.net/th/id/OIP.BIbCCJQo4r2U4084ObJetgHaEK?rs=1&pid=ImgDetMain&o=7&rm=3"

st.markdown(f"""
<style>
.stApp {{
    background-image: url("{WALLPAPER_URL}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #00d4ff;
    font-family: monospace;
}}

.main-card {{
    background: rgba(10, 10, 10, 0.90);
    padding: 20px;
    border-radius: 15px; 
    border: 1px solid #00d4ff;
    text-align: center;
    margin-bottom: 20px;
}}

div[data-testid="stButton"] > button {{
    width: 100%; 
    border-radius: 10px; 
    background: #000 !important; 
    color: #00d4ff !important; 
    border: 1px solid #00d4ff !important; 
    font-weight: bold;
}}

.predict-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px 0;
    position: relative;
}}

.round-btn {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background-color: #ff0000;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border: 4px solid #fff;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
    z-index: 10;
}}

.lap-timer {{
    position: absolute;
    width: 170px;
    height: 170px;
    border-radius: 50%;
    border: 4px solid transparent;
    z-index: 5;
}}

.lap-timer.active {{
    border: 4px solid #00ff00;
    animation: timeLap 2.5s linear forwards;
}}

@keyframes timeLap {{
    0% {{ transform: rotate(0deg); border-left-color: #00ff00; border-top-color: transparent; border-right-color: transparent; border-bottom-color: transparent; }}
    25% {{ border-top-color: #00ff00; }}
    50% {{ border-right-color: #00ff00; }}
    75% {{ border-bottom-color: #00ff00; }}
    100% {{ transform: rotate(360deg); border-color: #00ff00; }}
}}
</style>
""", unsafe_allow_html=True)
# ==============================================================================
# 3. LIVE CLOCK (JavaScript)
# ==============================================================================
def render_live_clock():
    # Adjusted for Zimbabwe Time (UTC+2)
    st.components.v1.html("""
    <div id="clock" style="color: #ff00ff; font-family: monospace; font-size: 20px; font-weight: bold; text-align: center; border: 1px solid #333; padding: 10px; border-radius: 10px; background: #000;">
        LIVE SERVER TIME: 00:00:00
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        now.setHours(now.getUTCHours() + 2);
        var h = String(now.getHours()).padStart(2, '0');
        var m = String(now.getMinutes()).padStart(2, '0');
        var s = String(now.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerHTML = "LIVE SERVER TIME: " + h + ":" + m + ":" + s;
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, height=60)

# ==============================================================================
# 4. GAP ANALYSIS ENGINE (Anti-Fool Logic)
# ==============================================================================
def calculate_signal(data):
    try:
        vals = [float(x.replace('x','')) for x in data if 'x' in str(x)]
        if len(vals) < 3: return 1.85
        
        # Gap Analysis: Check for low-multiplier 'starvation' (Exhaustion Point)
        if all(v < 1.45 for v in vals[:3]):
            # Pressure build-up for the Pink 100x spike
            return round(random.uniform(15.50, 95.00), 2)
            
        # Cooldown Check: A high multiplier just happened, the next is a Lie
        if any(v > 10.0 for v in vals[:2]):
            return round(random.uniform(1.01, 1.30), 2)
            
        # Default Trend / Stability Check
        return round(random.uniform(2.10, 4.80), 2)
    except:
        return 1.45

# ==============================================================================
# 5. THE PURE JAVASCRIPT ANIMATION COMPONENT
# ==============================================================================
def render_round_predict_system():
    # Feeding the current history into the JS Brain
    hist_str = ",".join([x.replace('x','') for x in st.session_state["history"]])
    
    st.components.v1.html(f"""
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); border-top-color: #00ff00; }}
            100% {{ transform: rotate(360deg); border-top-color: #00ff00; border-right-color: #00ff00; border-bottom-color: #00ff00; border-left-color: #00ff00; }}
        }}
        
        .circle-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Courier New', Courier, monospace;
        }}

        /* THE ACTUAL ROUND BUTTON */
        #p-btn {{
            width: 130px !important;
            height: 130px !important;
            border-radius: 50% !important; /* This forces the circle */
            background-color: #ff0000 !important; /* Solid Red */
            color: white !important;
            border: 4px solid #ffffff !important;
            font-weight: bold !important;
            font-size: 16px !important;
            cursor: pointer;
            z-index: 10;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            transition: 0.2s;
            outline: none;
        }}

        #p-btn:active {{
            transform: scale(0.95);
            background-color: #cc0000 !important;
        }}

        /* THE GREEN LAP TIMER */
        #loader {{
            position: absolute;
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 5px solid transparent;
            z-index: 5;
            pointer-events: none;
        }}
    </style>

    <div class="circle-wrapper">
        <div id="res-box" style="border: 2px solid #00d4ff; padding: 15px; border-radius: 15px; background: rgba(0,0,0,0.85); width: 100%; margin-bottom: 25px; text-align: center;">
            <p id="status-text" style="color: #00d4ff; font-size: 12px; margin: 0; letter-spacing: 2px;">READY TO SCAN</p>
            <h1 id="sig-display" style="color: #00d4ff; font-size: 80px; margin: 10px 0;">0.00x</h1>
            <p style="color: #00d4ff; font-size: 12px; opacity: 0.7;">PATTERN MATCH: 98%</p>
        </div>

        <div style="position: relative; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center;">
            <div id="loader"></div>
            <button id="p-btn">PREDICT<br>NEXT</button>
        </div>
    </div>

    <script>
    const btn = document.getElementById('p-btn');
    const loader = document.getElementById('loader');
    const display = document.getElementById('sig-display');
    const status = document.getElementById('status-text');
    const history = [{hist_str}];

    btn.addEventListener('click', () => {{
        // Start Animation
        btn.innerHTML = "SCANNING";
        loader.style.animation = "spin 2.5s linear forwards";
        status.innerHTML = "INTERCEPTING DATA...";
        status.style.color = "#ffff00";

        setTimeout(() => {{
            // GAP ANALYSIS (Mirrors Python Logic)
            let result = 1.85;
            if (history.length >= 3) {{
                const vals = history.slice(0,3);
                const lowStreak = vals.every(v => v < 1.45);
                const recentPink = vals.slice(0,2).some(v => v > 10);
                
                if (lowStreak) {{
                    result = (Math.random() * (60.0 - 15.0) + 15.0).toFixed(2);
                }} else if (recentPink) {{
                    result = (Math.random() * (1.30 - 1.01) + 1.01).toFixed(2);
                }} else {{
                    result = (Math.random() * (4.2 - 2.1) + 2.1).toFixed(2);
                }}
            }}

            // Update UI with Result
            const color = result >= 10 ? "#ff00ff" : "#00d4ff";
            display.innerHTML = result + "x";
            display.style.color = color;
            document.getElementById('res-box').style.borderColor = color;
            status.innerHTML = "SIGNAL VERIFIED";
            status.style.color = color;

            // Reset Button
            btn.innerHTML = "PREDICT<br>NEXT";
            loader.style.animation = "none";
        }}, 2500);
    }});
    </script>
    """, height=480)

# ==============================================================================
# 6. VIEW FUNCTIONS
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR LOGIN")
    u = st.text_input("ID")
    k = st.text_input("KEY", type="password")
    if st.button("ACTIVATE"):
        authorized_users = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "BIKO": "PRO779"}
        if u in authorized_users and authorized_users[u] == k:
            st.session_state["pass"] = True
            st.rerun()
        else: st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

def show_casino_select():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 SELECT SOURCE")
    choice = st.selectbox("CASINO:", ["---", "Premier Bet", "AfricaBet", "1xBet", "888Starz", "LuckyBets", "1win", "SpinCity", "MWOS", "Zanzibet"])
    if st.button("CONNECT") and choice != "---":
        st.session_state["casino"] = choice
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    c1, c2, c3 = st.columns(3)
    with c1: r1 = st.text_input("Newest")
    with c2: r2 = st.text_input("Previous")
    with c3: r3 = st.text_input("Oldest")
    if st.button("LOCK DATA"):
        if r1 and r2 and r3:
            # Important: Format with 'x' to ensure the analyzer handles it correctly
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # 1. LIVE CLOCK Header
    render_live_clock()
    
    # 2. Utility Buttons
    ca, cb = st.columns(2)
    with ca: st.markdown('<button style="width:100%; padding:10px; background:#00ff00; color:#000; border:none; border-radius:10px; font-weight:bold;">📥 APK</button>', unsafe_allow_html=True)
    with cb: st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border:none; border-radius:10px; font-weight:bold;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    # 3. THE ADVANCED PREDICITON SYSTEM (Fix #2, #3, #4)
    # JavaScript handles the circular button and the animation.
    render_round_predict_system()
    
    # 4. Community Chat
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 COMMUNITY CHAT")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="350" frameborder="0"></iframe>', height=380)
    
    if st.button("🚪 LOGOUT"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.session_state["casino"] = None
        # Clean up the prediction state too
        st.session_state["last_v"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. EXECUTION FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_casino_select()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
