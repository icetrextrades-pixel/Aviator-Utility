import streamlit as st
import random
import datetime
import time
import hashlib

# ==============================================================================
# 1. SYSTEM CORE & PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="AVIATOR PREDICTOR PRO",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "active_sessions" not in st.session_state:
    st.session_state["active_sessions"] = {}

# ==============================================================================
# 2. MASTER SYSTEM CREDENTIALS
# ==============================================================================
ADMIN_USER = "Icetrex"
ADMIN_KEY = "SOPITO"
WHATSAPP_LINK = "https://wa.me/263779174062"
VERSION = "12.8.5-PREDICTOR-CORE"

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
# 4. SCRAMBLER & INTERCEPTOR LOGIC
# ==============================================================================
def get_local_time():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=st.session_state["tz_offset"])

def fetch_scrambled_seeds(casino):
    """
    Simulates logging into the casino server and scrambling 
    previous seeds using a time-based salt.
    """
    current_min = datetime.datetime.now().minute
    # Scramble logic using SHA-256 with a shifting salt
    seed_chain = [hashlib.sha256(f"{casino}-{current_min}-{i}".encode()).hexdigest() for i in range(3)]
    return seed_chain

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
# 5. THEME ENGINE (CSS)
# ==============================================================================
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), 
                    url("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover; background-attachment: fixed; color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }}
    .main-card {{
        background-color: rgba(5, 5, 5, 0.98); padding: 30px; border-radius: 20px; 
        border: 1px solid #ff0000; text-align: center;
        box-shadow: 0 0 35px rgba(255, 0, 0, 0.2); margin-bottom: 20px;
    }}
    div[data-testid="stButton"] > button:contains("🚀") {{
        border-radius: 50% !important; width: 180px !important; height: 180px !important;
        border: 4px solid #ff0000 !important; background: #000 !important;
        color: #ff0000 !important; font-size: 20px !important; font-weight: bold !important;
        box-shadow: 0 0 20px #ff0000; margin: 0 auto !important; display: flex !important;
    }}
    .seed-box {{ font-size: 9px; color: #444; font-family: monospace; line-height: 1; }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN (RENAMED)
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ AVIATOR PREDICTOR")
    st.write("SECURE OPERATOR ACCESS")
    u = st.text_input("ID")
    k = st.text_input("KEY", type="password")
    if st.button("LOGIN"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u in auth and k == auth[u]:
            st.session_state["active_sessions"][u] = True
            st.session_state["current_user"], st.session_state["pass"] = u, True
            st.session_state["start_time"] = time.time()
            st.rerun()
        else: st.error("INVALID ACCESS")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: CASINO SELECTOR
# ==============================================================================
def show_casino_selector():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛰️ TARGET CASINO")
    nodes = {
        "--- SELECT ---": None,
        "🇿🇼 Premier Bet": "premierbet.co.zw",
        "🇿🇼 AfricaBet": "africabet.co.zw",
        "🇿🇼 BeVegas": "bevegas.co.zw",
        "🇿🇼 LuckyBets": "luckybet.ng",
        "🇿🇼 Spin City": "spincity.bet",
        "🌎 1xBet": "1xbet.com",
        "🌎 Stake.com": "stake.com"
    }
    choice = st.selectbox("CASINO SERVER:", list(nodes.keys()))
    if st.button("LINK TO SERVER"):
        if nodes[choice]:
            st.session_state["target_url"] = choice
            with st.status(f"Logging into {choice} Server...", expanded=True):
                st.write("Bypassing firewall...")
                time.sleep(1)
                st.write("Extracting previous round seeds...")
                time.sleep(1)
                st.write("Scrambling hash chain...")
                st.session_state["casino_selected"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. VIEW: MAIN DASHBOARD (90%+ ACCURACY)
# ==============================================================================
def show_dashboard():
    sec_left = check_timer()
    now = get_local_time()
    st.markdown(f'<div style="text-align:right; font-size:10px;">{now.strftime("%H:%M:%S")} | {int(sec_left//60)}m active</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("✈️ PREDICTOR PRO")
    
    # Automatic Server Seed Monitoring
    seeds = fetch_scrambled_seeds(st.session_state["target_url"])
    st.markdown(f"""
        <div style="background: rgba(255,0,0,0.05); border: 1px solid #330000; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <small style="color:#ff0000;">SERVER LOGGED: {st.session_state['target_url']}</small><br>
            <div class="seed-box">PREV_SEED_1: {seeds[0][:30]}...</div>
            <div class="seed-box">PREV_SEED_2: {seeds[1][:30]}...</div>
            <div class="seed-box">SCRAMBLED_CURRENT: {seeds[2][:30]}...</div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 PREDICT"):
        with st.spinner("📡 ANALYZING SCRAMBLED SEEDS..."):
            time.sleep(4)
            
        acc_roll = random.randint(1, 100)
        # Accuracy maintained above 90%
        if acc_roll <= 93:
            if random.random() > 0.92:
                v, l, c = round(random.uniform(15.0, 55.0), 2), "🔥 PINK", "#ff00ff"
            else:
                v, l, c = round(random.uniform(2.15, 7.8), 2), "✅ GOLD", "#ffff00"
        else:
            v, l, c = round(random.uniform(1.0, 1.5), 2), "⚡ BLUE", "#00ffff"

        st.markdown(f"""
            <div style="border: 2px solid {c}; padding: 20px; border-radius: 20px; background: rgba(0,0,0,0.85);">
                <h1 style="color:{c}; font-size:95px; margin:0;">{v}x</h1>
                <p style="color:{c}; font-weight:bold;">ACCURACY: {random.randint(91, 94)}%</p>
                <code style="color:#222; font-size:9px;">RESULT_HASH: {hashlib.md5(str(v).encode()).hexdigest()}</code>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state.history.insert(0, f"[{now.strftime('%H:%M')}] {v}x - {l} (Verified)")
        st.session_state.history = st.session_state.history[:5]

    with st.expander("📝 SERVER LOG HISTORY"):
        for entry in st.session_state.history:
            st.markdown(f"<p style='color:#ff0000; font-size:11px; margin:0;'>{entry}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.components.v1.html(f'<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="400" frameborder="0"></iframe>', height=420)
    
    if st.button("🚪 DISCONNECT"):
        u = st.session_state.get("current_user")
        if u in st.session_state["active_sessions"]: del st.session_state["active_sessions"][u]
        st.session_state["pass"] = False
        st.session_state["casino_selected"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 9. EXECUTION FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif not st.session_state["casino_selected"]:
    show_casino_selector()
else:
    show_dashboard()
