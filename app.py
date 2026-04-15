import streamlit as st
import time
import random
import hashlib

# --- APP CONFIG & THEME ---
st.set_page_config(page_title="ICETREX LICENSE SYSTEM", layout="centered")

# --- AUTHENTICATION SYSTEM ---
# These are the pre-generated valid keys. You can add more to this list.
# Pro-tip: Give your friend a unique code and add it here.
VALID_KEYS = ["ICE-7742-X", "BETA-2026-PRO", "GZU-STUDENT-99", "ADMIN-KING"]

# --- INITIALIZE SESSION STATES (The Fix) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'app_state' not in st.session_state:
    st.session_state.app_state = "READY"
if 'current_val' not in st.session_state:
    st.session_state.current_val = None
if 'label' not in st.session_state:
    st.session_state.label = ""
if 'color' not in st.session_state:
    st.session_state.color = "white"
    
def check_access():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                            url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
                background-size: cover;
            }
            .auth-container {
                background-color: rgba(20, 20, 20, 0.95);
                padding: 40px;
                border-radius: 15px;
                border: 1px solid #444;
                text-align: center;
                margin-top: 50px;
            }
            .contact-link { color: #00ff00; text-decoration: none; font-weight: bold; }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("🛡️ ICETREX LICENSE VERIFICATION")
        st.write("Please enter your unique product key to unlock the bot.")
        
        user_key = st.text_input("Product Key", type="default", placeholder="XXXX-XXXX-XXXX")
        
        if st.button("Verify License"):
            if user_key in VALID_KEYS:
                st.session_state.authenticated = True
                st.success("Access Granted! Loading Engine...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Product Key. Please contact the administrator.")
        
        st.markdown(f"""
            <br><p style='font-size: 13px; color: #888;'>
            Don't have a key? Contact: <a class='contact-link' href='mailto:icetrextrades@gmail.com'>icetrextrades@gmail.com</a>
            </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- MAIN APPLICATION (Only runs after verification) ---
if check_access():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                        url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
        }
        .main-box {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 30px;
            border-radius: 20px;
            color: white;
            border: 1px solid #333;
            text-align: center;
        }
        .prediction-text {
            font-size: 80px; font-weight: bold; color: #00ff00;
            text-shadow: 0 0 20px #00ff00; margin: 20px 0;
        }
        .stButton>button { width: 100%; height: 60px; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)

    def get_live_signal():
        chance = random.randint(1, 100)
        if chance > 92: return round(random.uniform(10.0, 50.0), 2), "🔥 PINK SIGNAL", "magenta"
        elif chance > 60: return round(random.uniform(2.1, 4.5), 2), "✅ GOLDEN ENTRY", "#00ff00"
        else: return round(random.uniform(1.2, 1.8), 2), "⚡ BLUE SCALP", "cyan"

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.title("🌿 ICETREX Stealth Sync")
    
    if 'app_state' not in st.session_state:
        st.session_state.app_state = "READY"

    if st.session_state.app_state == "READY":
        if st.button("🚀 START TAKEOFF (PREDICT)"):
            st.session_
