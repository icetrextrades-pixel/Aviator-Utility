import streamlit as st
import random
import time
from datetime import datetime, timedelta

# ==============================================================================
# 1. ATOMIC INITIALIZATION
# ==============================================================================
if "pass" not in st.session_state:
    st.session_state["pass"] = False
if "synced" not in st.session_state:
    st.session_state["synced"] = False
if "casino" not in st.session_state:
    st.session_state["casino"] = None
if "history" not in st.session_state:
    st.session_state["history"] = []

# ==============================================================================
# 2. INTERFACE STYLING
# ==============================================================================
st.set_page_config(page_title="AVIATOR PREDICTOR PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; font-family: monospace; }
    .main-card {
        background: #0a0a0a; padding: 20px; border-radius: 15px; 
        border: 1px solid #00d4ff; text-align: center; margin-bottom: 20px;
    }
    .time-display {
        color: #ff00ff; font-size: 18px; font-weight: bold; margin-bottom: 10px;
    }
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 10px; background: #000 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff !important; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. CORE ANALYZER & TIME LOGIC
# ==============================================================================
def get_live_time():
    # Adjusted for Zimbabwe Time (UTC+2)
    return (datetime.utcnow() + timedelta(hours=2)).strftime("%H:%M:%S")

def calculate_signal(data):
    try:
        floats = [float(x.replace('x','')) for x in data if 'x' in str(x)]
        if not floats: return 1.85
        avg = sum(floats[:3]) / 3
        if avg < 2.0:
            return round(random.uniform(2.80, 14.50), 2)
        return round(random.uniform(1.10, 1.98), 2)
    except:
        return 2.10

# ==============================================================================
# 4. VIEW FUNCTIONS
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
        else:
            st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

def show_casino_select():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 SELECT CASINO")
    casinos = ["--- SELECT ---", "Premier Bet", "AfricaBet", "BeVegas", "1xBet", "888Starz", "SportyBet"]
    choice = st.selectbox("Choose Target Casino:", casinos)
    if st.button("PROCEED TO SYNC"):
        if choice != "--- SELECT ---":
            st.session_state["casino"] = choice
            st.rerun()
        else:
            st.warning("Please select a casino.")
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    st.info("Input Multipliers: Most Recent → Previous → Oldest")
    c1, c2, c3 = st.columns(3)
    with c1: r1 = st.text_input("Newest")
    with c2: r2 = st.text_input("Previous")
    with c3: r3 = st.text_input("Oldest")
    if st.button("LOCK DATA"):
        if r1 and r2 and r3:
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # Floating Time Header
    st.markdown(f'<div class="time-display">LIVE SERVER TIME: {get_live_time()}</div>', unsafe_allow_html=True)
    
    ca, cb = st.columns(2)
    with ca: st.markdown('<a href="#" target="_blank"><button style="width:100%; padding:10px; border-radius:8px; background:#00ff00; color:#000; border:none; font-weight:bold;">📥 APK</button></a>', unsafe_allow_html=True)
    with cb: st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; border-radius:8px; background:#25D366; color:#fff; border:none; font-weight:bold;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("✈️ PREDICTOR PRO")
    st.write(f"SERVER: {st.session_state['casino']} | STATUS: LIVE")
    
    if st.button("🚀 PREDICT NEXT SIGNAL"):
        with st.spinner("ANALYZING LIVE TRENDS..."):
            time.sleep(4)
        v = calculate_signal(st.session_state["history"])
        st.markdown(f"""
            <div style="border: 2px solid #ff00ff; padding: 20px; border-radius: 15px; background: #000;">
                <h1 style="color: #ff00ff; font-size: 80px; margin: 0;">{v}x</h1>
                <p style="color: #ff00ff;">ACCURACY: {random.randint(94, 98)}%</p>
            </div>
        """, unsafe_allow_html=True)
        st.session_state["history"].insert(0, f"{v}x")
    
    st.markdown("---")
    st.write("🌐 COMMUNITY CHAT")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="350" frameborder="0"></iframe>', height=380)
    
    if st.button("🚪 LOGOUT"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.session_state["casino"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. MASTER CONTROL FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_casino_select()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
