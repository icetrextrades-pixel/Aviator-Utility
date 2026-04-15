import streamlit as st
import time
import random

# --- 1. APP CONFIG (Must be the very first Streamlit command) ---
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# --- 2. INITIALIZE SESSION STATES ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_state" not in st.session_state:
    st.session_state.app_state = "READY"

# --- 3. MASTER CREDENTIALS ---
ADMIN_USER = "Icetrex"
ADMIN_KEY = "ADMIN-KING"
APK_URL = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"

# --- 4. SECURE GATEWAY ---
def show_login():
    st.markdown("""
        <style>
        .stApp { background: #050505; }
        .auth-box {
            background-color: #0a0a0a;
            padding: 35px; border-radius: 20px; border: 2px solid #00ff00;
            text-align: center; color: white;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="auth-box">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX CENTRAL")
    
    u_in = st.text_input("👤 USERNAME").strip()
    k_in = st.text_input("🔑 PRODUCT KEY", type="password").strip()
    
    if st.button("UNLOCK SYSTEM", use_container_width=True):
        if u_in == ADMIN_USER and k_in == ADMIN_KEY:
            st.session_state.authenticated = True
            st.success("Access Granted.")
            time.sleep(0.5)
            st.rerun() # Only runs ONCE upon success
        else:
            st.error("Invalid Credentials.")

    # Download Section
    st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)
    st.write("📲 **Mobile Edition**")
    st.markdown(f'''
        <a href="{APK_URL}" target="_blank" style="text-decoration:none;">
            <button style="width:100%; height:45px; background-color:#00ff00; color:black; border-radius:10px; font-weight:bold; border:none; cursor:pointer;">
                📥 DOWNLOAD APK
            </button>
        </a>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MAIN APPLICATION LOGIC ---
if not st.session_state.authenticated:
    show_login()
else:
    # --- UI FOR AUTHENTICATED USERS ---
    st.markdown("""
        <style>
        .stApp { background-color: #000; color: white; }
        .main-box {
            background-color: #0a0a0a;
            padding: 30px; border-radius: 20px; border: 1px solid #00ff00; text-align: center;
        }
        .prediction { font-size: 80px; font-weight: bold; color: #00ff00; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.write(f"Logged in as: **{ADMIN_USER}**")
    st.title("🌿 ICETREX PRO V.12")
    
    if st.session_state.app_state == "READY":
        if st.button("🚀 START TAKEOFF"):
            # Signal Logic
            chance = random.randint(1, 100)
            if chance > 90: res, lab, col = round(random.uniform(10.0, 40.0), 2), "🔥 PINK", "magenta"
            elif chance > 50: res, lab, col = round(random.uniform(2.0, 4.0), 2), "✅ GOLD", "#00ff00"
            else: res, lab, col = round(random.uniform(1.2, 1.9), 2), "⚡ BLUE", "cyan"
            
            st.session_state.current_val = res
            st.session_state.label = lab
            st.session_state.color = col
            st.session_state.app_state = "FLYING"
            st.rerun()

    elif st.session_state.app_state == "FLYING":
        st.markdown(f"""
            <div style="border: 2px solid {st.session_state.color}; border-radius: 15px; padding: 20px;">
                <p style="color:{st.session_state.color};">{st.session_state.label}</p>
                <div class="prediction">{st.session_state.current_val}x</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💥 RESET"):
            st.session_state.app_state = "READY"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
