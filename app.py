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

if "active_sessions" not in st.session_state:
    st.session_state["active_sessions"] = {}

# ==============================================================================
# 2. MASTER SYSTEM CREDENTIALS & CONSTANTS
# ==============================================================================
ADMIN_USER = "Icetrex"
ADMIN_KEY = "SOPITO"
WHATSAPP_LINK = "https://wa.me/263779174062"
VERSION = "12.1.0-ULTRA"
BUILD_ID = "IX-779-ZIM-GZU-2026"

# ==============================================================================
# 3. STATE INITIALIZATION
# ==============================================================================
states = {
    "pass": False, "casino_selected": False, "target_url": "",
    "history": [], "start_time": None, "current_user": None, "tz_offset": 2
}
for key, val in states.items():
    if key not in st.session_state: st.session_state[key] = val

# ==============================================================================
# 4. SYSTEM LOGIC: TIMER & LOCAL TIME
# ==============================================================================
def get_local_time():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=st.session_state["tz_offset"])

def check_timer():
    if st.session_state["pass"] and st.session_state["start_time"]:
        elapsed = time.time() - st.session_state["start_time"]
        if elapsed > 10800:
            u = st.session_state.get("current_user")
            if u in st.session_state["active_sessions"]: del st.session_state["active_sessions"][u]
            st.session_state["pass"] = False
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
        border: 2px solid #00ff00; text-align: center; box-shadow: 0 0 25px rgba(0,255,0,0.2);
    }}
    div[data-testid="stButton"] > button:contains("🚀") {{
        border-radius: 50% !important; width: 180px !important; height: 180px !important;
        border: 6px solid #00ff00 !important; background-color: #000 !important;
        color: #00ff00 !important; font-size: 18px !important; font-weight: bold !important;
        margin: 0 auto !important; display: flex !important; align-items: center; justify-content: center;
    }}
    div[data-testid="stButton"] > button:not(:contains("🚀")) {{
        border-radius: 12px !important; width: 100% !important; background: #111 !important; color: #00ff00 !important; border: 1px solid #333 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN & CASINO SELECTOR
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    u_field = st.text_input("USERNAME")
    k_field = st.text_input("PRODUCT KEY", type="password")
    if st.button("ACTIVATE TERMINAL"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u_field in auth and k_field == auth[u_field]:
            if u_field in st.session_state["active_sessions"]: st.error("⚠️ KEY IN USE.")
            else:
                st.session_state["active_sessions"][u_field] = True
                st.session_state["current_user"], st.session_state["pass"] = u_field, True
                st.session_state["start_time"] = time.time()
                st.rerun()
        else: st.error("❌ INVALID.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_casino_selector():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🎰 SELECT LICENSED NODE")
    nodes = {
        "--- ZIMBABWE REGION ---": "",
        "🇿🇼 Premier Bet Zimbabwe": "https://www.premierbet.com/zw",
        "🇿🇼 AfricaBet": "https://www.africabet.co.zw/",
        "🇿🇼 BeVegas": "https://bevegas.co.zw/",
        "🇿🇼 LuckyBets": "https://www.luckybet.ng/", # Regional portal
        "🇿🇼 Spin City": "https://spincity.bet/", 
        "🇿🇼 Saharabet": "https://saharabet.com/",
        "--- GLOBAL REGION ---": "",
        "🌎 1xBet Official": "https://1xbet.com/",
        "🌎 Betway": "https://www.betway.com/",
        "🌎 Melbet": "https://melbet.com/",
        "🌎 Stake.com": "https://stake.com/"
    }
    choice = st.selectbox("ACTIVE SERVER NODES:", list(nodes.keys()))
    if st.button("SYNC DISMANTLE ENGINE"):
        if "---" not in choice:
            st.session_state["target_url"], st.session_state["casino_selected"] = nodes[choice], True
            st.rerun()
        else: st.warning("Select a valid node.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: MAIN DASHBOARD
# ==============================================================================
def show_dashboard():
    sec_left = check_timer()
    now = get_local_time()
    st.markdown(f'<div style="text-align:right; font-size:11px;">TIME: {now.strftime("%H:%M")} | {int(sec_left//60)}m left</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO")
    st.info(f"SYNCED TO: {st.session_state['target_url']}")

    if st.button("🚀 PREDICT SIGNAL"):
        with st.spinner("📡 SCANNING HASH..."): time.sleep(3)
        acc = random.randint(1, 100)
        if acc <= 80:
            v, l, c = (round(random.uniform(12.0, 48.0), 2), "🔥 PINK", "#ff00ff") if random.random() > 0.88 else (round(random.uniform(2.05, 5.5), 2), "✅ GOLDEN", "#ffff00")
        else: v, l, c = round(random.uniform(1.1, 1.8), 2), "⚡ BLUE", "#00ffff"

        st.markdown(f"<h1 style='color:{c}; font-size:90px; margin:0;'>{v}x</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{c}; font-weight:bold;'>ACCURACY: {random.randint(78, 80)}%</p>", unsafe_allow_html=True)
        st.session_state.history.insert(0, f"[{now.strftime('%H:%M')}] {v}x ({l})")
        st.session_state.history = st.session_state.history[:5]

    with st.expander("📝 LOGS"):
        for e in st.session_state.history: st.markdown(f"<p style='color:#0f0; margin:0;'>{e}</p>", unsafe_allow_html=True)
    
    st.components.v1.html(f'<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="400" frameborder="0"></iframe>', height=420)
    
    if st.button("🚪 DISCONNECT"):
        u = st.session_state.get("current_user")
        if u in st.session_state["active_sessions"]: del st.session_state["active_sessions"][u]
        st.session_state["pass"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. EXECUTION
# ==============================================================================
if not st.session_state["pass"]: show_login()
elif not st.session_state["casino_selected"]: show_casino_selector()
else: show_dashboard()
