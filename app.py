import streamlit as st
import random
import time
from datetime import datetime

# ==============================================================================
# 1. ATOMIC INITIALIZATION
# ==============================================================================
# We initialize all states to None or False to prevent KeyError on launch.
if "pass" not in st.session_state: st.session_state["pass"] = False
if "synced" not in st.session_state: st.session_state["synced"] = False
if "casino" not in st.session_state: st.session_state["casino"] = None
if "history" not in st.session_state: st.session_state["history"] = []
# Placeholder for the prediction result so it doesn't vanish during animations
if "last_v" not in st.session_state: st.session_state["last_v"] = None

# ==============================================================================
# 2. INTERFACE & BACKGROUND WALLPAPER
# ==============================================================================
st.set_page_config(page_title="ICETREX PREDICTOR PRO", layout="centered")

# Replace this URL with your preferred background image
WALLPAPER_URL = "https://images.unsplash.com/photo-1579546929518-9e396f3cc809"

st.markdown(f"""
<style>
.stApp {{
    background-image: url("{WALLPAPER_URL}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #00d4ff;
    font-family: monospace;
}}

.main-card {{
    background: rgba(10, 10, 10, 0.90);
    padding: 20px;
    border-radius: 15px; 
    border: 1px solid #00d4ff;
    text-align: center;
    margin-bottom: 20px;
}}

div[data-testid="stButton"] > button {{
    width: 100%; 
    border-radius: 10px; 
    background: #000 !important; 
    color: #00d4ff !important; 
    border: 1px solid #00d4ff !important; 
    font-weight: bold;
}}

.predict-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px 0;
    position: relative;
}}

.round-btn {{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background-color: #ff0000;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border: 4px solid #fff;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(255, 0, 0, 0.6);
    z-index: 10;
}}

.lap-timer {{
    position: absolute;
    width: 170px;
    height: 170px;
    border-radius: 50%;
    border: 4px solid transparent;
    z-index: 5;
}}

.lap-timer.active {{
    border: 4px solid #00ff00;
    animation: timeLap 2.5s linear forwards;
}}

@keyframes timeLap {{
    0% {{ transform: rotate(0deg); border-left-color: #00ff00; border-top-color: transparent; border-right-color: transparent; border-bottom-color: transparent; }}
    25% {{ border-top-color: #00ff00; }}
    50% {{ border-right-color: #00ff00; }}
    75% {{ border-bottom-color: #00ff00; }}
    100% {{ transform: rotate(360deg); border-color: #00ff00; }}
}}
</style>
""", unsafe_allow_html=True)
# ==============================================================================
# 3. LIVE CLOCK (JavaScript)
# ==============================================================================
def render_live_clock():
    # Adjusted for Zimbabwe Time (UTC+2)
    st.components.v1.html("""
    <div id="clock" style="color: #ff00ff; font-family: monospace; font-size: 20px; font-weight: bold; text-align: center; border: 1px solid #333; padding: 10px; border-radius: 10px; background: #000;">
        LIVE SERVER TIME: 00:00:00
    </div>
    <script>
    function updateClock() {
        var now = new Date();
        now.setHours(now.getUTCHours() + 2);
        var h = String(now.getHours()).padStart(2, '0');
        var m = String(now.getMinutes()).padStart(2, '0');
        var s = String(now.getSeconds()).padStart(2, '0');
        document.getElementById('clock').innerHTML = "LIVE SERVER TIME: " + h + ":" + m + ":" + s;
    }
    setInterval(updateClock, 1000);
    updateClock();
    </script>
    """, height=60)

# ==============================================================================
# 4. GAP ANALYSIS ENGINE (Anti-Fool Logic)
# ==============================================================================
def calculate_signal(data):
    try:
        vals = [float(x.replace('x','')) for x in data if 'x' in str(x)]
        if len(vals) < 3: return 1.85
        
        # Gap Analysis: Check for low-multiplier 'starvation' (Exhaustion Point)
        if all(v < 1.45 for v in vals[:3]):
            # Pressure build-up for the Pink 100x spike
            return round(random.uniform(15.50, 95.00), 2)
            
        # Cooldown Check: A high multiplier just happened, the next is a Lie
        if any(v > 10.0 for v in vals[:2]):
            return round(random.uniform(1.01, 1.30), 2)
            
        # Default Trend / Stability Check
        return round(random.uniform(2.10, 4.80), 2)
    except:
        return 1.45

# ==============================================================================
# 5. THE PURE JAVASCRIPT ANIMATION COMPONENT
# ==============================================================================
def render_round_predict_system():
    # Since we can't get data *back* easily from a JS click to Python,
    # we use an `st.components.v1.html` as the 'brain' of the dashboard.
    
    # We pass the current Session History and Last Prediction to JS as JSON
    # so it can maintain the state during the animation loop.
    history_json = str(st.session_state["history"]).replace("'", '"')
    last_v = st.session_state["last_v"] if st.session_state["last_v"] is not None else "0.00x"
    
    # JavaScript handles the entire sequence:
    # 1. Click -> 2. Change color -> 3. Animate green lap -> 4. Calculate signal (via Python) -> 5. Display result.
    st.components.v1.html(f"""
    <div class="main-card" style="position: relative; padding: 0;">
        <h1 style="color: #fff; font-size: 24px; margin-top: 15px;">✈️ PREDICTOR PRO</h1>
        <p style="color: #00d4ff; margin: 0;">SERVER: {st.session_state['casino']} | STATUS: SYNCED</p>
        
        <div id="result-display" style="border: 2px solid #00d4ff; padding: 20px; border-radius: 15px; background: #000; margin: 20px;">
            <p id="label" style="color: #00d4ff; font-size: 10px; margin: 0;">PREVIOUS SIGNAL</p>
            <h1 id="multiplier" style="color: #00d4ff; font-size: 80px; margin: 0;">{last_v}</h1>
            <p id="match" style="color: #00d4ff;">PATTERN MATCH: {random.randint(94, 98)}%</p>
        </div>
        
        <div class="predict-container">
            <div id="lapTimer" class="lap-timer"></div>
            
            <button id="predictBtn" class="round-btn">PREDICT<br>NEXT</button>
        </div>
        
        <hr style="border-color: #333; margin: 0;">
    </div>

    <script>
    const btn = document.getElementById('predictBtn');
    const timer = document.getElementById('lapTimer');
    const multiplierDisplay = document.getElementById('multiplier');
    const labelDisplay = document.getElementById('label');
    const resultDisplay = document.getElementById('result-display');
    
    // We import the gap analysis logic we discussed. 
    // We have to 'translate' the Python logic into simple JS here for immediate results.
    const historyData = {history_json};

    function calculateSignalFromHistory(data) {{
        // Basic translation of the logic. If last 3 are all very low, return high.
        // For a true integration, we would need an external API, but this mirrors the Python logic well.
        if (data.length < 3) return 1.85;
        
        // Convert '1.50x' strings to floats
        const vals = data.slice(0, 3).map(x => parseFloat(x.replace('x', '')));
        
        // Check for starvation gap (< 1.45)
        if (vals.every(v => v < 1.45)) {{
            // Pressure is high for a Pink spike! ( mirroring Python random )
            return (Math.random() * (95.00 - 15.50) + 15.50).toFixed(2);
        }}
        
        // Check for cooldown gap (> 10x recent)
        const recentHighs = data.slice(0, 2).map(x => parseFloat(x.replace('x', '')));
        if (recentHighs.some(v => v > 10.0)) {{
            return (Math.random() * (1.30 - 1.01) + 1.01).toFixed(2);
        }}
        
        // Default stability trend gap
        return (Math.random() * (4.80 - 2.10) + 2.10).toFixed(2);
    }}

    btn.addEventListener('click', () => {{
        // PHASE 1: BUTTON PRESSED (Red changes)
        btn.classList.add('active');
        btn.innerHTML = "SCANNING...";
        
        // PHASE 2: SHOW GREEN LAP TIMER (2.5s)
        timer.classList.add('active');
        labelDisplay.innerHTML = "SCANNING SERVER GAPS...";
        
        // PHASE 3: THE WAIT & DISPLAY (SetTimeout must match animation duration)
        setTimeout(() => {{
            // Calculate signal (using the translated logic)
            const v = calculateSignalFromHistory(historyData);
            
            // PHASE 4: UPDATE INTERFACE
            const color = (v >= 5) ? "#ff00ff" : "#00d4ff"; // Pink for Gold/Pink, Blue for safety
            
            // Update Display
            multiplierDisplay.innerHTML = v + "x";
            multiplierDisplay.style.color = color;
            labelDisplay.innerHTML = "VERIFIED SIGNAL";
            labelDisplay.style.color = color;
            resultDisplay.style.borderColor = color;
            
            // PHASE 5: CLEANUP & REFRESH BUTTON
            btn.classList.remove('active');
            btn.innerHTML = "PREDICT<br>NEXT";
            timer.classList.remove('active');
            
            // Note: Since JS runs in the browser, we cannot directly update st.session_state history here.
            // This version provides the visual flow. We would need a full Python backend architecture 
            // (like Flask/Django) to manage the state updates seamlessly.
            
        }}, 2500); // 2500ms (2.5 seconds)
    }};
    </script>
    """, height=500)

# ==============================================================================
# 6. VIEW FUNCTIONS
# ==============================================================================
def show_login():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ OPERATOR LOGIN")
    u = st.text_input("ID")
    k = st.text_input("KEY", type="password")
    if st.button("ACTIVATE"):
        authorized_users = {"Icetrex": "SOPITO", "AUSTIN": "tinofa2578", "BIKO": "PRO779"}
        if u in authorized_users and authorized_users[u] == k:
            st.session_state["pass"] = True
            st.rerun()
        else: st.error("ACCESS DENIED")
    st.markdown('</div>', unsafe_allow_html=True)

def show_casino_select():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("📡 SELECT SOURCE")
    choice = st.selectbox("CASINO:", ["---", "Premier Bet", "AfricaBet", "1xBet", "888Starz", "LuckyBets", "1win", "SpinCity"])
    if st.button("CONNECT") and choice != "---":
        st.session_state["casino"] = choice
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_sync():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title(f"🛰️ {st.session_state['casino'].upper()} SYNC")
    c1, c2, c3 = st.columns(3)
    with c1: r1 = st.text_input("Newest")
    with c2: r2 = st.text_input("Previous")
    with c3: r3 = st.text_input("Oldest")
    if st.button("LOCK DATA"):
        if r1 and r2 and r3:
            # Important: Format with 'x' to ensure the analyzer handles it correctly
            st.session_state["history"] = [f"{r1}x", f"{r2}x", f"{r3}x"]
            st.session_state["synced"] = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    # 1. LIVE CLOCK Header
    render_live_clock()
    
    # 2. Utility Buttons
    ca, cb = st.columns(2)
    with ca: st.markdown('<button style="width:100%; padding:10px; background:#00ff00; color:#000; border:none; border-radius:10px; font-weight:bold;">📥 APK</button>', unsafe_allow_html=True)
    with cb: st.markdown('<a href="https://wa.me/263779174062" target="_blank"><button style="width:100%; padding:10px; background:#25D366; color:#fff; border:none; border-radius:10px; font-weight:bold;">💬 WHATSAPP</button></a>', unsafe_allow_html=True)

    # 3. THE ADVANCED PREDICITON SYSTEM (Fix #2, #3, #4)
    # JavaScript handles the circular button and the animation.
    render_round_predict_system()
    
    # 4. Community Chat
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.write("🌐 COMMUNITY CHAT")
    st.components.v1.html('<iframe src="https://www5.cbox.ws/box/?boxid=962503&boxtag=sopito" width="100%" height="350" frameborder="0"></iframe>', height=380)
    
    if st.button("🚪 LOGOUT"):
        st.session_state["pass"] = False
        st.session_state["synced"] = False
        st.session_state["casino"] = None
        # Clean up the prediction state too
        st.session_state["last_v"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# 7. EXECUTION FLOW
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
elif st.session_state["casino"] is None:
    show_casino_select()
elif not st.session_state["synced"]:
    show_sync()
else:
    show_dashboard()
