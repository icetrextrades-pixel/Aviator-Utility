import streamlit as st
import numpy as np
import math
import os
from datetime import datetime
import pytz
from supabase import create_client, Client

# ==============================================================================
# 1. SUPABASE CLIENT & AUTH CONFIG
# ==============================================================================
SUPABASE_URL = os.environ.get("VITE_SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("VITE_SUPABASE_ANON_KEY", "")

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase()

ADMIN_EMAIL = "icetrextrades@gmail.com"
ADMIN_WHATSAPP = "+263779174062"

KNOWN_USERS = {
    "icetrex": "icetrex@aviator.app",
    "austin": "austin@aviator.app",
    "biko": "biko@aviator.app",
}

if "pass" not in st.session_state: st.session_state["pass"] = False
if "user" not in st.session_state: st.session_state["user"] = ""
if "user_email" not in st.session_state: st.session_state["user_email"] = ""
if "casino" not in st.session_state: st.session_state["casino"] = "AFRICABET"
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "AVI10"
if "auth_mode" not in st.session_state: st.session_state["auth_mode"] = "login"
if "current_signal" not in st.session_state: st.session_state["current_signal"] = None
if "signal_anim_state" not in st.session_state: st.session_state["signal_anim_state"] = "idle"

st.set_page_config(page_title="AVI10 NEURAL MATRIX", layout="centered", initial_sidebar_state="collapsed")

# ==============================================================================
# 2. STRATEGY CONFIGURATIONS
# ==============================================================================
# Each tab gets a distinct prediction personality.
# min_target / max_target clamp the final signal.
# boost_multiplier amplifies the raw target when a boost fires.
# boost_threshold is the percentile above which a boost triggers.
# blend_recent controls how much weight recent actuals get vs raw math.
STRATEGIES = {
    "PREDICTOR": {
        "min_target": 1.10,
        "max_target": 2.00,
        "boost_multiplier": 1.15,
        "boost_threshold": 0.80,
        "blend_recent": 0.40,
        "tagline": "SAFE & STEADY",
        "accent_color": "#3b82f6",
    },
    "MR CRUSHER": {
        "min_target": 2.00,
        "max_target": 5.00,
        "boost_multiplier": 1.50,
        "boost_threshold": 0.65,
        "blend_recent": 0.20,
        "tagline": "HIGH ROLLER",
        "accent_color": "#ef4444",
    },
    "AVI10": {
        "min_target": 1.40,
        "max_target": 3.50,
        "boost_multiplier": 1.30,
        "boost_threshold": 0.72,
        "blend_recent": 0.30,
        "tagline": "BALANCED MODE",
        "accent_color": "#10b981",
    },
}

# ==============================================================================
# 3. DATABASE FUNCTIONS (SUPABASE)
# ==============================================================================
def fetch_live_history(casino_name: str, limit: int = 50) -> list:
    try:
        resp = supabase.table("round_history") \
            .select("multiplier") \
            .eq("casino", casino_name) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        if resp.data:
            return [f"{row['multiplier']:.2f}x" for row in resp.data]
    except Exception:
        pass
    return ["1.50x", "2.10x", "1.15x", "1.80x", "1.30x", "2.50x", "1.10x", "1.60x", "3.20x", "1.05x"]

def insert_round_result(casino_name: str, multiplier: float) -> bool:
    try:
        supabase.table("round_history") \
            .insert({"casino": casino_name, "multiplier": multiplier}) \
            .execute()
        resolve_pending_signals(casino_name, multiplier)
        return True
    except Exception:
        return False

def get_round_count(casino_name: str) -> int:
    try:
        resp = supabase.table("round_history") \
            .select("id", count="exact") \
            .eq("casino", casino_name) \
            .execute()
        return resp.count or 0
    except Exception:
        return 0

def save_prediction(casino_name: str, strategy: str, predicted: float):
    try:
        supabase.table("signal_history") \
            .insert({
                "casino": casino_name,
                "strategy": strategy,
                "predicted_multiplier": round(predicted, 2),
            }) \
            .execute()
    except Exception:
        pass

def resolve_pending_signals(casino_name: str, actual: float):
    """Mark the oldest unresolved prediction for this casino as hit or miss."""
    try:
        resp = supabase.table("signal_history") \
            .select("id, predicted_multiplier") \
            .eq("casino", casino_name) \
            .is_("resolved_at", "null") \
            .order("created_at", desc=False) \
            .limit(1) \
            .execute()
        if resp.data:
            row = resp.data[0]
            hit = float(row["predicted_multiplier"]) <= actual
            supabase.table("signal_history") \
                .update({
                    "actual_multiplier": actual,
                    "hit": hit,
                    "resolved_at": datetime.now(pytz.UTC).isoformat(),
                }) \
                .eq("id", row["id"]) \
                .execute()
    except Exception:
        pass

def get_accuracy_stats(casino_name: str, strategy: str) -> dict:
    """Return hit rate stats for a given casino + strategy."""
    try:
        resp = supabase.table("signal_history") \
            .select("hit") \
            .eq("casino", casino_name) \
            .eq("strategy", strategy) \
            .not_.is_("hit", "null") \
            .execute()
        total = len(resp.data) if resp.data else 0
        hits = sum(1 for r in resp.data if r["hit"]) if resp.data else 0
        return {"total": total, "hits": hits, "rate": round(hits / total * 100) if total > 0 else 0}
    except Exception:
        return {"total": 0, "hits": 0, "rate": 0}

def get_recent_signals(casino_name: str, strategy: str, limit: int = 3) -> list:
    """Fetch recent resolved signals for display in the recalibration box."""
    try:
        resp = supabase.table("signal_history") \
            .select("predicted_multiplier, actual_multiplier, hit") \
            .eq("casino", casino_name) \
            .eq("strategy", strategy) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return resp.data if resp.data else []
    except Exception:
        return []

# ==============================================================================
# 4. STOCHASTIC MATH ENGINE
# ==============================================================================

def hill_estimator(arr: np.ndarray, k: int = None) -> float:
    sorted_desc = np.sort(arr)[::-1]
    n = len(sorted_desc)
    if n < 5:
        return 2.0
    if k is None:
        k = max(5, n // 4)
    k = min(k, n - 1)
    top_k = sorted_desc[:k]
    threshold = sorted_desc[k]
    if threshold <= 0:
        return 2.0
    ratios = np.log(top_k / threshold)
    valid = ratios[ratios > 0]
    if len(valid) == 0:
        return 2.0
    return float(1.0 / np.mean(valid))

def compute_confidence(arr: np.ndarray, mu: float, sigma: float, tail_index: float) -> float:
    n = len(arr)
    if n == 0 or mu <= 0:
        return 50.0
    cv = sigma / mu
    sample_score = min(n / 50.0, 1.0)
    cv_score = max(0.0, 1.0 - min(cv, 1.0))
    tail_score = max(0.0, 1.0 - min(tail_index / 10.0, 1.0))
    confidence = (sample_score * 0.4 + cv_score * 0.35 + tail_score * 0.25) * 100.0
    return float(max(50.0, min(98.0, confidence)))

def estimate_boost_probability(arr: np.ndarray, threshold: float = 2.0) -> float:
    if len(arr) == 0:
        return 0.15
    high_count = int(np.sum(arr >= threshold))
    return float(high_count / len(arr))

def execute_neural_math(history_data):
    try:
        vals = [float(x.replace('x','').strip()) for x in history_data if x.strip()]
        if len(vals) < 3:
            return 1.45, 0.20, 0.0, 2.0, 50.0, 0.15, []
        arr = np.array(vals)
        mu = float(np.mean(arr))
        raw_sigma = float(np.std(arr))
        sigma = max(raw_sigma, 1e-6)
        log_returns = np.diff(np.log(arr))
        momentum = float(np.mean(log_returns)) if len(log_returns) > 0 else 0.0
        tail_index = hill_estimator(arr)
        confidence = compute_confidence(arr, mu, sigma, tail_index)
        boost_prob = estimate_boost_probability(arr)
        recent_actual = [float(v) for v in vals[:3]]
        return mu, sigma, momentum, min(tail_index, 15.0), confidence, boost_prob, recent_actual
    except Exception:
        return 1.45, 0.20, 0.0, 2.0, 50.0, 0.15, []

def generate_signal(mu, sigma, momentum, tail_index, boost_prob, recent_actual, strategy_name: str) -> float:
    """Generate a prediction using the strategy-specific parameters."""
    strat = STRATEGIES[strategy_name]
    uniform_random = np.random.random()
    frechet_jump = abs(np.log(uniform_random)) ** (-1.0 / tail_index)
    raw_target = mu + (sigma * frechet_jump)
    raw_target *= (1.0 + momentum)

    percentile = np.random.random()
    if percentile > strat["boost_threshold"]:
        raw_target *= strat["boost_multiplier"]

    raw_target = max(1.05, raw_target)

    if recent_actual:
        recent_avg = np.mean(recent_actual[-3:])
        blend = strat["blend_recent"]
        final_target = (raw_target * (1.0 - blend)) + (recent_avg * blend)
    else:
        final_target = raw_target

    final_target = max(strat["min_target"], min(strat["max_target"], final_target))
    return float(final_target)

# ==============================================================================
# 5. CSS
# ==============================================================================
LOGIN_CSS = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(5, 5, 8, 0.85), rgba(5, 5, 8, 0.95)),
                    url('https://images.hdqwalls.com/wallpapers/lionel-messi-4k-2020-qt.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .login-container {{
        background: rgba(10, 10, 16, 0.85);
        border: 1px solid #2a1644;
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center;
        max-width: 450px;
        margin: 20px auto;
        box-shadow: 0 0 50px rgba(147, 51, 234, 0.2);
        backdrop-filter: blur(10px);
    }}
    .padlock-wrapper {{
        width: 70px; height: 70px; border-radius: 50%; border: 2px solid #5b21b6;
        margin: 0 auto 20px auto; display: flex; align-items: center; justify-content: center;
        box-shadow: 0 0 20px rgba(91, 33, 182, 0.4);
    }}
    .title-aviator {{ font-size: 30px; font-weight: 900; font-style: italic; color: white; margin: 0; }}
    .title-signals {{ font-size: 30px; font-weight: 900; font-style: italic; color: #a855f7; margin: 0; }}
    .subtext {{ font-size: 10px; letter-spacing: 4px; color: #c084fc; margin-top: 8px; margin-bottom: 25px; font-weight: bold; }}
    .footer-text {{ font-size: 10px; letter-spacing: 2px; color: #9ca3af; margin-top: 25px; text-align: center; font-weight: bold; }}

    div[data-baseweb="input"] {{ background-color: rgba(0,0,0,0.8) !important; border: 1px solid #3b0764 !important; border-radius: 12px !important; }}
    div[data-baseweb="input"] input {{ color: #a855f7 !important; text-align: center !important; font-weight: bold; letter-spacing: 2px; }}

    div[data-testid="stButton"] > button {{
        background: linear-gradient(90deg, #9333ea, #db2777) !important;
        color: white !important; border: none !important; border-radius: 12px !important;
        padding: 12px 0 !important; font-weight: 900 !important; letter-spacing: 1.5px !important;
        width: 100% !important; margin-top: 10px !important; transition: all 0.3s ease;
    }}
    div[data-testid="stButton"] > button:hover {{ box-shadow: 0 0 25px rgba(219, 39, 119, 0.6) !important; }}
    header {{ display: none !important; }}
</style>
"""

DASHBOARD_CSS = f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(3, 8, 5, 0.88), rgba(3, 8, 5, 0.95)),
                    url('https://images.hdqwalls.com/wallpapers/lionel-messi-trophy-4k-hy.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
        font-family: 'Inter', sans-serif;
    }}
    .top-nav {{ display: flex; justify-content: space-between; font-size: 10px; color: #9ca3af; font-weight: bold; margin-bottom: 20px; }}
    .dash-header {{ text-align: center; margin-bottom: 20px; }}
    .dash-title {{ font-size: 28px; font-style: italic; font-weight: 900; margin: 0; color: #ffffff; }}
    .dash-bullets {{ list-style: none; padding: 0; margin: 10px 0; font-size: 10px; font-weight: bold; color: #10b981; letter-spacing: 1px; }}
    .dash-bullets li::before {{ content: "● "; color: #10b981; }}

    div[data-baseweb="select"] > div {{ background-color: rgba(5,5,5,0.9) !important; border: 1px solid #064e3b !important; border-radius: 10px !important; color: white !important;}}
    header {{ display: none !important; }}

    div[data-testid="stHorizontalBlock"] button {{
        background: rgba(5, 5, 5, 0.85) !important;
        color: #9ca3af !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }}
</style>
"""

# ==============================================================================
# 6. SIGNAL CARD RENDERER
# ==============================================================================
def render_signal_card(active_mode: str, signal_value: float, confidence: float,
                       recent_signals: list, accuracy: dict):
    strat = STRATEGIES[active_mode]
    accent = strat["accent_color"]
    tagline = strat["tagline"]
    cat_timezone = pytz.timezone('Africa/Harare')
    current_time = datetime.now(cat_timezone).strftime("%H:%M:%S")

    display_target = f"{signal_value:.2f}X" if signal_value else "1.00X"
    conf_display = f"{int(confidence)}%" if confidence else "---"

    sig_labels = ["S1: ---", "S2: ---", "S3: ---"]
    sig_colors = [accent, accent, accent]
    for i, s in enumerate(recent_signals[:3]):
        hit_icon = "+" if s.get("hit") else "-"
        sig_labels[i] = f"S{i+1}: {s['predicted_multiplier']:.2f}x {hit_icon}"
        sig_colors[i] = "#10b981" if s.get("hit") else "#ef4444"

    remaining = max(15, min(120, int(signal_value * 30))) if signal_value else 0

    acc_total = accuracy["total"]
    acc_rate = accuracy["rate"]
    acc_hits = accuracy["hits"]
    acc_color = "#10b981" if acc_rate >= 60 else ("#f59e0b" if acc_rate >= 40 else "#ef4444")

    html_code = f"""
    <div style="background: rgba(2, 17, 7, 0.92); border: 1px solid #064e3b; border-radius: 25px; padding: 25px; text-align: center; color: white; font-family: sans-serif; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 40px rgba(0,0,0,0.9); backdrop-filter: blur(12px);">

        <h2 style="margin:0; font-weight: 900; font-size: 22px;">
            <span style="color: {accent};">⚡</span> {active_mode} MATRIX BOT <span style="color: {accent};">⚡</span>
        </h2>
        <p style="color: {accent}; font-size: 10px; font-weight: 900; letter-spacing: 3px; margin: 4px 0 0 0;">{tagline}</p>
        <p style="color: #059669; font-size: 11px; font-weight: 900; letter-spacing: 2px; margin-top: 8px; margin-bottom: 20px;">
            ZIMBABWE TIME: <span id="clock-display">{current_time}</span>
        </p>

        <div style="position:relative; width: 190px; height: 190px; margin: 0 auto; display:flex; flex-direction:column; justify-content:center; align-items:center;">
            <div id="ring" style="position:absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid #064e3b; border-top-color: {accent}; transition: all 0.3s; z-index: 1;"></div>
            <div style="position:absolute; width: 110%; height: 110%; border-radius: 50%; background: radial-gradient(circle, {accent}22 0%, rgba(0,0,0,0) 70%); z-index: 0;"></div>

            <p style="color: #059669; font-size: 9px; margin:0; font-weight:900; z-index:2; letter-spacing: 1px;">POTENTIAL TARGET</p>
            <h1 id="target-display" style="font-size: 50px; margin:-5px 0 0 0; font-weight:900; z-index:2; color: white;">{display_target}</h1>
        </div>

        <!-- ACCURACY TRACKER -->
        <div style="background: rgba(1, 20, 9, 0.9); border: 1px solid {acc_color}; border-radius: 12px; padding: 12px; margin-top: 15px; text-align: center;">
            <p style="color: {acc_color}; font-size: 9px; font-weight: 900; letter-spacing: 1.5px; margin: 0 0 6px 0;">
                PREDICTION ACCURACY
            </p>
            <div style="display: flex; justify-content: space-around; font-family: monospace; font-size: 14px; font-weight: bold;">
                <span style="color: {acc_color};">{acc_rate}%</span>
                <span style="color: #9ca3af; font-size: 10px; padding-top: 3px;">{acc_hits}/{acc_total} HITS</span>
            </div>
        </div>

        <!-- PAST 3 SIGNALS RECALIBRATION BOX -->
        <div style="background: rgba(1, 20, 9, 0.9); border: 1px dashed #059669; border-radius: 12px; padding: 12px; margin-top: 15px; text-align: center;">
            <p style="color: #10b981; font-size: 9px; font-weight: 900; letter-spacing: 1.5px; margin: 0 0 8px 0;">
                TRIPLE-SIGNAL RECALIBRATION HISTORY
            </p>
            <div style="display: flex; justify-content: space-around; font-family: monospace; font-size: 12px; font-weight: bold;">
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: {sig_colors[0]};">{sig_labels[0]}</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: {sig_colors[1]};">{sig_labels[1]}</span>
                <span style="background: #030805; border: 1px solid #1f2937; padding: 4px 10px; border-radius: 6px; color: {sig_colors[2]};">{sig_labels[2]}</span>
            </div>
        </div>

        <div style="background: rgba(3, 8, 5, 0.9); border: 1px solid #1f2937; border-radius: 15px; padding: 18px; margin-top: 15px; text-align: left; font-family: monospace; font-size: 13px;">
            <div style="display:flex; justify-content: space-between; margin-bottom: 12px; font-weight: bold;">
                <span style="color: white;">⏱ REMAINING:</span> <span id="rem-val" style="color: {accent};">{remaining}s</span>
            </div>
            <div style="display:flex; justify-content: space-between; margin-bottom: 12px; font-weight: bold;">
                <span style="color: white;">✅ CONFIDENCE:</span> <span id="conf-val" style="color: {accent};">{conf_display}</span>
            </div>
            <div style="background: #000; padding: 10px; border-radius: 8px; color: #047857; font-size: 10px; font-weight: bold;" id="term-text">
                ● SIGNAL LOCKED • {active_mode} STRATEGY ACTIVE
            </div>
        </div>

        <p style="color: #059669; font-size: 10px; font-weight: 900; letter-spacing: 1px; margin-top: 20px; margin-bottom: 5px;">RECALIBRATE MATRIX</p>
        <p style="color: #6b7280; font-size: 8px; font-weight: bold; letter-spacing: 2px; margin: 0;">NEURAL MATRIX V3.0 • LIVE ACCURACY TRACKING</p>
    </div>

    <script>
    setInterval(() => {{
        const now = new Date();
        const timeStr = now.toTimeString().split(' ')[0];
        const clockElem = document.getElementById('clock-display');
        if (clockElem) clockElem.innerText = timeStr;
    }}, 1000);
    </script>
    <style> @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }} </style>
    """
    st.components.v1.html(html_code, height=700)

# ==============================================================================
# 7. LOGIN & DASHBOARD VIEWS
# ==============================================================================
def show_login():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="login-container">
        <div class="padlock-wrapper">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#a855f7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
        </div>
        <h1 class="title-aviator">AVIATOR <span class="title-signals">SIGNALS</span></h1>
        <p class="subtext">NO RISK NO GAIN</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if st.session_state["auth_mode"] == "login":
            username_input = st.text_input("USERNAME", placeholder="ENTER USERNAME", label_visibility="collapsed")
            password_input = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD", label_visibility="collapsed")

            if st.button("INITIALIZE NEURAL MATRIX"):
                user_clean = username_input.strip().lower()
                pass_clean = password_input.strip()
                if not user_clean or not pass_clean:
                    st.error("Please enter both username and password.")
                    return
                if user_clean in KNOWN_USERS:
                    email = KNOWN_USERS[user_clean]
                elif "@" in user_clean:
                    email = user_clean
                else:
                    email = f"{user_clean}@aviator.app"
                try:
                    resp = supabase.auth.sign_in_with_password({"email": email, "password": pass_clean})
                    if resp.user:
                        st.session_state["pass"] = True
                        st.session_state["user"] = user_clean
                        st.session_state["user_email"] = email
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
                except Exception:
                    st.error("Invalid username or password.")

            switch_col1, switch_col2 = st.columns(2)
            with switch_col1:
                if st.button("CREATE ACCOUNT", use_container_width=True):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()
            with switch_col2:
                st.info("Existing? Sign in above.", icon="ℹ️")
        else:
            new_user = st.text_input("NEW USERNAME", placeholder="CHOOSE A USERNAME", label_visibility="collapsed")
            new_email = st.text_input("EMAIL", placeholder="ENTER YOUR EMAIL", label_visibility="collapsed")
            new_pass = st.text_input("NEW PASSWORD", type="password", placeholder="CHOOSE A PASSWORD", label_visibility="collapsed")
            confirm_pass = st.text_input("CONFIRM PASSWORD", type="password", placeholder="CONFIRM PASSWORD", label_visibility="collapsed")

            if st.button("CREATE ACCOUNT"):
                user_clean = new_user.strip().lower()
                email_clean = new_email.strip()
                pass_clean = new_pass.strip()
                confirm_clean = confirm_pass.strip()
                if not user_clean or not email_clean or not pass_clean:
                    st.error("All fields are required.")
                    return
                if pass_clean != confirm_clean:
                    st.error("Passwords do not match.")
                    return
                if "@" not in email_clean:
                    st.error("Please enter a valid email address.")
                    return
                try:
                    resp = supabase.auth.sign_up({"email": email_clean, "password": pass_clean})
                    if resp.user:
                        st.success("Account created! You can now sign in.")
                        st.session_state["auth_mode"] = "login"
                        st.rerun()
                    else:
                        st.error("Could not create account. Please try again.")
                except Exception as e:
                    err_msg = str(e)
                    if "already" in err_msg.lower() or "registered" in err_msg.lower():
                        st.error("An account with this email already exists.")
                    else:
                        st.error("Sign-up failed: please try again.")

            if st.button("BACK TO LOGIN", use_container_width=True):
                st.session_state["auth_mode"] = "login"
                st.rerun()

    st.markdown(f'<p class="footer-text">AUTHORIZED ACCESS ONLY • CONTACT: {ADMIN_EMAIL}</p>', unsafe_allow_html=True)

def show_dashboard():
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="top-nav">
        <div>🖧 CPU: 14% &nbsp;&nbsp; ⚗ USER: <span style="color:#10b981;">{st.session_state['user'].upper()}</span></div>
        <div><span style="border: 1px solid #1f2937; padding: 3px 8px; border-radius: 5px;">💾 SAVE WORK</span> &nbsp; <span style="color: #10b981;">📶 LIVE SYNC</span></div>
    </div>
    """, unsafe_allow_html=True)

    active_tab = st.session_state["active_tab"]
    strat = STRATEGIES[active_tab]

    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("PREDICTOR", use_container_width=True):
            st.session_state["active_tab"] = "PREDICTOR"
            st.session_state["current_signal"] = None
            st.rerun()
    with t2:
        if st.button("MR CRUSHER", use_container_width=True):
            st.session_state["active_tab"] = "MR CRUSHER"
            st.session_state["current_signal"] = None
            st.rerun()
    with t3:
        if st.button("AVI10", use_container_width=True):
            st.session_state["active_tab"] = "AVI10"
            st.session_state["current_signal"] = None
            st.rerun()

    st.markdown(f"""
    <div class="dash-header" style="margin-top: 15px;">
        <h1 class="dash-title">{active_tab} NEURAL</h1>
        <p style="color: {strat['accent_color']}; font-size: 12px; font-weight: 900; letter-spacing: 2px; margin: 5px 0 0 0;">{strat['tagline']}</p>
        <ul class="dash-bullets">
            <li>NO RISK NO GAIN</li>
            <li>THE KEY TO SUCCESS IS A LONG JOURNEY</li>
            <li>NEURAL MATRIX V3.0</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    colA, colB = st.columns([4, 1])
    with colA:
        selected_casino = st.selectbox("CASINO", ["AFRICABET", "1XBET", "PREMIER BET"], label_visibility="collapsed")
        if selected_casino != st.session_state["casino"]:
            st.session_state["casino"] = selected_casino
            st.session_state["current_signal"] = None
        st.session_state["casino"] = selected_casino
    with colB:
        if st.button("LOGOUT"):
            try:
                supabase.auth.sign_out()
            except Exception:
                pass
            st.session_state["pass"] = False
            st.session_state["user"] = ""
            st.session_state["user_email"] = ""
            st.rerun()

    st.write("")

    # Fetch data and compute math
    live_history = fetch_live_history(st.session_state["casino"])
    round_count = get_round_count(st.session_state["casino"])
    mu, sigma, momentum, tail_index, confidence, boost_prob, recent_actual = execute_neural_math(live_history)

    # Generate signal button
    gen_col1, gen_col2 = st.columns([3, 1])
    with gen_col1:
        if st.button("GENERATE SIGNAL", use_container_width=True, type="primary"):
            signal = generate_signal(mu, sigma, momentum, tail_index, boost_prob, recent_actual, active_tab)
            st.session_state["current_signal"] = signal
            save_prediction(st.session_state["casino"], active_tab, signal)
            st.rerun()
    with gen_col2:
        strat_label = f"{strat['min_target']:.1f}-{strat['max_target']:.1f}x"
        st.markdown(f"""
        <div style="text-align: center; padding-top: 8px;">
            <p style="color: #6b7280; font-size: 9px; font-weight: bold; margin: 0;">TARGET RANGE</p>
            <p style="color: {strat['accent_color']}; font-size: 14px; font-weight: 900; margin: 2px 0 0 0;">{strat_label}</p>
        </div>
        """, unsafe_allow_html=True)

    # Fetch accuracy and recent signals
    accuracy = get_accuracy_stats(st.session_state["casino"], active_tab)
    recent_sigs = get_recent_signals(st.session_state["casino"], active_tab)

    # Render the signal card
    current_signal = st.session_state.get("current_signal") or 1.00
    render_signal_card(active_tab, current_signal, confidence, recent_sigs, accuracy)

    # --------------------------------------------------------------------------
    # ROUND INPUT SECTION
    # --------------------------------------------------------------------------
    st.write("")
    st.markdown("""
    <div style="background: rgba(2, 17, 7, 0.92); border: 1px solid #064e3b; border-radius: 15px; padding: 20px; text-align: center; max-width: 500px; margin: 0 auto;">
        <h4 style="color: #10b981; margin: 0 0 5px 0; font-size: 14px; font-weight: 900;">📋 LOG ROUND RESULT</h4>
        <p style="color: #6b7280; font-size: 10px; margin-bottom: 15px;">Enter the actual multiplier — this resolves your last prediction and improves future signals</p>
    </div>
    """, unsafe_allow_html=True)

    input_col1, input_col2, input_col3 = st.columns([3, 2, 2])
    with input_col1:
        round_multiplier = st.number_input(
            "MULTIPLIER", min_value=1.00, max_value=100.00, value=1.50, step=0.05, format="%.2f",
            label_visibility="collapsed"
        )
    with input_col2:
        if st.button("LOG ROUND", use_container_width=True):
            if insert_round_result(st.session_state["casino"], float(round_multiplier)):
                st.success(f"Logged {round_multiplier:.2f}x — prediction accuracy updated")
                st.rerun()
            else:
                st.error("Failed to log round. Please try again.")
    with input_col3:
        st.markdown(f"""
        <div style="text-align: center; padding-top: 8px;">
            <p style="color: #10b981; font-size: 18px; font-weight: 900; margin: 0;">{round_count}</p>
            <p style="color: #6b7280; font-size: 9px; font-weight: bold; margin: 2px 0 0 0;">ROUNDS LOGGED</p>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # APK & ADMIN BOXES
    # --------------------------------------------------------------------------
    st.write("")
    box_col1, box_col2 = st.columns(2)

    with box_col1:
        st.markdown(f"""
        <div style="background: rgba(10, 10, 16, 0.9); border: 1px solid #2a1644; border-radius: 15px; padding: 15px; text-align: center;">
            <h4 style="color: #a855f7; margin: 0 0 5px 0; font-size: 14px; font-weight: 900;">📲 DOWNLOAD APK</h4>
            <p style="color: #9ca3af; font-size: 10px; margin-bottom: 12px;">Get the official Android app package for mobile execution.</p>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            label="DOWNLOAD MATRIX APK",
            data=b"ICETREX_NEURAL_MATRIX_V2_APK_BINARY",
            file_name="Icetrex_Aviator_Matrix_v2.apk",
            mime="application/vnd.android.package-archive",
            use_container_width=True
        )

    with box_col2:
        st.markdown(f"""
        <div style="background: rgba(2, 17, 7, 0.9); border: 1px solid #064e3b; border-radius: 15px; padding: 15px; text-align: center;">
            <h4 style="color: #10b981; margin: 0 0 5px 0; font-size: 14px; font-weight: 900;">👤 ADMIN INFORMATION</h4>
            <p style="color: #ffffff; font-size: 11px; margin: 3px 0; font-weight: bold;">📧 Email: <span style="color:#10b981;">{ADMIN_EMAIL}</span></p>
            <p style="color: #ffffff; font-size: 11px; margin: 3px 0; font-weight: bold;">💬 WhatsApp: <span style="color:#10b981;">{ADMIN_WHATSAPP}</span></p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 8. ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
else:
    show_dashboard()
