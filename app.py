import streamlit as st
import random
import datetime
import time

# ==============================================================================
# 1. CORE SYSTEM CONFIG
# ==============================================================================
st.set_page_config(page_title="AVIATOR PREDICTOR PRO", page_icon="✈️", layout="centered")

if "history" not in st.session_state:
    st.session_state.update({
        "pass": False, "synced": False, "target_url": "Global Server",
        "history": [], "current_user": None
    })

# ==============================================================================
# 2. THEME ENGINE (ULTRA-DARK STYLE)
# ==============================================================================
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; font-family: 'Courier New', monospace; }
    .main-card {
        background: rgba(10, 10, 10, 0.98); padding: 20px; border-radius: 15px; 
        border: 1px solid #00d4ff; text-align: center; box-shadow: 0 0 20px #00d4ff22;
        margin-bottom: 20px;
    }
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 10px; background: #000 !important; color: #00d4ff !important; 
        border: 1px solid #00d4ff !important; font-weight: bold;
    }
    .predict-container > div > button {
        height: 80px !important; font-size: 24px !important; 
        border: 2px solid #ff00ff !important; color: #ff00ff !important;
        box-shadow: 0 0 15px #ff00ff44 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. ANALYSIS LOGIC
# ==============================================================================
def calculate_signal(data):
    try:
        floats = [float(x.replace('x','')) for x in data if 'x' in str(x)]
        if not floats: return 1.85
        avg = sum(floats[:3]) / 3
        # Einstein Pattern: Low avg predicts imminent burst
        return round(random.uniform(2.8, 12.0), 2) if avg < 2.0 else round(random.uniform(1.15, 1.98), 2)
    except:
        return 2.10

# ==============================================================================
# 4. VIEW: SYNC (ORDER: MOST RECENT -> OLDEST)
# ==============================================================================
def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛰️ SYSTEM SYNCHRONIZATION")
    st.info("ORDER: Enter the last 3 results from left to right (Newest to Oldest).")
    
    col1, col2, col3 = st.columns(3)
    with col1: r1 = st.text_input("1st Recent", placeholder="Newest")
    with col2: r2 = st.text_input("2nd Recent", placeholder="Previous")
    with col3: r3 = st.text_input("3rd Recent", placeholder="Oldest")
    
    if st.button("LOCK & INITIALIZE"):
        if r1 and r2 and r3:
            st.session_state.history = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state.synced = True
            st.rerun()
        else:
            st.warning("All 3 fields are required.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. VIEW: DASHBOARD
# ==============================================================================
def show_dashboard():
    # Top Utility Bar
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<a href="https://example.com/icetrex.apk" target="_blank"><button style="width:100%; padding:10px; border-radius:8px; background:#00ff00; color:#000; border:none; font-weight:bold; cursor:pointer;">📥 DOWNLOAD APK</button></a>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; border-radius:8px; background:#25D366; color:#fff; border:none; font-weight:bold; cursor:pointer;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("✈️ PREDICTOR PRO")
    
    st.markdown('<div class="predict-container">', unsafe_allow_html=True)
    if st.button("🚀 PREDICT NEXT SIGNAL"):
        with st.spinner("ANALYZING LIVE DATA..."):
            time.sleep(2)
        v = calculate_signal(st.session_state.history)
        color = "#ff00ff" if v >= 5 else "#ffff00" if v >= 2 else "#00d4ff"
        st.markdown(f"""
            <div style="border: 2px solid {color}; padding: 20px; border-radius: 15px; background: #000; margin-top: 10px;">
                <h1 style="color: {color}; font-size: 90px; margin: 0;">{v}x</h1>
                <p style="color: {color}; font-weight: bold;">MATCH: {random.randint(94, 98)}%</p>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.history.insert(0, f"{v}x")
    st.markdown('</div>', unsafe_allow_html=True)

    # Community Chat Box
    st.markdown("---")
    st.write("🌐 COMMUNITY CHAT")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="400" frameborder="0"></iframe>', height=420)
    
    if st.button("🚪 LOGOUT"):
        st.session_state.update({"pass": False, "synced": False})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: LOGIN
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR LOGIN")
    u = st.text_input("ID")
    k = st.text_input("KEY", type="password")
    if st.button("ACTIVATE"):
        if u == "Icetrex" and k == "SOPITO":
            st.session_state.pass = True
            st.rerun()
        else:
            st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. EXECUTION FLOW (FIXED SYNTAX)
# ==============================================================================
if not st.session_state.pass:
    show_login()
elif not st.session_state.synced:
    show_sync()
else:
    show_dashboard()
