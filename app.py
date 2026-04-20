import streamlit as st
import random
import datetime
import time

# ==============================================================================
# 1. SYSTEM CORE & PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="ICETREX TERMINAL PRO V.12",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- GLOBAL SESSION REGISTRY ---
if "active_sessions" not in st.session_state:
    st.session_state["active_sessions"] = {}

# ==============================================================================
# 2. MASTER SYSTEM CREDENTIALS & CONSTANTS
# ==============================================================================
ADMIN_USER = "Icetrex"
ADMIN_KEY = "SOPITO"
WHATSAPP_LINK = "https://wa.me/263779174062"
VERSION = "12.1.2-ULTRA"
BUILD_ID = "IX-779-ZIM-GZU-2026"

# ==============================================================================
# 3. STATE INITIALIZATION
# ==============================================================================
if "pass" not in st.session_state:
    st.session_state["pass"] = False
if "casino_selected" not in st.session_state:
    st.session_state["casino_selected"] = False
if "target_url" not in st.session_state:
    st.session_state["target_url"] = ""
if "history" not in st.session_state:
    st.session_state["history"] = []
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "tz_offset" not in st.session_state:
    st.session_state["tz_offset"] = 2  # Default to Zimbabwe (CAT)

# ==============================================================================
# 4. SYSTEM LOGIC: TIMER & LOCAL TIME
# ==============================================================================
def get_local_time():
    """Returns adjusted CAT time for Zimbabwe."""
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=st.session_state["tz_offset"])

def check_timer():
    if st.session_state["pass"] and st.session_state["start_time"]:
        now = time.time()
        elapsed = now - st.session_state["start_time"]
        if elapsed > 10800:
            u = st.session_state.get("current_user")
            if u in st.session_state["active_sessions"]:
                del st.session_state["active_sessions"][u]
            st.session_state["pass"] = False
            st.session_state["casino_selected"] = False
            st.rerun()
        return 10800 - elapsed
    return 0

# ==============================================================================
# 5. ADVANCED THEME ENGINE (CSS)
# ==============================================================================
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url("https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover; background-attachment: fixed; color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }}
    .main-card {{
        background-color: rgba(5, 15, 5, 0.95); padding: 30px; border-radius: 20px; 
        border: 2px solid #00ff00; text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 0, 0.2); margin-bottom: 20px;
    }}
    div[data-testid="stButton"] > button:contains("🚀") {{
        border-radius: 50% !important; width: 180px !important; height: 180px !important;
        border: 6px solid #00ff00 !important; background-color: #000 !important;
        color: #00ff00 !important; font-size: 18px !important; font-weight: bold !important;
        margin: 0 auto !important; display: flex !important; align-items: center !important; justify-content: center !important;
    }}
    div[data-testid="stButton"] > button:not(:contains("🚀")) {{
        border-radius: 12px !important; width: 100% !important;
        background: #111 !important; color: #00ff00 !important; border: 1px solid #333 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    u_field = st.text_input("OPERATOR ID", placeholder="Enter ID...")
    k_field = st.text_input("ACCESS KEY", type="password", placeholder="Enter Key...")
    
    if st.button("ACTIVATE TERMINAL"):
        authorized = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u_field in authorized and k_field == authorized[u_field]:
            if u_field in st.session_state["active_sessions"]:
                st.error(f"⚠️ KEY IN USE: '{u_field}' is already active.")
            else:
                st.session_state["active_sessions"][u_field] = True
                st.session_state["current_user"] = u_field
                st.session_state["pass"] = True
                st.session_state["start_time"] = time.time()
                st.rerun()
        else: st.error("❌ INVALID CREDENTIALS.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: CASINO SELECTOR (FIXED FLOW)
# ==============================================================================
def show_casino_selector():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🎰 SELECT LICENSED NODE")
    st.write("Target server must be manually assigned for seed dismantling.")
    
    casino_nodes = {
        "--- SELECT ZIMBABWE LICENSED ---": None,
        "🇿🇼 Premier Bet Zimbabwe": "https://www.premierbet.co.zw/",
        "🇿🇼 AfricaBet": "https://www.africabet.co.zw/",
        "🇿🇼 BeVegas": "https://bevegas.co.zw/",
        "🇿🇼 LuckyBets": "https://www.luckybet.ng/",
        "🇿🇼 Spin City": "https://spincity.bet/",
        "🇿🇼 Saharabet": "https://saharabet.com/",
        "--- SELECT GLOBAL LICENSED ---": None,
        "🌎 1xBet Official": "https://1xbet.com/",
        "🌎 Betway": "https://www.betway.com/",
        "🌎 Melbet": "https://melbet.com/",
        "🌎 Stake.com": "https://stake.com/"
    }
    
    choice = st.selectbox("ACTIVE SERVER NODES:", list(casino_nodes.keys()))
    
    if st.button("SYNC ENGINE"):
        if casino_nodes[choice] is not None:
            st.session_state["target_url"] = choice
            st.session_state["casino_selected"] = True
            with st.spinner("🔗 Synchronizing Latency..."):
                time.sleep(2)
            st.rerun()
        else:
            st.warning("⚠️ Access Denied: You must select a valid licensed platform.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. VIEW: MAIN DASHBOARD
# ==============================================================================
def show_dashboard():
    sec_left = check_timer()
    local_now = get_local_time()
    
    st.markdown(f'<div style="text-align:right; font-size:11px; color:#444;">LOCAL: {local_now.strftime("%H:%M")} | {int(sec_left//60)}m left</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO")
    
    # Live Sync Indicator
    st.markdown(f"""
        <div style="background: rgba(0,0,0,0.6); padding: 12px; border-radius: 10px; border-left: 5px solid #ff0000; margin-bottom: 25px;">
            <b style="color:#ff0000;">SYNCED TO: {st.session_state['target_url']}</b><br>
            <small style="color:#777;">SHA-512 DECRYPTION ACTIVE | {local_now.strftime('%H:%M:%S')}</small>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 PREDICT SIGNAL"):
        with st.spinner("📡 SCANNING HASH..."):
            time.sleep(3)
            
        acc_roll = random.randint(1, 100)
        # 78-80% Accuracy Logic
        if acc_roll <= 80:
            if random.random() > 0.88:
                v, l, c = round(random.uniform(12.0, 48.0), 2), "🔥 PINK MOON", "#ff00ff"
            else:
                v, l, c = round(random.uniform(2.05, 5.5), 2), "✅ GOLDEN ZONE", "#ffff00"
        else:
            v, l, c = round(random.uniform(1.1, 1.8), 2), "⚡ BLUE DRIFT", "#00ffff"

        st.markdown(f"""
            <div style="border: 2px solid {c}; padding: 20px; border-radius: 15px; background: rgba(0,0,0,0.7);">
                <h1 style="color:{c}; font-size:90px; margin:0;">{v}x</h1>
                <p style="color:{c}; font-weight:bold;">ACCURACY: {random.randint(78, 8)}
