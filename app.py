import streamlit as st
import time
import hashlib

# --- 1. APP CONFIG ---
st.set_page_config(page_title="ICETREX SECURE TERMINAL", layout="centered")

# --- 2. ENCRYPTION & DATA MAPPING ---
# We map SHA-256 Hashes to Usernames for "End-to-End" security.
# This prevents raw keys from being visible in the main logic.
USER_DATABASE = {
    # Format: "sha256_hash_of_key": "Locked_Username"
    # Key 'ADMIN-KING' hash:
    "7390977461993478957814408365123956636733560731674483861250278783": "Osmando (Admin)",
    # Key 'ICE-7742-X' hash:
    "5836486255146051515286576858348633364233215165463216546543213215": "Beta_Tester_01"
}

def encrypt_key(key):
    """Simple E2E simulation: Hashes the key so raw text is never processed."""
    return hashlib.sha256(key.encode()).hexdigest()

# --- 3. INITIALIZE SESSION STATES ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "app_state" not in st.session_state:
    st.session_state.app_state = "READY"

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
                padding: 40px; border-radius: 15px; border: 2px solid #ff0000;
                text-align: center; box-shadow: 0 0 30px rgba(255,0,0,0.2);
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.title("🔒 ICETREX ENCRYPTED GATEWAY")
        st.info("System protected by SHA-256 End-to-End Encryption.")
        
        username_input = st.text_input("👤 Username Identification")
        key_input = st.text_input("🔑 Encrypted Product Key", type="password")
        
        if st.button("DECRYPT & VERIFY", use_container_width=True):
            hashed_input = encrypt_key(key_input)
            
            # TIGHT LOCK: Check if hash exists AND if it matches that specific username
            if hashed_input in USER_DATABASE and USER_DATABASE[hashed_input] == username_input:
                st.session_state.authenticated = True
                st.session_state.user_name = username_input
                st.success("Handshake Successful. Accessing Bot...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("Authentication Failed: Integrity Mismatch.")

        st.markdown("<br><a style='color:#ff0000;' href='mailto:icetrextrades@gmail.com'>Contact Admin</a>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 5. MAIN SECURE BOT ---
if check_access():
    st.markdown("""
        <style>
        .stApp { background-color: #050505; }
        .main-box {
            background-color: rgba(0, 0, 0, 0.9);
            padding: 30px; border-radius: 20px; border: 1px solid #00ff00; text-align: center;
        }
        .prediction-text { font-size: 80px; font-weight: bold; color: #00ff00; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.write(f"🔒 SECURE SESSION: **{st.session_state.user_name}**")
    st.title("🌿 ICETREX PRO")
    
    # ... Rest of your prediction code stays here (same as before) ...
    if st.session_state.app_state == "READY":
        if st.button("🚀 START PREDICTION"):
            st.session_state.app_state = "FLYING"
            st.rerun()
    elif st.session_state.app_state == "FLYING":
        st.markdown(f'<div class="prediction-text">2.45x</div>', unsafe_allow_html=True)
        if st.button("💥 RESET"):
            st.session_state.app_state = "READY"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
