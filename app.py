import streamlit as st
import time
import random
import hashlib

# --- APP CONFIG & THEME ---
st.set_page_config(page_title="ICETREX PRO + VAULT", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
    }
    .main-box {
        background-color: rgba(0, 0, 0, 0.85);
        padding: 30px;
        border-radius: 20px;
        color: white;
        border: 1px solid #444;
    }
    .stVideo { border-radius: 15px; border: 2px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.markdown('<div class="main-box">', unsafe_allow_html=True)
st.title("🛡️ ICETREX Predictor & Vault")

# --- SECTION 1: THE SYNC TRACKER (Current Code) ---
st.header("🎮 Live Game Sync")
# (Keeping your manual sync logic here)
if 'sync_state' not in st.session_state:
    st.session_state.sync_state = "READY"

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 START TAKEOFF", use_container_width=True):
        st.session_state.sync_state = "FLYING"
with col2:
    if st.button("💥 FLEW AWAY", use_container_width=True):
        st.session_state.sync_state = "READY"

st.write(f"Current Status: **{st.session_state.sync_state}**")

st.divider()

# --- SECTION 2: THE VIDEO EVIDENCE VAULT ---
st.header("📂 Video Evidence Vault")
st.write("Upload your screen recordings here to save your winning rounds.")

uploaded_file = st.file_uploader("Choose a video file (MP4, WebM, MOV)", type=["mp4", "webm", "mov"])

if uploaded_file is not None:
    st.success(f"Successfully loaded: {uploaded_file.name}")
    # Display the video in the app
    st.video(uploaded_file)
    
    # Option to download it back (useful for converting)
    st.download_button(
        label="📥 Download Video from Vault",
        data=uploaded_file,
        file_name=f"ICETREX_WIN_{uploaded_file.name}",
        mime="video/mp4"
    )

st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption("ICETREX V11.0 | Masvingo Innovation Hub Project")
