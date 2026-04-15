import streamlit as st
import random

# 1. SETUP
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# 2. MASTER CREDENTIALS
ADMIN_USER = "Icetrex"
ADMIN_KEY = "ADMIN-KING"
APK_URL = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"

# 3. STYLES (Ultra-Lightweight for Compatibility)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    .main-card {
        background-color: #0a0a0a; padding: 25px; 
        border-radius: 15px; border: 1px solid #00ff00; text-align: center;
    }
    .prediction-box {
        font-size: 60px; font-weight: bold; margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SESSION STATE INITIALIZATION (No Reruns Needed)
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "READY"

# 5. APP LOGIC
if not st.session_state.authenticated:
    # --- LOGIN SCREEN ---
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    
    # Using a form prevents the "Redirect" loop entirely
    with st.form("login_form"):
        u_in = st.text_input("👤 USERNAME").strip()
        k_in = st.text_input("🔑 PRODUCT KEY", type="password").strip()
        submit = st.form_submit_button("UNLOCK SYSTEM")
        
        if submit:
            if u_in == ADMIN_USER and k_in == ADMIN_KEY:
                st.session_state.authenticated = True
                st.success("Access Granted! Click again to enter.")
            else:
                st.error("Invalid Credentials")

    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)
    st.write("📲 **Download Mobile App**")
    st.markdown(f'<a href="{APK_URL}" target="_blank"><button style="background-color:#00ff00; color:black; height:45px; width:100%; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">📥 DOWNLOAD APK</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- MAIN BOT ---
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write(f"ADMIN: **{ADMIN_USER}**")
    st.title("🌿 ICETREX PRO V.12")

    if st.session_state.app_mode == "READY":
        if st.button("🚀 START TAKEOFF"):
            chance = random.randint(1, 100)
            if chance > 90: 
                st.session_state.v, st.session_state.l, st.session_state.c = round(random.uniform(10.0, 40.0), 2), "🔥 PINK", "magenta"
            elif chance > 50: 
                st.session_state.v, st.session_state.l, st.session_state.c = round(random.uniform(2.0, 4.0), 2), "✅ GOLD", "#00ff00"
            else: 
                st.session_state.v, st.session_state.l, st.session_state.c = round(random.uniform(1.2, 1.9), 2), "⚡ BLUE", "cyan"
            
            st.session_state.app_mode = "FLYING"
            # We don't use rerun here; the page will update on next click/interaction

    if st.session_state.app_mode == "FLYING":
        st.markdown(f"""
            <div style="border: 2px solid {st.session_state.c}; border-radius: 10px; padding: 15px;">
                <p style="color:{st.session_state.c}; font-weight:bold; margin:0;">{st.session_state.l}</p>
                <div class="prediction-box" style="color:{st.session_state.c};">{st.session_state.v}x</div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("💥 RESET ENGINE"):
            st.session_state.app_mode = "READY"

    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state.authenticated = False
