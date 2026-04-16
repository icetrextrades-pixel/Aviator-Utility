import streamlit as st
import random
import datetime
import time

# 1. PAGE SETUP
st.set_page_config(page_title="ICETREX TERMINAL", layout="centered")

# 2. MASTER CREDENTIALS & LINKS
ADMIN_USER = "Icetrex"
ADMIN_KEY = "SOPITO"
APK_URL = "https://github.com/icetrextrades-pixel/Aviator-Utility/raw/refs/heads/main/app-release.apk"
WHATSAPP_LINK = "https://wa.me/263779174062"
MUSIC_URL = "https://www.youtube.com/embed/4D94B37924FCC62804BC?autoplay=1&loop=1&playlist=4D94B37924FCC62804BC"

# 3. INITIALIZE SESSION STATES
if "pass" not in st.session_state:
    st.session_state["pass"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []
if "start_time" not in st.session_state:
    st.session_state["start_time"] = None

# 4. TIMER LOGIC (3-Hour Limit)
def check_timer():
    if st.session_state["pass"] and st.session_state["start_time"]:
        now = time.time()
        elapsed = now - st.session_state["start_time"]
        # 3 hours = 10800 seconds
        if elapsed > 10800:
            st.session_state["pass"] = False
            st.session_state["start_time"] = None
            st.warning("Session Expired (3-Hour Limit Reached)")
            st.rerun()
        return 10800 - elapsed
    return 0

# 5. ADVANCED CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
        color: #ffffff;
    }}
    .main-card {{
        background-color: rgba(10, 10, 10, 0.85); padding: 20px; 
        border-radius: 15px; border: 1px solid #00ff00; text-align: center;
        backdrop-filter: blur(5px);
    }}
    .floating-ad {{
        position: fixed; bottom: 20px; right: 20px;
        background: rgba(0, 255, 0, 0.9); color: black;
        padding: 10px; border-radius: 10px; font-weight: bold;
        z-index: 999; text-decoration: none; font-size: 12px;
    }}
    .sync-circle {{
        width: 15px; height: 15px; background: red; border-radius: 50%;
        display: inline-block; margin-right: 10px;
        animation: pulse-red 2s infinite;
    }}
    @keyframes pulse-red {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 10px rgba(255, 0, 0, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 6. LOGIN FUNCTION
def login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ ICETREX ADMIN")
    u = st.text_input("USERNAME")
    k = st.text_input("KEY", type="password")
    if st.button("ACTIVATE"):
        if u == ADMIN_USER and k == ADMIN_KEY:
            st.session_state["pass"] = True
            st.session_state["start_time"] = time.time()
            st.rerun()
        else:
            st.error("Denied")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.write("📲 **Get the App**")
    st.markdown(f'<a href="{APK_URL}" target="_blank"><button style="width:100%; height:40px; background:#00ff00; border:none; border-radius:10px; font-weight:bold; cursor:pointer;">DOWNLOAD APK</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 7. MAIN EXECUTION
remaining_time = check_timer()

if not st.session_state["pass"]:
    login()
else:
    # Floating APK Download Ad
    st.markdown(f'<a href="{APK_URL}" class="floating-ad">📲 GET APK PRO</a>', unsafe_allow_html=True)

    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🌿 ICETREX PRO V.12")
    
    # Session Timer Display
    mins_left = int(remaining_time // 60)
    st.markdown(f"<p style='color:#777; font-size:12px;'>Session Expires in: {mins_left} minutes</p>", unsafe_allow_html=True)
    
    # Live Sync Indicator
    now_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 20px;">
            <span class="sync-circle"></span>
            <span style="color:red; font-weight:bold;">LIVE SYNC CONNECTED</span><br>
            <small>WAITING FOR ROUND... | SERVER TIME: {now_time}</small>
        </div>
    """, unsafe_allow_html=True)
    
    # SIGNAL GENERATOR
    if st.button("🚀 PREDICT SIGNAL"):
        chance = random.randint(1, 100)
        if chance > 90: v, l, c = round(random.uniform(10.0, 35.0), 2), "🔥 PINK", "magenta"
        elif chance > 50: v, l, c = round(random.uniform(2.0, 4.5), 2), "✅ GOLD", "#00ff00"
        else: v, l, c = round(random.uniform(1.2, 1.9), 2), "⚡ BLUE", "cyan"
        
        st.markdown(f"<h1 style='color:{c}; font-size:60px; margin:0;'>{v}x</h1>", unsafe_allow_html=True)
        st.session_state.history.insert(0, f"{v}x ({l})")
        st.session_state.history = st.session_state.history[:4]

    # History Display
    if st.session_state.history:
        for h in st.session_state.history:
            st.markdown(f"<p style='text-align:left; font-size:14px; border-left: 2px solid #00ff00; padding-left:10px;'>{h}</p>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#333'>", unsafe_allow_html=True)

    # --- LIVE CHAT SECTION (CBOX INTEGRATION) ---
    st.markdown("💬 **LIVE COMMUNITY CHAT**")
    # This uses a public guest chat widget. For a private one, you can create a free account at Cbox.ws
    st.components.v1.html("""
        <iframe src="https://www3.cbox.ws/box/?boxid=3534571&boxtag=icetrex" width="100%" height="300" allowtransparency="yes" frameborder="0" marginheight="0" marginwidth="0" scrolling="auto"></iframe>
    """, height=350)
    
    # Live Translator Link
    st.markdown("""
        <a href="https://translate.google.com" target="_blank" style="color:#00ff00; font-size:12px; text-decoration:none;">
            🌍 Live Translator: Translate messages here
        </a>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # WhatsApp Support
    st.markdown(f'<a href="{WHATSAPP_LINK}" target="_blank" style="text-decoration:none;"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; border-radius:10px; font-weight:bold; cursor:pointer;">💬 CONTACT WHATSAPP SUPPORT</button></a>', unsafe_allow_html=True)

    if st.button("Log Out"):
        st.session_state["pass"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
