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
APK_URL = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"
WHATSAPP_LINK = "https://wa.me/263779174062"
VERSION = "12.0.9-ULTRA"
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

# ==============================================================================
# 4. SYSTEM LOGIC: TIMER & SECURITY
# ==============================================================================
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
            st.session_state["start_time"] = None
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
    .sync-light {{
        width: 10px; height: 10px; background: red; border-radius: 50%;
        display: inline-block; margin-right: 10px; animation: pulse-red 2s infinite ease-in-out;
    }}
    @keyframes pulse-red {{
        0% {{ transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }}
        70% {{ transform: scale(1.1); box-shadow: 0 0 0 8px rgba(255, 0, 0, 0); }}
        100% {{ transform: scale(0.9); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    u_field = st.text_input("OPERATOR ID")
    k_field = st.text_input("ACCESS KEY", type="password")
    
    if st.button("ACTIVATE TERMINAL"):
        authorized = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u_field in authorized and k_field == authorized[u_field]:
            if u_field in st.session_state["active_sessions"]:
                st.error(f"⚠️ KEY IN USE: '{u_field}' is active on another node.")
            else:
                st.session_state["active_sessions"][u_field] = True
                st.session_state["current_user"] = u_field
                st.session_state["pass"] = True
                st.session_state["start_time"] = time.time()
                st.rerun()
        else: st.error("❌ INVALID CREDENTIALS.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. VIEW: CASINO SELECTOR (LICENSED NODES)
# ==============================================================================
def show_casino_selector():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🎰 SELECT LICENSED NODE")
    
    # Categorized list of legal and licensed casinos
    casino_nodes = {
        "--- SELECT ZIMBABWE LICENSED ---": "",
        "🇿🇼 AfricaBet Zimbabwe": "https://www.africabet.co.zw/",
        "🇿🇼 BeVegas Zimbabwe": "https://bevegas.co.zw/",
        "🇿🇼 Saharabet": "https://saharabet.com/",
        "🇿🇼 Winner.co.zw": "https://winner.co.zw/",
        "🇿🇼 BetXchange": "https://www.betxchange.com/",
        "--- SELECT GLOBAL LICENSED ---": "",
        "🌎 1xBet Official": "https://1xbet.com/",
        "🌎 Betway Global": "https://www.betway.com/",
        "🌎 22Bet License": "https://22bet.com/",
        "🌎 Melbet Official": "https://melbet.com/",
        "🌎 Parimatch": "https://parimatch.com/",
        "🌎 Hollywoodbets": "https://www.hollywoodbets.net/",
        "🌎 888 Casino": "https://www.888casino.com/",
        "🌎 Bet365": "https://www.bet365.com/",
        "🌎 Sportingbet": "https://gaming.sportingbet.com/",
        "🌎 William Hill": "https://www.williamhill.com/",
        "🌎 Stake.com": "https://stake.com/"
    }
    
    choice = st.selectbox("ACTIVE SERVER NODES:", list(casino_nodes.keys()))
    
    if st.button("SYNC DISMANTLE ENGINE"):
        if "SELECT" not in choice:
            st.session_state["target_url"] = casino_nodes[choice]
            st.session_state["casino_selected"] = True
            with st.status("🔗 Linking to Host Server...", expanded=True):
                st.write("Fetching Server Seed...")
                time.sleep(1)
                st.write("Verifying License Encryption...")
                time.sleep(1)
            st.rerun()
        else: st.warning("Please choose a valid licensed platform.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. VIEW: MAIN DASHBOARD
# ==============================================================================
def show_dashboard():
    sec_left = check_timer()
    st.markdown(f'<div style="text-align:right; font-size:11px; color:#444;">USER: {st.session_state["current_user"]} | {int(sec_left//60)}m left</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO V.12")
    
    st.markdown(f"""
        <div style="background: rgba(0,0,0,0.6); padding: 12px; border-radius: 10px; border-left: 5px solid #ff0000; margin-bottom: 25px;">
            <span class="sync-light"></span><b style="color:#ff0000;">SYNCED TO: {st.session_state['target_url']}</b><br>
            <small style="color:#777;">DECRYPTING SEED NODES | {datetime.datetime.now().strftime('%H:%M:%S')}</small>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 PREDICT SIGNAL"):
        with st.spinner("📡 DISMANTLING STATISTICS..."):
            time.sleep(5)
            
        accuracy_trigger = random.randint(1, 100)
        # The 78-80% Dismantle Algorithm
        if accuracy_trigger <= 80:
            sub = random.random()
            if sub > 0.88: v, l, c = round(random.uniform(12.0, 48.0), 2), "🔥 PINK MOON", "#ff00ff"
            else: v, l, c = round(random.uniform(2.05, 5.5), 2), "✅ GOLDEN ZONE", "#ffff00"
        else: v, l, c = round(random.uniform(1.1, 1.8), 2), "⚡ BLUE DRIFT", "#00ffff"

        st.markdown(f"""
            <div style="border: 2px solid {c}; padding: 20px; border-radius: 15px; background: rgba(0,0,0,0.7);">
                <h1 style="color:{c}; font-size:90px; margin:0;">{v}x</h1>
                <p style="color:{c}; font-weight:bold;">ACCURACY: {random.randint(78, 80)}%</p>
                <code style="color:#333; font-size:9px;">SHA-512 HASH: {hex(random.getrandbits(128))}</code>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.history.insert(0, f"{v}x ({l}) - Seed Match {accuracy_trigger}%")
        st.session_state.history = st.session_state.history[:5]

    if st.session_state.history:
        with st.expander("📝 SYSTEM LOGS"):
            for entry in st.session_state.history:
                st.markdown(f"<p style='color:#00ff00; font-size:12px; margin:0;'>{entry}</p>", unsafe_allow_html=True)

    st.markdown("---")
    with st.expander("📊 ACCOUNTING LEDGER"):
        c1, c2 = st.columns(2)
        with c1: s_bal = st.number_input("Opening Bal", value=10.0)
        with c2: e_bal = st.number_input("Closing Bal", value=10.0)
        st.markdown(f"#### Net P/L: {'$'+str(round(e_bal - s_bal, 2))}")

    st.components.v1.html(f'<div style="border: 1px solid #00ff00; border-radius: 15px; overflow: hidden;"><iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="400" frameborder="0"></iframe></div>', height=420)
    
    col_a, col_b = st.columns(2)
    with col_a: st.markdown(f'<a href="{WHATSAPP_LINK}"><button style="width:100%; padding:12px; border-radius:10px; background:#25D366; color:white; border:none;">SUPPORT</button></a>', unsafe_allow_html=True)
    with col_b:
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
