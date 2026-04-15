import streamlit as st
import time
import hashlib
import random

# --- 1. APP CONFIG ---
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# --- 2. THE MASTER LOCK (HARDCODED) ---
# Username: Icetrex
# Key: ADMIN-KING
ADMIN_HASH = "7390977461993478957814408365123956636733560731674483861250278783"

# --- 3. INITIALIZE SESSION STATES ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_state" not in st.session_state:
    st.session_state.app_state = "READY"
if "current_val" not in st.session_state:
    st.session_state.current_val = 1.00

# --- 4. SECURE LOGIN INTERFACE ---
def check_access():
    if not st.session_state.authenticated:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), 
                            url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
                background-size: cover;
            }
            .auth-container {
                background-color: rgba(5, 5, 5, 0.98);
                padding: 40px; border-radius: 15px; border: 2px solid #00ff00;
                text-align: center;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("🛡️ ICETREX ADMIN LOGIN")
        
        user_in = st.text_input("👤 ADMIN USERNAME")
        key_in = st.text_input("🔑 PRODUCT KEY", type="password")
        
        if st.button("AUTHORIZE ACCESS", use_container_width=True):
            hashed_key = hashlib.sha256(key_in.encode()).hexdigest()
            
            # THE FRESH START CHECK
            if user_in == "Icetrex" and hashed_key == ADMIN_HASH:
                st.session_state.authenticated = True
                st.session_state.user_name = user_in
                st.success("Admin Verified. Welcome back, Osmando.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Access Denied: Credentials do not match Admin Database.")
        
        st.markdown("<br><a style='color:#00ff00;' href='mailto:icetrextrades@gmail.com'>Support: icetrextrades@gmail.com</a>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 5. THE BOT ENGINE (PREDICTION LOGIC) ---
if check_access():
    st.markdown("""
        <style>
        .stApp { background-color: #050505; }
        .main-box {
            background-color: rgba(0, 0, 0, 0.9);
            padding: 30px; border-radius: 20px; border: 1px solid #00ff00; text-align: center;
        }
        .prediction-text { font-size: 80px; font-weight: bold; color: #00ff00; text-shadow: 0 0 20px #00ff00; }
        </style>
        """, unsafe_allow_html=True)

    def get_signal():
        chance = random.randint(1, 100)
        if chance > 92: return round(random.uniform(10.0, 48.0), 2), "🔥 PINK SIGNAL", "magenta"
        elif chance > 60: return round(random.uniform(2.0, 4.5), 2), "✅ GOLDEN ENTRY", "#00ff00"
        else: return round(random.uniform(1.1, 1.9), 2), "⚡ BLUE SCALP", "cyan"

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.write(f"SESSION ACTIVE: **{st.session_state.user_name}**")
    st.title("🌿 ICETREX PRO V.12")
    
    if st.session_state.app_state == "READY":
        st.write("### Awaiting Next Flight...")
        if st.button("🚀 START TAKEOFF (SYNC)"):
            val, lab, col = get_signal()
            st.session_state.current_val = val
            st.session_state.label = lab
            st.session_state.color = col
            st.session_state.app_state = "FLYING"
            st.rerun()

    elif st.session_state.app_state == "FLYING":
        st.markdown(f"""
            <div style="border: 2px solid {st.session_state.color}; border-radius: 15px; padding: 20px;">
                <p style="color: {st.session_state.color};">{st.session_state.label}</p>
                <div class="prediction-text">{st.session_state.current_val}x</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("💥 FLEW AWAY (RESET)"):
            st.session_state.app_state = "READY"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Video Vault remains at the bottom
    st.write("---")
    st.header("📂 Video Evidence Vault")
    uploaded_file = st.file_uploader("Upload winning rounds", type=["mp4", "webm"])
    if uploaded_file:
        st.video(uploaded_file)
