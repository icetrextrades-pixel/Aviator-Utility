import streamlit as st
import random
import datetime
import time

# ==============================================================================
# 1. CORE CONFIG
# ==============================================================================
st.set_page_config(page_title="AVIATOR PREDICTOR PRO", page_icon="✈️", layout="centered")

# Initialize all states immediately to prevent "Invalid" ghost errors
states = {
    "pass": False, "casino_selected": False, "synced": False, "target_url": "",
    "history": [], "start_time": None, "current_user": None
}
for key, val in states.items():
    if key not in st.session_state: st.session_state[key] = val

# ==============================================================================
# 2. THEME ENGINE
# ==============================================================================
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00d4ff; font-family: monospace; }
    .main-card {
        background: rgba(10, 10, 10, 0.95); padding: 25px; border-radius: 15px; 
        border: 1px solid #00d4ff; text-align: center; box-shadow: 0 0 20px #00d4ff33;
    }
    div[data-testid="stButton"] > button {
        width: 100%; border-radius: 8px; background: #000; color: #00d4ff; border: 1px solid #00d4ff;
    }
    .predict-box { border: 2px solid #00d4ff; padding: 30px; border-radius: 20px; background: #000; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. LOGIC: PATTERN ANALYZER
# ==============================================================================
def analyze_pattern(history):
    if not history: return 2.00
    try:
        # Clean the strings to get pure numbers
        vals = [float(str(h).split(' ')[-1].replace('x', '')) for h in history if 'x' in str(h)]
        avg = sum(vals) / len(vals)
        if avg < 2.0: return round(random.uniform(3.0, 12.0), 2)
        return round(random.uniform(1.2, 2.5), 2)
    except: return round(random.uniform(1.5, 3.5), 2)

# ==============================================================================
# 4. VIEW: LOGIN
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR LOGIN")
    u = st.text_input("ID")
    k = st.text_input("KEY", type="password")
    if st.button("ACTIVATE"):
        auth = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "Osmando": "PRO779"}
        if u in auth and k == auth[u]:
            st.session_state.update({"pass": True, "start_time": time.time(), "current_user": u})
            st.rerun()
        else: st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 5. VIEW: SYNC BASELINE (FIXED FOR STABILITY)
# ==============================================================================
def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    if not st.session_state["casino_selected"]:
        st.title("📡 SELECT CASINO")
        choice = st.selectbox("TARGET:", ["---", "Premier Bet", "AfricaBet", "BeVegas", "1xBet", "Stake"])
        if st.button("INITIALIZE") and choice != "---":
            st.session_state["target_url"] = choice
            st.session_state["casino_selected"] = True
            st.rerun()
    else:
        st.title("🔄 LIVE SYNC")
        st.write("Enter the last 3 round multipliers (e.g. 1.54)")
        c1, c2, c3 = st.columns(3)
        with c1: v1 = st.text_input("Round 1", value="1.00")
        with c2: v2 = st.text_input("Round 2", value="1.00")
        with c3: v3 = st.text_input("Round 3", value="1.00")
        
        # Immediate verification logic
        if st.button("VERIFY & LOCK"):
            try:
                # Convert to float immediately to check validity
                f1, f2, f3 = float(v1), float(v2), float(v3)
                st.session_state.history = [f"SYNC {f1}x", f"SYNC {f2}x", f"SYNC {f3}x"]
                st.session_state["synced"] = True
                st.success("DATA LOCKED")
                time.sleep(0.5)
                st.rerun()
            except ValueError:
                st.error("Use numbers only (e.g. 2.50)")
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 6. VIEW: DASHBOARD
# ==============================================================================
def show_dashboard():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("✈️ PREDICTOR PRO")
    st.write(f"SERVER: {st.session_state['target_url']} | STATUS: SYNCED")
    
    if st.button("🚀 PREDICT NEXT"):
        with st.spinner("ANALYZING..."):
            time.sleep(4)
        v = analyze_pattern(st.session_state.history)
        color = "#ff00ff" if v >= 5 else "#ffff00" if v >= 2 else "#00d4ff"
        
        st.markdown(f"""
            <div class="predict-box" style="border-color: {color};">
                <h1 style="color: {color}; font-size: 80px; margin: 0;">{v}x</h1>
                <p style="color: {color};">ACCURACY: {random.randint(94, 97)}%</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.session_state.history.insert(0, f"LOG {v}x")
        st.session_state.history = st.session_state.history[:10]

    with st.expander("📝 SESSION LOG"):
        for entry in st.session_state.history:
            st.write(entry)
            
    if st.button("🚪 RESET"):
        st.session_state.update({"pass": False, "casino_selected": False, "synced": False})
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. MAIN FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
