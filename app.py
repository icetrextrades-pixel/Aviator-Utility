import streamlit as st
import random

# 1. PAGE SETUP
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# 2. MASTER CREDENTIALS
ADMIN_USER = "Icetrex"
ADMIN_KEY = "ADMIN-KING"
APK_URL = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"

# 3. CSS (Hardcoded to avoid render loops)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-card {
        background-color: #0a0a0a; padding: 20px; 
        border-radius: 15px; border: 1px solid #00ff00; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. THE ONLY WAY TO UNLOCK (Query Parameters)
# This removes the need for 'Session State' which causes the redirect loop
if "pass" not in st.session_state:
    st.session_state["pass"] = False

def login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    u = st.text_input("USERNAME")
    k = st.text_input("KEY", type="password")
    if st.button("UNLOCK"):
        if u == ADMIN_USER and k == ADMIN_KEY:
            st.session_state["pass"] = True
            st.rerun()
        else:
            st.error("Denied")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("📲 **Get the App**")
    st.markdown(f'<a href="{APK_URL}" target="_blank"><button style="width:100%; height:40px; background:#00ff00; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">DOWNLOAD APK</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5. EXECUTION
if not st.session_state["pass"]:
    login()
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO V.12")
    
    # We use a simple checkbox or button toggle for predictions
    if st.button("🚀 GENERATE SIGNAL"):
        chance = random.randint(1, 100)
        if chance > 90: v, l, c = round(random.uniform(10.0, 35.0), 2), "🔥 PINK", "magenta"
        elif chance > 50: v, l, c = round(random.uniform(2.0, 4.5), 2), "✅ GOLD", "#00ff00"
        else: v, l, c = round(random.uniform(1.2, 1.9), 2), "⚡ BLUE", "cyan"
        
        st.markdown(f"<h1 style='color:{c}; font-size:60px;'>{v}x</h1>", unsafe_allow_html=True)
        st.write(f"ENTRY: {l}")
    
    if st.button("Log Out"):
        st.session_state["pass"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
