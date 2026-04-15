import streamlit as st
import time
import random
import hashlib

# --- 1. APP CONFIG & THEME ---
st.set_page_config(page_title="ICETREX LICENSE SYSTEM", layout="centered")

# --- 2. INITIALIZE ALL SESSION STATES (Prevents AttributeError) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_state" not in st.session_state:
    st.session_state.app_state = "READY"
if "current_val" not in st.session_state:
    st.session_state.current_val = 1.00
if "label" not in st.session_state:
    st.session_state.label = "WAITING"
if "color" not in st.session_state:
    st.session_state.color = "#ffffff"

# --- 3. LICENSE KEYS ---
# Add your custom keys here
VALID_KEYS = ["ICE-7742-X", "BETA-2026-PRO", "ADMIN-KING", "GZU-PILOT-01"]

# --- 4. AUTHENTICATION FUNCTION ---
def check_access():
    if not st.session_state.authenticated:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                            url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1920&q=80");
                background-size: cover;
            }
            .auth-container {
                background-color: rgba(10, 10, 10, 0.95);
                padding: 40px; border-radius: 15px; border: 1px solid #333;
                text-align: center; margin-top: 50px;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("🛡️ ICETREX VERIFICATION")
        st.write("Enter Product Key to Unlock Bot")
        
        user_key = st.text_input("Product Key", type="default", placeholder="XXXX-XXXX-XXXX")
        
        if st.button("Verify License"):
            if user_key in VALID_KEYS:
                st.session_state.authenticated = True
                st.success("License Verified!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Key. Contact icetrextrades@gmail.com")
        
        st.markdown("<br><a style='color:#00ff00;' href='mailto:icetrextrades@gmail.com'>Get Access Key</a>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 5. MAIN APP (Runs only after login) ---
if check_access():
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                        url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
        }
        .main-box {
            background-color: rgba(0, 0, 0, 0.85);
            padding: 30px; border-radius: 20px; border: 1px solid #333; text-align: center;
        }
        .prediction-text {
            font-size: 80px; font-weight: bold; color: #00ff00;
            text-shadow: 0 0 20px #00ff00; margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True)

    def generate_signal():
        chance = random.randint(1, 100)
        if chance > 90: return round(random.uniform(10.0, 45.0), 2), "🔥 PINK SIGNAL", "magenta"
        elif chance > 60: return round(random.uniform(2.1, 4.0), 2), "✅ GOLDEN ENTRY", "#00ff00"
        else: return round(random.uniform(1.2, 1.8), 2), "⚡ BLUE SCALP", "cyan"

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.title("🌿 ICETREX Stealth Sync")
    
    # State Logic
    if st.session_state.app_state == "READY":
        st.write("### Standby Mode")
        if st.button("🚀 START TAKEOFF (PREDICT)"):
            val, lab, col = generate_signal()
            st.session_state.current_val = val
            st.session_state.label = lab
            st.session_state.color = col
            st.session_state.app_state = "FLYING"
            st.rerun()

    elif st.session_state.app_state == "FLYING":
        st.markdown(f"""
            <div style="border: 2px solid {st.session_state.color}; border-radius: 15px; padding: 20px;">
                <p style="color: {st.session_state.color}; letter-spacing: 2px;">{st.session_state.label}</p>
                <div class="prediction-text">{st.session_state.current_val}x</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💥 FLEW AWAY (RESET)"):
            st.session_state.app_state = "READY"
            st.rerun()
    
    st.markdown(f"<br><small>Support: icetrextrades@gmail.com</small>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Video Vault
    st.write("---")
    st.header("📂 Video Evidence Vault")
    uploaded_file = st.file_uploader("Upload winning rounds", type=["mp4", "webm"])
    if uploaded_file:
        st.video(uploaded_file)
