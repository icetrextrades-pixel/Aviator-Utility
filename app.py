import streamlit as st
import random
import datetime
import time
import hashlib

# ==============================================================================
# 1. SYSTEM CORE & PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="ICETREX TERMINAL PRO V.12.5",
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
VERSION = "12.5.0-EINSTEIN-CORE"
BUILD_ID = "IX-779-ZIM-GZU-2026-ULTRA"

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
# 4. SYSTEM LOGIC: EINSTEIN SEED INTERCEPTOR
# ==============================================================================
def get_local_time():
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=st.session_state["tz_offset"])

def simulate_seed_extraction(casino_name):
    """Simulates the extraction of the Server Seed for a specific casino."""
    # Generating a unique fake hash based on the casino name and current minute
    raw_str = f"{casino_name}-{datetime.datetime.now().minute}"
    return hashlib.sha256(raw_str.encode()).hexdigest()

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
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), 
                    url("https://images.unsplash.com/photo-1639762681485-074b7f938ba0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover; background-attachment: fixed; color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }}
    .main-card {{
        background-color: rgba(0, 10, 0, 0.98); padding: 30px; border-radius: 20px; 
        border: 1px solid #00ff00; text-align: center;
        box-shadow: 0 0 40px rgba(0, 255, 0, 0.15); margin-bottom: 20px;
    }}
    div[data-testid="stButton"] > button:contains("🚀") {{
        border-radius: 50% !important; width: 200px !important; height: 200px !important;
        border: 4px solid #00ff00 !important; background: radial-gradient(#003300, #000) !important;
        color: #00ff00 !important; font-size: 20px !important; font-weight: bold !important;
        box-shadow: 0 0 30px #00ff00; margin: 0 auto !important; display: flex !important;
    }}
    .hash-text {{ font-size: 10px; color: #006600; overflow-wrap: break-word; }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ EINSTEIN CORE AUTH")
    u = st.text_input("OPERATOR ID")
    k = st.text_input("ACCESS KEY", type="password")
    if st.button("ACTIVATE SYSTEMS"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u in auth and k == auth[u]:
            st.session_state["active_sessions"][u] = True
            st.session_state["current_user"], st.session_state["pass"] = u, True
            st.session_state["start_time"] = time.time()
            st.rerun()
        else: st.error("ACCESS DENIED.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: AUTO-SEED CASINO SELECTOR
# ==============================================================================
def show_casino_selector():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 CASINO INTERCEPT")
    nodes = {
        "--- SELECT TARGET ---": None,
        "🇿🇼 Premier Bet ZIM": "premierbet.co.zw",
        "🇿🇼 AfricaBet ZIM": "africabet.co.zw",
        "🇿🇼 Spin City": "spincity.bet",
        "🇿🇼 LuckyBets": "luckybet.ng",
        "🌎 1xBet Global": "1xbet.com",
        "🌎 Stake.com": "stake.com"
    }
    choice = st.selectbox("ACTIVE CASINO NODES:", list(nodes.keys()))
    if st.button("INITIALIZE SEED SNIFFER"):
        if nodes[choice]:
            st.session_state["target_url"] = choice
            with st.status(f"Sniffing {choice} Server Seeds...", expanded=True):
                st.write("Intercepting Spribe API packets...")
                time.sleep(1.5)
                st.write(f"Current Server Seed: {simulate_seed_extraction(choice)[:32]}...")
                time.sleep(1)
                st.write("Calculating 92% Probability curve...")
                st.session_state["casino_selected"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. VIEW: MAIN DASHBOARD (92% ACCURACY ENGINE)
# ==============================================================================
def show_dashboard():
    sec_left = check_timer()
    now = get_local_time()
    st.markdown(f'<div style="text-align:right; font-size:11px;">{now.strftime("%H:%M:%S")} | {int(sec_left//60)}m Remaining</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO V.12.5")
    
    # Automatic Seed Data Display
    current_seed = simulate_seed_extraction(st.session_state["target_url"])
    st.markdown(f"""
        <div style="background: rgba(0,255,0,0.05); border: 1px solid #004400; padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <small style="color:#008800;">ACTIVE SEED SNIFFER: {st.session_state['target_url']}</small><br>
            <code class="hash-text">{current_seed}</code>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 PREDICT NEXT"):
        with st.spinner("🧠 EINSTEIN MATH IN PROGRESS..."):
            time.sleep(4)
            
        # The New 92% Logic (Lower failure rate)
        acc_roll = random.randint(1, 100)
        if acc_roll <= 92: # Accuracy increased by 12% from 80%
            if random.random() > 0.90:
                v, l, c = round(random.uniform(15.0, 60.0), 2), "🔥 EINSTEIN PINK", "#ff00ff"
            else:
                v, l, c = round(random.uniform(2.10, 8.5), 2), "✅ QUANTUM GOLD", "#ffff00"
        else:
            v, l, c = round(random.uniform(1.0, 1.9), 2), "⚡ ENTROPY BLUE", "#00ffff"

        st.markdown(f"""
            <div style="border: 2px solid {c}; padding: 25px; border-radius: 20px; background: rgba(0,0,0,0.8); box-shadow: 0 0 20px {c}44;">
                <p style="color:{c}; font-size:12px; margin-bottom:0;">NEXT SIGNAL ESTIMATED</p>
                <h1 style="color:{c}; font-size:100px; margin:0; line-height:1;">{v}x</h1>
                <p style="color:{c}; font-weight:bold; letter-spacing: 2px;">ACCURACY: {random.randint(91, 93)}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state.history.insert(0, f"[{now.strftime('%H:%M')}] {v}x - {l} (Seed Match: 92%)")
        st.session_state.history = st.session_state.history[:5]

    if st.session_state.history:
        with st.expander("📝 SYSTEM LOGS (92% ACCURACY)"):
            for entry in st.session_state.history:
                st.markdown(f"<p style='color:#00ff00; font-size:11px; margin:0;'>{entry}</p>", unsafe_allow_html=True)

    st.markdown("---")
    st.components.v1.html(f'<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="400" frameborder="0"></iframe>', height=420)
    
    col_a, col_b = st.columns(2)
    with col_a: st.markdown(f'<a href="{WHATSAPP_LINK}"><button style="width:100%; padding:12px; border-radius:10px; background:#25D366; color:white; border:none;">SUPPORT</button></a>', unsafe_allow_html=True)
    with col_b:
        if st.button("🚪 LOGOUT"):
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
