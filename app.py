import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import math
import os
import re
import time
from datetime import datetime
from urllib.parse import urlparse
import pytz
from supabase import create_client, Client

# Page configuration must be the first Streamlit command.
st.set_page_config(
    page_title="AVI10 NEURAL MATRIX",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ==============================================================================
# 1. SUPABASE CLIENT & AUTH CONFIG
# ==============================================================================
def _get_config_value(*names: str) -> str:
    """Read a setting from environment variables or Streamlit secrets."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()

    try:
        for name in names:
            if name in st.secrets:
                value = st.secrets[name]
                if value:
                    return str(value).strip()
    except Exception:
        pass

    return ""


# Support both conventional Streamlit/Supabase names and the existing Vite names.
SUPABASE_URL = _get_config_value("SUPABASE_URL", "VITE_SUPABASE_URL")
SUPABASE_KEY = _get_config_value(
    "SUPABASE_KEY",
    "SUPABASE_ANON_KEY",
    "SUPABASE_PUBLISHABLE_KEY",
    "VITE_SUPABASE_ANON_KEY",
)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error(
        "Supabase is not configured for this Streamlit deployment. "
        "Add SUPABASE_URL and SUPABASE_KEY (or the existing VITE_SUPABASE_* names) "
        "in Streamlit App Settings → Secrets, then reboot the app."
    )
    st.stop()


def _create_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# Keep the authenticated client isolated to this browser session.
if "supabase_client" not in st.session_state:
    st.session_state["supabase_client"] = _create_supabase_client()

supabase: Client = st.session_state["supabase_client"]

ADMIN_EMAIL = "icetrextrades@gmail.com"
ADMIN_WHATSAPP = "+263779174062"
ADMIN_DISPLAY_PHONE = "0779 174 062"


def normalize_phone_number(value: str) -> str:
    """Convert Zimbabwe local mobile numbers to E.164; preserve other international codes."""
    cleaned = re.sub(r"[^0-9+]", "", value.strip())
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    elif cleaned.startswith("0"):
        cleaned = "+263" + cleaned[1:]
    elif cleaned.startswith("263"):
        cleaned = "+" + cleaned
    elif not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    if not re.fullmatch(r"\+[1-9]\d{7,14}", cleaned):
        raise ValueError("Enter a valid international phone number, for example +263 77 123 4567.")
    return cleaned


KNOWN_USERS = {
    "icetrex": "icetrex@aviator.app",
    "austin": "austin@aviator.app",
    "biko": "biko@aviator.app",
}

if "pass" not in st.session_state: st.session_state["pass"] = False
if "user" not in st.session_state: st.session_state["user"] = ""
if "user_email" not in st.session_state: st.session_state["user_email"] = ""
if "user_id" not in st.session_state: st.session_state["user_id"] = ""
if "pending_signup" not in st.session_state: st.session_state["pending_signup"] = {}
if "refresh_after_round" not in st.session_state: st.session_state["refresh_after_round"] = False
if "casino" not in st.session_state: st.session_state["casino"] = "AFRICABET"
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "AVI10"
if "auth_mode" not in st.session_state: st.session_state["auth_mode"] = "login"
if "auth_notice" not in st.session_state: st.session_state["auth_notice"] = ""
if "signal_generated_at" not in st.session_state: st.session_state["signal_generated_at"] = 0.0
if "auto_signal" not in st.session_state: st.session_state["auto_signal"] = False
if "current_signal" not in st.session_state: st.session_state["current_signal"] = None
if "signal_anim_state" not in st.session_state: st.session_state["signal_anim_state"] = "idle"

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

def insert_round_result(casino_name: str, multiplier: float, strategy: str) -> bool:
    try:
        supabase.table("round_history") \
            .insert({"casino": casino_name, "multiplier": multiplier}) \
            .execute()
        resolve_pending_signals(casino_name, multiplier, strategy)
        return True
    except Exception:
        return False


def get_latest_round_timestamp(casino_name: str) -> float:
    """Return the current user's most recent logged round time for this casino."""
    try:
        resp = supabase.table("round_history") \
            .select("created_at") \
            .eq("casino", casino_name) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        if resp.data:
            value = resp.data[0].get("created_at")
            return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except Exception:
        pass
    return 0.0


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

def resolve_pending_signals(casino_name: str, actual: float, strategy: str):
    """Resolve the oldest outstanding prediction for the casino and mode just logged."""
    try:
        resp = supabase.table("signal_history") \
            .select("id, predicted_multiplier") \
            .eq("casino", casino_name) \
            .eq("strategy", strategy) \
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

def fetch_community_messages(limit: int = 60) -> list:
    """Read the newest community messages visible to signed-in users."""
    response = supabase.table("community_chat_messages") \
        .select("id, user_id, username, message, created_at") \
        .order("created_at", desc=True) \
        .limit(limit) \
        .execute()
    return list(reversed(response.data or []))


def send_community_message(message: str) -> None:
    username = (st.session_state.get("user") or "member")[:40]
    supabase.table("community_chat_messages").insert({
        "user_id": st.session_state["user_id"],
        "username": username,
        "message": message.strip()[:1000],
    }).execute()


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

DASHBOARD_CSS = """
<style>
    :root { --accent: #10b981; --accent-soft: rgba(16,185,129,.16); }
    .stApp {
        background:
          radial-gradient(ellipse at 8% 0%, color-mix(in srgb, var(--accent) 16%, transparent), transparent 38%),
          radial-gradient(ellipse at 100% 80%, rgba(25,54,86,.2), transparent 42%),
          linear-gradient(135deg, #05070d 0%, #080d16 48%, #05070c 100%);
        color: #e9f4ff;
        font-family: Inter, ui-sans-serif, system-ui, sans-serif;
    }
    .stApp:before {
        content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
        opacity: .11; background-image: linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
        background-size: 38px 38px; mask-image: linear-gradient(to bottom, black, transparent 84%);
    }
    [data-testid="stAppViewContainer"] > .main { position: relative; z-index: 1; }
    header { display: none !important; }
    .block-container { max-width: 1160px; padding-top: 1.4rem; padding-bottom: 3rem; }
    .top-nav {
        display:flex; justify-content:space-between; align-items:center; gap:16px;
        padding:10px 14px; margin-bottom:18px; border:1px solid rgba(148,163,184,.18);
        border-left:3px solid var(--accent); background:rgba(7,12,21,.8);
        color:#90a4ba; font:700 10px ui-monospace,monospace; letter-spacing:1.4px;
        box-shadow:0 12px 36px rgba(0,0,0,.28); clip-path:polygon(0 0,99% 0,100% 25%,100% 100%,1% 100%,0 75%);
    }
    .top-nav .live { color:var(--accent); }
    .dash-header { padding:18px 12px 12px; text-align:center; }
    .eyebrow { color:var(--accent); font:800 10px ui-monospace,monospace; letter-spacing:4px; }
    .dash-title { margin:6px 0 0; font-size:clamp(32px,5vw,58px); line-height:.95; font-weight:950; font-style:italic; letter-spacing:-2px; color:#f8fafc; text-shadow:0 0 28px color-mix(in srgb,var(--accent) 35%,transparent); }
    .dash-tagline { margin:12px 0 0; color:#99aabd; font:700 11px ui-monospace,monospace; letter-spacing:2px; }
    .dash-description { max-width:650px; margin:9px auto 0; color:#6f8094; font-size:12px; line-height:1.6; }
    div[data-testid="stHorizontalBlock"] button {
        border:1px solid rgba(148,163,184,.18) !important; background:rgba(8,14,24,.85) !important;
        color:#c7d2df !important; border-radius:4px !important; font-weight:850 !important;
        letter-spacing:1.5px !important; min-height:44px; transition:all .2s ease !important;
    }
    div[data-testid="stHorizontalBlock"] button:hover { border-color:var(--accent) !important; color:white !important; box-shadow:0 0 22px var(--accent-soft) !important; transform:translateY(-1px); }
    div[data-testid="stButton"] button[kind="primary"], div[data-testid="stLinkButton"] a {
        background:linear-gradient(105deg,color-mix(in srgb,var(--accent) 76%,#07101a),color-mix(in srgb,var(--accent) 46%,#111827)) !important;
        border:1px solid color-mix(in srgb,var(--accent) 75%,white) !important; color:#f8fafc !important;
        border-radius:4px !important; font-weight:900 !important; letter-spacing:1.5px !important;
        box-shadow:0 0 25px var(--accent-soft), inset 0 0 18px rgba(255,255,255,.04) !important;
    }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] { background:rgba(4,9,17,.94) !important; border:1px solid rgba(148,163,184,.25) !important; border-radius:4px !important; color:white !important; }
    div[data-baseweb="input"] input { color:#ecf4ff !important; }
    [data-testid="stMetric"] { background:rgba(8,14,24,.82); border:1px solid rgba(148,163,184,.16); border-left:2px solid var(--accent); padding:12px 15px; }
    [data-testid="stMetricLabel"] { color:#8292a5 !important; font:700 10px ui-monospace,monospace !important; letter-spacing:1.5px; }
    [data-testid="stMetricValue"] { color:#f8fafc !important; font-weight:900; }
    [data-testid="stAlert"] { border-radius:4px; }
    .section-label { color:var(--accent); font:800 10px ui-monospace,monospace; letter-spacing:2px; margin:14px 0 8px; }
    .feed-note { border:1px solid rgba(148,163,184,.18); border-left:3px solid var(--accent); background:rgba(7,12,21,.8); padding:12px 15px; color:#aab8c9; font-size:11px; line-height:1.55; }
    .footer-line { display:flex; align-items:center; gap:8px; color:#556477; font:700 9px ui-monospace,monospace; letter-spacing:1.4px; justify-content:center; margin-top:20px; }
    @media (max-width:640px) {
        .block-container { padding-left:1rem; padding-right:1rem; }
        .top-nav { font-size:8px; letter-spacing:.7px; }
        .dash-title { letter-spacing:-1px; }
    }
</style>
"""# ==============================================================================
# 6. SIGNAL CARD RENDERER
# ==============================================================================
def render_signal_card(active_mode: str, signal_value: float, confidence: float,
                       recent_signals: list, accuracy: dict, generated_at: float = 0.0, last_round_at: float = 0.0):
    strat = STRATEGIES[active_mode]
    accent = strat["accent_color"]
    mode_tag = {"PREDICTOR": "01 / LOW-VARIANCE LAB", "AVI10": "10 / NEURAL CORE", "MR CRUSHER": "X / HIGH-IMPACT ENGINE"}[active_mode]
    skin_class = {"PREDICTOR": "skin-predictor", "AVI10": "skin-avi10", "MR CRUSHER": "skin-crusher"}[active_mode]
    display_target = f"{signal_value:.2f}X" if signal_value else "— —"
    confidence_text = f"{int(confidence)}%" if confidence else "—"
    hits = accuracy["hits"]
    total = accuracy["total"]
    rate = accuracy["rate"]
    signal_age = max(0, time.time() - generated_at) if generated_at else 0
    initial_elapsed = max(0, int(time.time() - last_round_at)) if last_round_at else -1
    signal_state = "SIGNAL LOCKED" if generated_at else "AWAITING GENERATION"
    accuracy_color = "#4ade80" if rate >= 60 else ("#fbbf24" if rate >= 40 else "#fb7185")

    recent = []
    for row in recent_signals[:3]:
        if row.get("hit") is None:
            status, row_color = "OPEN", accent
        else:
            status = "HIT" if row.get("hit") else "MISS"
            row_color = "#4ade80" if row.get("hit") else "#fb7185"
        recent.append(f'<span class="mini-signal" style="--row-color:{row_color}">{row["predicted_multiplier"]:.2f}x <b>{status}</b></span>')
    while len(recent) < 3:
        recent.append('<span class="mini-signal muted">NO DATA</span>')

    card = f"""
    <style>
      * {{ box-sizing:border-box; }}
      .instrument {{ --accent:{accent}; color:#eff6ff; position:relative; overflow:hidden; max-width:760px; margin:8px auto 16px; padding:25px 26px 20px; border:1px solid color-mix(in srgb,var(--accent) 55%,#263449); border-top:3px solid var(--accent); background:radial-gradient(ellipse at 50% 0%,color-mix(in srgb,var(--accent) 14%,transparent),transparent 54%),linear-gradient(145deg,rgba(10,18,30,.98),rgba(4,8,15,.98)); box-shadow:0 22px 70px rgba(0,0,0,.55),0 0 35px color-mix(in srgb,var(--accent) 12%,transparent); font-family:Inter,Arial,sans-serif; clip-path:polygon(0 0,97% 0,100% 4%,100% 100%,3% 100%,0 96%); }}
      .instrument:before {{ content:""; position:absolute; inset:0; pointer-events:none; opacity:.12; background:repeating-linear-gradient(0deg,transparent 0 4px,rgba(255,255,255,.08) 5px); }}
      .instrument:after {{ content:""; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,var(--accent),transparent); }}
      .instrument.skin-predictor {{ background:radial-gradient(ellipse at 50% 0%,rgba(59,130,246,.18),transparent 58%),linear-gradient(145deg,rgba(8,17,34,.98),rgba(4,8,15,.98)); }}
      .instrument.skin-predictor .dial-track {{ background:repeating-conic-gradient(from 0deg,rgba(59,130,246,.12) 0 1deg,transparent 1deg 12deg); }}
      .instrument.skin-avi10 {{ background:radial-gradient(ellipse at 50% 0%,rgba(16,185,129,.18),transparent 58%),linear-gradient(145deg,rgba(7,24,23,.98),rgba(4,8,15,.98)); }}
      .instrument.skin-avi10 .dial-orbit {{ border-top-color:#6ee7b7; border-right-color:rgba(16,185,129,.5); }}
      .instrument.skin-crusher {{ background:repeating-linear-gradient(135deg,rgba(239,68,68,.045) 0 2px,transparent 2px 11px),radial-gradient(ellipse at 50% 0%,rgba(239,68,68,.2),transparent 58%),linear-gradient(145deg,rgba(31,9,14,.98),rgba(8,7,13,.98)); }}
      .instrument.skin-crusher .dial-orbit.spin-up {{ animation-duration:1.8s; }}
      .instrument.skin-crusher .dial-orbit {{ border-width:4px; }}
      .instrument.skin-crusher .dial-value {{ text-shadow:0 0 26px rgba(239,68,68,.55); }}
      .instrument-head,.instrument-body,.instrument-foot {{ position:relative; z-index:1; }}
      .instrument-head {{ display:flex; justify-content:space-between; align-items:flex-start; gap:10px; border-bottom:1px solid rgba(148,163,184,.15); padding-bottom:16px; }}
      .instrument-title {{ margin:0; font-size:clamp(17px,3vw,22px); font-weight:950; font-style:italic; letter-spacing:1px; }}
      .instrument-sub {{ color:#8193a8; font:700 9px ui-monospace,monospace; letter-spacing:2px; margin-top:6px; }}
      .live-chip {{ border:1px solid color-mix(in srgb,var(--accent) 45%,transparent); color:var(--accent); background:color-mix(in srgb,var(--accent) 10%,transparent); padding:6px 8px; font:900 9px ui-monospace,monospace; letter-spacing:1px; white-space:nowrap; }}
      .live-chip i {{ display:inline-block; width:6px; height:6px; border-radius:50%; background:var(--accent); margin-right:6px; box-shadow:0 0 10px var(--accent); }}
      .instrument-body {{ display:grid; grid-template-columns:minmax(230px,1fr) minmax(180px,.82fr); align-items:center; gap:15px; padding:20px 0; }}
      .dial-wrap {{ position:relative; display:grid; place-items:center; width:260px; height:260px; margin:auto; }}
      .dial-glow {{ position:absolute; inset:23px; border-radius:50%; background:radial-gradient(circle,color-mix(in srgb,var(--accent) 15%,transparent),transparent 68%); filter:blur(5px); }}
      .dial-track,.dial-orbit,.dial-core {{ position:absolute; border-radius:50%; }}
      .dial-track {{ inset:15px; border:1px solid rgba(148,163,184,.18); background:conic-gradient(from 210deg,transparent 0 9%,color-mix(in srgb,var(--accent) 17%,transparent) 10% 85%,transparent 86%); }}
      .dial-track:before {{ content:""; position:absolute; inset:9px; border-radius:50%; border:1px dashed color-mix(in srgb,var(--accent) 40%,transparent); }}
      .dial-orbit {{ inset:7px; border:3px solid transparent; border-top-color:var(--accent); border-right-color:color-mix(in srgb,var(--accent) 30%,transparent); filter:drop-shadow(0 0 9px var(--accent)); }}
      .dial-orbit.spin-up {{ animation:orbit 2.7s cubic-bezier(.13,.75,.18,1) 1 both; }}
      .dial-orbit:after {{ content:""; position:absolute; width:10px; height:10px; top:-6px; left:50%; border-radius:50%; background:#fff; box-shadow:0 0 12px 4px var(--accent); }}
      .dial-inner {{ position:absolute; inset:28px; border-radius:50%; border:1px solid rgba(148,163,184,.12); animation:reverse-orbit 8s linear infinite; }}
      .dial-inner:after {{ content:""; position:absolute; width:5px; height:5px; right:12%; top:16%; border-radius:50%; background:var(--accent); box-shadow:0 0 10px var(--accent); }}
      .dial-core {{ inset:52px; display:flex; flex-direction:column; justify-content:center; align-items:center; background:radial-gradient(circle at 50% 28%,rgba(30,48,68,.8),rgba(4,8,15,.96) 68%); border:1px solid color-mix(in srgb,var(--accent) 42%,#1e293b); box-shadow:inset 0 0 28px rgba(0,0,0,.7),0 0 26px color-mix(in srgb,var(--accent) 12%,transparent); animation:core-in .55s ease-out both; }}
      .dial-kicker {{ color:#8497aa; font:800 8px ui-monospace,monospace; letter-spacing:2px; }}
      .dial-value {{ margin:5px 0; color:#fff; font-size:clamp(34px,6vw,45px); line-height:1; font-weight:950; letter-spacing:-2px; text-shadow:0 0 22px color-mix(in srgb,var(--accent) 32%,transparent); }}
      .dial-label {{ color:var(--accent); font:900 8px ui-monospace,monospace; letter-spacing:2px; }}
      .dial-stat {{ position:absolute; color:#8293a8; font:800 8px ui-monospace,monospace; letter-spacing:1px; }}
      .dial-stat.left {{ left:0; top:48%; writing-mode:vertical-rl; transform:rotate(180deg); }}
      .dial-stat.right {{ right:0; top:48%; writing-mode:vertical-rl; }}
      .telemetry {{ display:grid; gap:10px; }}
      .telemetry-box {{ padding:12px 13px; border:1px solid rgba(148,163,184,.16); border-left:2px solid var(--accent); background:rgba(4,9,17,.72); }}
      .telemetry-label {{ color:#8190a3; font:800 9px ui-monospace,monospace; letter-spacing:1.4px; }}
      .telemetry-value {{ color:#f1f5f9; font:900 21px ui-monospace,monospace; margin-top:6px; }}
      .telemetry-value em {{ color:var(--accent); font-style:normal; font-size:11px; }}
      .window-track {{ margin-top:8px; height:3px; background:#182333; overflow:hidden; }}
      .sync-fill {{ height:100%; width:34%; background:var(--accent); box-shadow:0 0 10px var(--accent); animation:sync-pulse 2.2s ease-in-out infinite alternate; }}
      .history-head {{ display:flex; justify-content:space-between; align-items:center; margin:6px 0 8px; color:#8190a3; font:800 9px ui-monospace,monospace; letter-spacing:1.3px; }}
      .history-row {{ display:flex; gap:7px; }}
      .mini-signal {{ flex:1; text-align:center; padding:9px 5px; border:1px solid color-mix(in srgb,var(--row-color) 30%,transparent); background:rgba(6,12,20,.8); color:var(--row-color); font:800 10px ui-monospace,monospace; }}
      .mini-signal b {{ display:block; font-size:8px; margin-top:3px; letter-spacing:1px; }}
      .mini-signal.muted {{ color:#516074; border-color:rgba(148,163,184,.12); }}
      .instrument-foot {{ display:flex; justify-content:space-between; gap:10px; align-items:center; border-top:1px solid rgba(148,163,184,.15); padding-top:13px; color:#697b90; font:700 8px ui-monospace,monospace; letter-spacing:1.2px; }}
      .instrument-foot strong {{ color:var(--accent); }}
      @keyframes orbit {{ 0% {{ transform:rotate(-90deg) scale(.92); opacity:.45; }} 68% {{ transform:rotate(1040deg) scale(1.04); opacity:1; }} 100% {{ transform:rotate(1080deg) scale(1); opacity:1; }} }}
      @keyframes reverse-orbit {{ to {{ transform:rotate(-360deg); }} }}
      @keyframes core-in {{ from {{ transform:scale(.84); filter:blur(4px); opacity:.4; }} to {{ transform:scale(1); filter:blur(0); opacity:1; }} }}
      @keyframes sync-pulse {{ from {{ transform:translateX(-10%); opacity:.45; }} to {{ transform:translateX(190%); opacity:1; }} }}
      @media (max-width:560px) {{ .instrument {{ padding:18px 15px; }} .instrument-body {{ grid-template-columns:1fr; }} .dial-wrap {{ width:240px;height:240px; }} .telemetry {{ grid-template-columns:1fr 1fr; }} .telemetry-box:first-child {{ grid-column:1 / -1; }} }}
    </style>
    <div class="instrument {skin_class}">
      <div class="instrument-head">
        <div><p class="instrument-title">{active_mode} / SIGNAL CORE</p><div class="instrument-sub">{mode_tag} &nbsp;•&nbsp; {strat["tagline"]}</div></div>
        <div class="live-chip"><i></i>ENGINE READY</div>
      </div>
      <div class="instrument-body">
        <div class="dial-wrap">
          <div class="dial-glow"></div><div class="dial-track"></div><div class="dial-orbit {"spin-up" if generated_at and signal_age < 4 else ""}"></div><div class="dial-inner"></div>
          <div class="dial-core"><div class="dial-kicker">POTENTIAL TARGET</div><div class="dial-value">{display_target}</div><div class="dial-label">MULTIPLIER</div></div>
          <div class="dial-stat left">NEURAL SIGNAL</div><div class="dial-stat right">ROUND SYNC</div>
        </div>
        <div class="telemetry">
          <div class="telemetry-box">
            <div class="telemetry-label">TIME SINCE LAST RESULT</div>
            <div class="telemetry-value"><span id="round-age">{"—" if initial_elapsed < 0 else f"{initial_elapsed:02d}"}</span><em> SEC</em></div>
            <div class="window-track"><div class="sync-fill"></div></div>
          </div>
          <div class="telemetry-box"><div class="telemetry-label">MODEL CONFIDENCE</div><div class="telemetry-value">{confidence_text}<em> / SAMPLE</em></div></div>
          <div class="telemetry-box"><div class="telemetry-label">HISTORY ACCURACY</div><div class="telemetry-value" style="color:{accuracy_color}">{rate}% <em>{hits}/{total} RESOLVED</em></div></div>
        </div>
      </div>
      <div class="history-head"><span>RECENT SIGNAL CHECKS</span><span>TRIPLE TRACE</span></div>
      <div class="history-row">{''.join(recent)}</div>
      <div class="instrument-foot"><span>STATE: <strong id="signal-state">{signal_state}</strong></span><span>EVENT-DRIVEN ROUND SYNC &nbsp;•&nbsp; NO FIXED TIMER</span></div>
    </div>
    <script>
      let elapsed = {initial_elapsed};
      const age = document.getElementById("round-age");
      const state = document.getElementById("signal-state");
      if (elapsed < 0) {{
        if (state) state.textContent = "WAITING FOR FIRST RESULT";
      }} else {{
        const tick = setInterval(() => {{
          elapsed += 1;
          if (age) age.textContent = String(elapsed).padStart(2, "0");
        }}, 1000);
      }}
    </script>
    """
    components.html(card, height=590, scrolling=False)

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
        mode = st.session_state["auth_mode"]
        if mode == "login":
            identifier = st.text_input("EMAIL OR VERIFIED PHONE", placeholder="EMAIL OR +263 77 123 4567", label_visibility="collapsed")
            password_input = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD", label_visibility="collapsed")
            if st.session_state["auth_notice"]:
                st.info(st.session_state["auth_notice"])
                st.session_state["auth_notice"] = ""

            if st.button("INITIALIZE NEURAL MATRIX"):
                identity = identifier.strip()
                password = password_input.strip()
                if identity.lower() in KNOWN_USERS:
                    identity = KNOWN_USERS[identity.lower()]
                if not identity or not password:
                    st.error("Enter your email or verified phone number and password.")
                    return
                try:
                    payload = ({"email": identity.lower(), "password": password}
                               if "@" in identity else
                               {"phone": normalize_phone_number(identity), "password": password})
                    response = supabase.auth.sign_in_with_password(payload)
                    if response.user:
                        metadata = response.user.user_metadata or {}
                        display_name = metadata.get("username") or (response.user.email or identity).split("@", 1)[0]
                        st.session_state["pass"] = True
                        st.session_state["user"] = display_name
                        st.session_state["user_email"] = response.user.email or metadata.get("contact_email", "")
                        st.session_state["user_id"] = response.user.id
                        st.rerun()
                    else:
                        st.error("Sign-in failed. Check your email or verified phone, password, and confirmation status.")
                except Exception:
                    st.error("Sign-in failed. Check your email or verified phone, password, and confirmation status.")

            if st.button("CREATE ACCOUNT", use_container_width=True):
                st.session_state["auth_mode"] = "signup"
                st.rerun()

        elif mode == "signup":
            new_user = st.text_input("NEW USERNAME", placeholder="CHOOSE A USERNAME", label_visibility="collapsed")
            new_email = st.text_input("EMAIL", placeholder="ENTER YOUR EMAIL", label_visibility="collapsed")
            new_phone = st.text_input("PHONE NUMBER", placeholder="+263 77 123 4567", label_visibility="collapsed")
            channel_label = st.selectbox("VERIFICATION CHANNEL", ["SMS", "WhatsApp"], key="signup_channel")
            new_pass = st.text_input("NEW PASSWORD", type="password", placeholder="CHOOSE A PASSWORD", label_visibility="collapsed")
            confirm_pass = st.text_input("CONFIRM PASSWORD", type="password", placeholder="CONFIRM PASSWORD", label_visibility="collapsed")
            st.caption("Phone verification must be enabled in Supabase. WhatsApp delivery requires Twilio or Twilio Verify.")

            if st.button("SEND VERIFICATION CODE", type="primary"):
                username = new_user.strip().lower()
                email = new_email.strip().lower()
                password = new_pass.strip()
                if not username or not email or not new_phone.strip() or not password:
                    st.error("Complete every field before requesting a code.")
                elif "@" not in email:
                    st.error("Enter a valid email address.")
                elif password != confirm_pass.strip():
                    st.error("Passwords do not match.")
                else:
                    try:
                        phone = normalize_phone_number(new_phone)
                        channel = "whatsapp" if channel_label == "WhatsApp" else "sms"
                        response = supabase.auth.sign_up({
                            "phone": phone,
                            "password": password,
                            "options": {
                                "channel": channel,
                                "data": {"username": username, "contact_email": email},
                            },
                        })
                        if response.user:
                            st.session_state["pending_signup"] = {
                                "phone": phone, "username": username, "email": email,
                                "password": password, "channel": channel,
                            }
                            st.session_state["auth_mode"] = "verify_phone"
                            st.rerun()
                        else:
                            st.error("Supabase did not start phone verification. Check the phone provider configuration.")
                    except Exception as exc:
                        if "already" in str(exc).lower() or "registered" in str(exc).lower():
                            st.error("That phone number is already registered. Sign in with it or contact support.")
                        elif "provider" in str(exc).lower() or "sms" in str(exc).lower() or "whatsapp" in str(exc).lower():
                            st.error("Phone delivery is not configured for that channel in Supabase yet.")
                        else:
                            st.error("Could not send a verification code. Check the number and Supabase phone provider settings.")

            if st.button("BACK TO LOGIN", use_container_width=True):
                st.session_state["auth_mode"] = "login"
                st.rerun()

        else:
            pending = st.session_state.get("pending_signup", {})
            if not pending:
                st.error("Your verification session expired. Start account creation again.")
                if st.button("BACK TO ACCOUNT CREATION"):
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()
            else:
                channel_name = "WhatsApp" if pending.get("channel") == "whatsapp" else "SMS"
                st.markdown(f"### Verify your {channel_name} number")
                st.caption(f"Enter the code sent to {pending['phone']}.")
                otp_code = st.text_input("VERIFICATION CODE", max_chars=8, placeholder="ENTER CODE", label_visibility="collapsed")
                if st.button("VERIFY & FINISH ACCOUNT", type="primary"):
                    if not otp_code.strip():
                        st.error("Enter the verification code.")
                    else:
                        try:
                            verified = supabase.auth.verify_otp({
                                "phone": pending["phone"],
                                "token": otp_code.strip(),
                                "type": "sms",
                            })
                            if not verified.user:
                                st.error("The code could not be verified. Check it and try again.")
                            else:
                                metadata = {
                                    "username": pending["username"],
                                    "contact_email": pending["email"],
                                    "phone_verified": True,
                                }
                                email_linked = True
                                try:
                                    supabase.auth.update_user({
                                        "email": pending["email"],
                                        "password": pending["password"],
                                        "data": metadata,
                                    })
                                except Exception:
                                    email_linked = False
                                    supabase.auth.update_user({
                                        "password": pending["password"],
                                        "data": metadata,
                                    })
                                try:
                                    supabase.auth.sign_out()
                                except Exception:
                                    pass
                                st.session_state["pending_signup"] = {}
                                st.session_state["auth_mode"] = "login"
                                if email_linked:
                                    st.session_state["auth_notice"] = "Phone verified. Sign in with your verified phone number and password. Check your email for confirmation if Supabase requires it."
                                else:
                                    st.session_state["auth_notice"] = "Phone verified and account created. Sign in with your phone number and password; email is saved as contact information because it could not be linked."
                                st.rerun()
                        except Exception:
                            st.error("Verification failed. Check the code and try again.")

                if st.button("CANCEL / BACK TO CREATE ACCOUNT"):
                    st.session_state["pending_signup"] = {}
                    st.session_state["auth_mode"] = "signup"
                    st.rerun()

    st.markdown(
        f'<div class="footer-text">NEED HELP? <a href="https://wa.me/263779174062">WhatsApp {ADMIN_DISPLAY_PHONE}</a> &nbsp;•&nbsp; <a href="tel:{ADMIN_WHATSAPP}">CALL {ADMIN_DISPLAY_PHONE}</a></div>',
        unsafe_allow_html=True,
    )

def show_dashboard():
    active_tab = st.session_state["active_tab"]
    strat = STRATEGIES[active_tab]
    accent = strat["accent_color"]
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    st.markdown(f"<style>:root {{ --accent: {accent}; --accent-soft: color-mix(in srgb, {accent} 20%, transparent); }}</style>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="top-nav">
      <span>AVI10 / NEURAL MATRIX &nbsp;•&nbsp; MEMBER: {st.session_state['user'].upper()}</span>
      <span><span class="live">● SECURE SESSION</span> &nbsp; / &nbsp; ZIMBABWE STANDARD TIME</span>
    </div>
    """, unsafe_allow_html=True)

    mode_detail = {
        "PREDICTOR": ("THE QUIET EDGE", "Measured targets • lower-variance presentation • cool blue instrument suite"),
        "AVI10": ("THE NEURAL CORE", "Balanced target engine • live matrix visuals • emerald signal suite"),
        "MR CRUSHER": ("THE IMPACT ENGINE", "High-energy targets • heavy pulse visuals • redline signal suite"),
    }
    eyebrow, description = mode_detail[active_tab]
    st.markdown(f"""
    <div class="dash-header">
      <div class="eyebrow">{eyebrow} &nbsp; / &nbsp; {active_tab}</div>
      <h1 class="dash-title">{active_tab} NEURAL</h1>
      <p class="dash-tagline">{strat['tagline']} &nbsp; • &nbsp; {strat['min_target']:.1f}–{strat['max_target']:.1f}X TARGET BAND</p>
      <p class="dash-description">{description}</p>
    </div>
    """, unsafe_allow_html=True)

    mode_columns = st.columns(3)
    for col, mode in zip(mode_columns, ["PREDICTOR", "AVI10", "MR CRUSHER"]):
        with col:
            if st.button(mode, key=f"mode_{mode}", use_container_width=True, type="primary" if mode == active_tab else "secondary"):
                st.session_state["active_tab"] = mode
                st.session_state["current_signal"] = None
                st.session_state["signal_generated_at"] = 0.0
                st.session_state["auto_signal"] = False
                st.rerun()

    if "casino_selector" not in st.session_state:
        st.session_state["casino_selector"] = st.session_state.get("casino", "AFRICABET")
    if "custom_casinos" not in st.session_state:
        st.session_state["custom_casinos"] = {}
    casinos = {
        "AFRICABET": "https://www.africabet.com/",
        "1XBET": "https://www.1xbet.com/",
        "PREMIER BET": "https://www.premierbet.com/",
        "BETIKA - KENYA": "https://www.betika.com/en-ke/",
        "BETIKA - ZAMBIA": "https://www.betika.co.zm/en-zm/crash/flying-high",
        "SPORTPESA - KENYA": "https://www.ke.sportpesa.com/en/casino/aviator",
        "BET9JA - NIGERIA": "https://www.bet9ja.com/",
        "HOLLYWOODBETS - SOUTH AFRICA": "https://www.hollywoodbets.net/aviator",
    }
    st.markdown('<div class="section-label">01 / OPERATOR CONNECTION</div>', unsafe_allow_html=True)
    op_col, link_col, sync_col = st.columns([2.2, 1.5, 2])
    with op_col:
        selected_casino = st.selectbox(
            "SEARCH OR ENTER CASINO",
            list(casinos.keys()) + list(st.session_state["custom_casinos"].keys()),
            key="casino_selector",
            label_visibility="collapsed",
            accept_new_options=True,
            help="Type to search the list, or enter a casino name that is not listed.",
        )
        casino_url = casinos.get(selected_casino) or st.session_state["custom_casinos"].get(selected_casino, "")
        if selected_casino not in casinos:
            st.caption("Unlisted casino? Enter its official HTTPS address to open it.")
            custom_url = st.text_input(
                "OFFICIAL CASINO WEBSITE",
                placeholder="https://example.com",
                key=f"custom_casino_url_{selected_casino.lower().replace(' ', '_')[:40]}",
                label_visibility="collapsed",
            ).strip()
            parsed_url = urlparse(custom_url)
            if parsed_url.scheme == "https" and parsed_url.hostname and not any(char.isspace() for char in custom_url):
                casino_url = custom_url
                st.session_state["custom_casinos"][selected_casino] = custom_url
            elif custom_url:
                st.warning("Enter a complete secure address beginning with https://.")
    if selected_casino != st.session_state["casino"]:
        st.session_state["casino"] = selected_casino
        st.session_state["current_signal"] = None
        st.session_state["signal_generated_at"] = 0.0
        st.session_state["auto_signal"] = False
    with link_col:
        if casino_url:
            st.link_button(f"OPEN {selected_casino} ↗", casino_url, use_container_width=True)
        else:
            st.button("ADD WEBSITE URL", use_container_width=True, disabled=True, key="missing_casino_url")
    with sync_col:
        round_count = get_round_count(selected_casino)
        st.markdown(f"""
        <div class="feed-note"><b style="color:{accent}">SUPABASE ROUND LOG</b><br>{round_count} results stored for {selected_casino}. {("Saved history active" if round_count else "Baseline data active · log the first round")} . Select a casino to switch its history and signal model.</div>
        """, unsafe_allow_html=True)

    live_history = fetch_live_history(selected_casino)
    mu, sigma, momentum, tail_index, confidence, boost_prob, recent_actual = execute_neural_math(live_history)

    # A submitted result is the synchronization event, even when it is 1.00x.
    if st.session_state.get("refresh_after_round"):
        signal = generate_signal(mu, sigma, momentum, tail_index, boost_prob, recent_actual, active_tab)
        st.session_state["current_signal"] = signal
        st.session_state["signal_generated_at"] = time.time()
        st.session_state["signal_casino"] = selected_casino
        st.session_state["signal_mode"] = active_tab
        st.session_state["refresh_after_round"] = False
        save_prediction(selected_casino, active_tab, signal)

    st.markdown('<div class="section-label">02 / LIVE SIGNAL INSTRUMENT</div>', unsafe_allow_html=True)
    gen_col, band_col = st.columns([2.3, 1.3])
    with gen_col:
        if st.button("GENERATE NEW SIGNAL  ⟲", use_container_width=True, type="primary", key="generate_signal"):
            signal = generate_signal(mu, sigma, momentum, tail_index, boost_prob, recent_actual, active_tab)
            st.session_state["current_signal"] = signal
            st.session_state["signal_generated_at"] = time.time()
            st.session_state["signal_casino"] = selected_casino
            st.session_state["signal_mode"] = active_tab
            save_prediction(selected_casino, active_tab, signal)
            st.rerun()
    with band_col:
        st.metric("TARGET BAND", f"{strat['min_target']:.1f}–{strat['max_target']:.1f}x")

    accuracy = get_accuracy_stats(selected_casino, active_tab)
    recent_signals = get_recent_signals(selected_casino, active_tab)
    current_signal = st.session_state.get("current_signal")
    matching_signal = (st.session_state.get("signal_casino") == selected_casino and st.session_state.get("signal_mode") == active_tab)
    if current_signal is not None and not matching_signal:
        current_signal = None
    if current_signal is None:
        st.info("Signal core is idle. Choose a casino, then generate a signal. Enter actual round results below to update the selected casino's Supabase history.")
        render_signal_card(active_tab, 0.0, confidence, recent_signals, accuracy, last_round_at=get_latest_round_timestamp(selected_casino))
    else:
        render_signal_card(
            active_tab, current_signal, confidence, recent_signals, accuracy,
            st.session_state.get("signal_generated_at", 0.0),
            get_latest_round_timestamp(selected_casino),
        )
    st.caption("Round sync is event-driven: every submitted result, including 1.00x, resolves the previous signal and immediately generates the next estimate.")

    st.markdown('<div class="section-label">03 / ROUND DATA & ACCURACY</div>', unsafe_allow_html=True)
    round_col, submit_col, stats_col = st.columns([1.5, 1, 2])
    with round_col:
        round_multiplier = st.number_input("ACTUAL MULTIPLIER", min_value=1.00, max_value=100.00, value=1.50, step=0.05, format="%.2f", key="round_multiplier")
    with submit_col:
        st.write("")
        if st.button("LOG ROUND RESULT", use_container_width=True, key="log_round"):
            if insert_round_result(selected_casino, float(round_multiplier), active_tab):
                st.session_state["refresh_after_round"] = True
                st.success(f"Logged {round_multiplier:.2f}x to {selected_casino}; refreshing from the updated history.")
                st.rerun()
            else:
                st.error("Could not log this result to Supabase. Check the database table and row-level security policies.")

    with stats_col:
        st.metric("ROUNDS STORED", round_count)
    st.markdown("""
    <div class="feed-note">
      <b>DATA SOURCE STATUS</b><br>
      The selected operator button opens its website. This build has no official operator result feed connected.
      Round values entered here are saved to Supabase and are then used for that operator's history and signal calculations.
      Estimates are stochastic summaries of entered data; they are not guaranteed outcomes.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">04 / PREDICTOR COMMUNITY CHAT</div>', unsafe_allow_html=True)
    st.markdown('<div class="feed-note">Chat with other signed-in members in the shared predictor room.</div>', unsafe_allow_html=True)

    @st.fragment(run_every="4s")
    def community_chat():
        try:
            messages = fetch_community_messages()
        except Exception:
            st.warning("Community chat needs its Supabase table. Apply the community-chat migration from this repository in Supabase SQL Editor.")
            messages = []

        for item in messages:
            mine = item["user_id"] == st.session_state.get("user_id")
            with st.chat_message("user" if mine else "assistant"):
                st.caption(item.get("username") or "Member")
                st.write(item.get("message", ""))

        new_message = st.chat_input("Message the predictor community…", max_chars=1000, key="community_chat_input")
        if new_message and new_message.strip():
            try:
                send_community_message(new_message)
                st.rerun(scope="fragment")
            except Exception:
                st.error("Could not send the message. Check that the chat migration has been applied and your Supabase session is active.")

    community_chat()

    st.markdown('<div class="footer-line">AVI10 NEURAL MATRIX &nbsp;•&nbsp; EDGE SYSTEMS / SESSION ACTIVE</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. ROUTER
# ==============================================================================
if not st.session_state["pass"]:
    show_login()
else:
    show_dashboard()
