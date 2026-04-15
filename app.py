import streamlit as st
import time
import hashlib
import random

# --- 1. APP CONFIG ---
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# --- 2. THE MASTER LOCK ---
# I've simplified this to direct text for your Fresh Start.
ADMIN_USER = "Icetrex"
ADMIN_KEY = "ADMIN-KING"

# --- 3. INITIALIZE SESSION STATES ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_state" not in st.session_state:
    st.session_state.app_state = "READY"

# --- 4. LOGIN INTERFACE ---
def check_access():
    if not st.session_state.authenticated:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), 
                            url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
                background-size: cover;
            }
            .auth-box {
                background-color: rgba(10, 10, 10, 0.95);
                padding: 35px; border-radius: 20px; border: 2px solid #00ff00;
                text-align: center; box-shadow: 0 0 25px rgba(0, 255, 0, 0.1);
            }
            .download-section {
                margin-top: 25px;
                padding-top: 25px;
                border-top: 1px solid #222;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="auth-box">', unsafe_allow_html=True)
        st.title("🛡️ ICETREX CENTRAL")
        st.markdown("<p style='color:#777; font-size:14px;'>Authorized Personnel Only</p>", unsafe_allow_html=True)
        
        # Identity Inputs
        u_in = st.text_input("👤 USERNAME").strip()
        k_in = st.text_input("🔑 PRODUCT KEY", type="password").strip()
        
        if st.button("UNLOCK SYSTEM", use_container_width=True):
            # Using your specific hardcoded credentials
            if u_in == "Icetrex" and k_in == "ADMIN-KING":
                st.session_state.authenticated = True
                st.session_state.user_name = u_in
                st.success("Access Granted. Syncing...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Authentication Failed: Integrity Mismatch")

        # --- MOBILE DISTRIBUTION SECTION ---
        st.markdown('<div class="download-section">', unsafe_allow_html=True)
        st.write("📲 **Download Mobile Edition**")
        
        # YOUR VERIFIED GITHUB LINK
        apk_url = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"
        
        st.markdown(f'''
            <a href="{apk_url}" target="_blank" style="text-decoration:none;">
                <button style="width:100%; height:50px; background-color:#00ff00; color:black; border-radius:12px; font-weight:bold; border:none; cursor:pointer; font-size:16px; box-shadow: 0 4px 15px rgba(0,255,0,0.3);">
                    📥 INSTALL APP-RELEASE.APK
                </button>
            </a>
        ''', unsafe_allow_html=True)
        st.markdown("<p style='color:#555; font-size:11px; margin-top:10px;'>V1.12 Build | E2E Encrypted</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br><a style='color:#00ff00; font-size:12px; text-decoration:none;' href='mailto:icetrextrades@gmail.com'>Contact: icetrextrades@gmail.com</a>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 5. MAIN BOT CODE ---
if check_access():
    st.markdown("""
        <style>
        .stApp { background-color: #050505; color: white; }
        .main-box {
            background-color: rgba(20, 20, 20, 0.9);
            padding: 30px; border-radius: 20px; border: 1px solid #00ff00; text-align: center;
        }
        .prediction-text { font-size: 85px; font-weight: bold; color: #00ff00; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.write(f"Logged in: **{st.session_state.user_name}**")
    st.title("🌿 ICETREX PRO V.12")
    
    # Prediction Engine
    if st.session_state.app_state == "READY":
        if st.button("🚀 START TAKEOFF"):
            # Logic for probability
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
                <p style="color:{st.session_state.color}; font-weight:bold;">{st.session_state.label}</p>
                <div class="prediction-text">{st.session_state.current_val}x</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💥 RESET"):
            st.session_state.app_state = "READY"
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)
