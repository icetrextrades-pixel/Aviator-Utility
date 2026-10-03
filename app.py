import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import math
import os
import re
import secrets
import string
import time
from datetime import datetime
from urllib.parse import urlparse
import pytz
from supabase import create_client, Client

# Page configuration must be the first Streamlit command.
st.set_page_config(
    page_title="AVI10 NEURAL MATRIX",
    layout="centered",
    initial_sidebar_state="expanded",
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
# Server-only Supabase Auth administration key. Never render or log this value.
SUPABASE_ADMIN_KEY = _get_config_value("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY")


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
ONBOARDING_TERMS_VERSION = "2026-10-03"
ONBOARDING_TERMS_KEY = "aviator_terms_accepted_version"
SUPPORT_WHATSAPP_CONTACTS = [
    ("0785 828 643", "263785828643"),
    ("0779 174 062", "263779174062"),
]
WHATSAPP_ICON_HTML = """
<svg class="whatsapp-brand-icon" viewBox="0 0 24 24" role="img" aria-label="WhatsApp">
  <circle cx="12" cy="12" r="12" fill="#25D366"></circle>
  <path fill="#fff" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.768.966-.94 1.164-.173.198-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.372-.025-.521-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.273.298-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.095 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.999-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.002-5.45 4.437-9.884 9.892-9.884 2.643.001 5.126 1.03 6.993 2.898a9.825 9.825 0 0 1 2.896 6.999c-.003 5.45-4.437 9.878-9.898 9.878M20.526 3.511A11.815 11.815 0 0 0 12.046.001C5.42.001.029 5.39.026 12.017c0 2.12.555 4.189 1.612 6.014L0 24.017l6.139-1.611a11.9 11.9 0 0 0 5.705 1.452h.005c6.627 0 12.017-5.39 12.02-12.017a11.9 11.9 0 0 0-3.343-8.33"></path>
</svg>
"""


if "pass" not in st.session_state: st.session_state["pass"] = False
if "user" not in st.session_state: st.session_state["user"] = ""
if "user_email" not in st.session_state: st.session_state["user_email"] = ""
if "user_id" not in st.session_state: st.session_state["user_id"] = ""
if "onboarding_complete" not in st.session_state: st.session_state["onboarding_complete"] = False
if "onboarding_step" not in st.session_state: st.session_state["onboarding_step"] = 0
if "onboarding_consent_checkbox" not in st.session_state: st.session_state["onboarding_consent_checkbox"] = False
if "refresh_after_round" not in st.session_state: st.session_state["refresh_after_round"] = False
if "casino" not in st.session_state: st.session_state["casino"] = "AFRICABET"
if "active_tab" not in st.session_state: st.session_state["active_tab"] = "AVI10"
if "auth_mode" not in st.session_state: st.session_state["auth_mode"] = "login"
if "auth_notice" not in st.session_state: st.session_state["auth_notice"] = ""
if "signup_email" not in st.session_state: st.session_state["signup_email"] = ""
if "signup_username_options" not in st.session_state: st.session_state["signup_username_options"] = []
if "profile_theme" not in st.session_state: st.session_state["profile_theme"] = "Neon Cyan"
if "signal_generated_at" not in st.session_state: st.session_state["signal_generated_at"] = 0.0
if "auto_signal" not in st.session_state: st.session_state["auto_signal"] = False
if "current_signal" not in st.session_state: st.session_state["current_signal"] = None
if "signal_anim_state" not in st.session_state: st.session_state["signal_anim_state"] = "idle"
if "session_started_at" not in st.session_state: st.session_state["session_started_at"] = 0.0
if "session_signals_generated" not in st.session_state: st.session_state["session_signals_generated"] = 0
if "session_rounds_logged" not in st.session_state: st.session_state["session_rounds_logged"] = 0
if "session_time_limit_minutes" not in st.session_state: st.session_state["session_time_limit_minutes"] = 30
if "session_budget_limit" not in st.session_state: st.session_state["session_budget_limit"] = 0.0
if "session_spend_amount" not in st.session_state: st.session_state["session_spend_amount"] = 0.0

# ==============================================================================
# 2. STRATEGY CONFIGURATIONS
# ==============================================================================
MIN_REFERENCE_ROUNDS = 5
MATURE_REFERENCE_ROUNDS = 20

# These are distinct historical-reference methods, not forecasts.
STRATEGIES = {
    "PREDICTOR": {
        "min_target": 1.10,
        "max_target": 2.00,
        "tagline": "LOW-STAKES PROFILE · P25 LOWER QUARTILE",
        "method_note": "Conservative lower-quartile reference from the full logged sample.",
        "accent_color": "#3b82f6",
    },
    "MR CRUSHER": {
        "min_target": 2.00,
        "max_target": 5.00,
        "tagline": "HIGH-STAKES PROFILE · P75/P90 TAIL BLEND",
        "method_note": "Upper-tail reference for higher variance; it is not a recommendation to wager more.",
        "accent_color": "#ef4444",
    },
    "AVI10": {
        "min_target": 1.40,
        "max_target": 3.50,
        "tagline": "MID-STAKES PROFILE · RECENCY-WEIGHTED P50",
        "method_note": "Median reference with recent logged rounds given more descriptive weight.",
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
    return []

def insert_round_result(casino_name: str, multiplier: float, strategy: str) -> bool:
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.session_state["round_save_error"] = "No authenticated user ID is present in this Streamlit session."
        return False

    try:
        supabase.table("round_history") \
            .insert({
                "user_id": user_id,
                "casino": casino_name,
                "multiplier": multiplier,
            }) \
            .execute()
        st.session_state["round_save_error"] = ""
        resolve_pending_signals(casino_name, multiplier, strategy)
        return True
    except Exception as exc:
        # Keep diagnostics in the signed-in session; only the admin UI renders them.
        st.session_state["round_save_error"] = f"{type(exc).__name__}: {str(exc)[:500]}"
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

def fetch_round_sample(casino_name: str, limit: int = 500) -> list:
    """Fetch real member-submitted outcomes for descriptive odds analysis."""
    try:
        response = (supabase.table("round_history").select("multiplier")
                    .eq("casino", casino_name).order("created_at", desc=True)
                    .limit(limit).execute())
        values = []
        for row in response.data or []:
            try:
                value = float(row.get("multiplier"))
                if math.isfinite(value) and value >= 1.0:
                    values.append(value)
            except (TypeError, ValueError):
                continue
        return values
    except Exception:
        return []


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple:
    """Wilson score interval for a binomial proportion."""
    if total <= 0:
        return 0.0, 0.0
    proportion = successes / total
    z_squared = z * z
    denominator = 1 + z_squared / total
    center = (proportion + z_squared / (2 * total)) / denominator
    margin = z * math.sqrt((proportion * (1 - proportion) + z_squared / (4 * total)) / total) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def build_historical_odds_rows(values: list) -> list:
    """Summarize observed threshold frequencies from logged rounds."""
    sample = []
    for value in values:
        try:
            value = float(value)
            if math.isfinite(value) and value >= 1.0:
                sample.append(value)
        except (TypeError, ValueError):
            continue
    total = len(sample)
    if not total:
        return []

    rows = []
    for target in (1.5, 2.0, 3.0, 5.0, 10.0, 20.0):
        hits = sum(value >= target for value in sample)
        observed = hits / total
        low, high = wilson_interval(hits, total)
        rows.append({
            "Cash-out target": f"{target:g}x",
            "Logged rounds reaching target": f"{hits} / {total}",
            "Observed hit rate": f"{observed * 100:.1f}%",
            "95% Wilson range": f"{low * 100:.1f}%–{high * 100:.1f}%",
            "Break-even hit rate": f"{100 / target:.1f}%",
            "Historical net per 100 staked": f"{(observed * target - 1) * 100:+.1f}%",
        })
    return rows


def show_historical_odds_lab(casino_name: str):
    st.markdown('<div class="section-label">02B / HISTORICAL ODDS & BREAK-EVEN LAB</div>', unsafe_allow_html=True)
    with st.expander("VIEW OBSERVED ODDS BY CASH-OUT TARGET", expanded=True):
        values = fetch_round_sample(casino_name)
        total = len(values)
        if not total:
            st.info("No valid member-submitted rounds are available for this casino yet. Log real results to build the sample.")
            return

        st.metric("ROUNDS IN SAMPLE", total)
        st.dataframe(build_historical_odds_rows(values), use_container_width=True, hide_index=True)
        st.caption(
            "These are historical frequencies from member-submitted, unverified results. "
            "Break-even hit rate is 1 divided by target; historical net assumes a fixed cash-out "
            "and ignores operator rules, promotions, and data errors. The 95% Wilson range describes "
            "sampling uncertainty in this log; it is not a probability range for the next round."
        )
        if total < 100:
            st.warning("Small samples can swing sharply. Treat these figures as weak evidence, not a betting edge.")
        st.info("Crash rounds are designed to be unpredictable. Recent outcomes do not tell you when the next round will crash.")


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


def fetch_recent_round_pulse(limit: int = 15) -> list:
    """Return shared member-submitted rounds, newest first."""
    response = (
        supabase.table("round_history")
        .select("casino, multiplier, created_at")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []


def fetch_signal_lab_rows(casino_name: str, strategy: str, limit: int = 100) -> list:
    """Return resolved predictions for a compact historical comparison chart."""
    response = (
        supabase.table("signal_history")
        .select("predicted_multiplier, actual_multiplier, hit, created_at")
        .eq("casino", casino_name)
        .eq("strategy", strategy)
        .not_.is_("actual_multiplier", "null")
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )
    return response.data or []


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
            return 1.45, 0.20, 0.0, 2.0, 0.0, 0.15, []
        arr = np.array(vals)
        mu = float(np.mean(arr))
        raw_sigma = float(np.std(arr))
        sigma = max(raw_sigma, 1e-6)
        log_returns = np.diff(np.log(arr))
        momentum = float(np.mean(log_returns)) if len(log_returns) > 0 else 0.0
        tail_index = hill_estimator(arr)
        confidence = float(len(arr))
        boost_prob = estimate_boost_probability(arr)
        recent_actual = [float(v) for v in vals[:3]]
        return mu, sigma, momentum, min(tail_index, 15.0), confidence, boost_prob, recent_actual
    except Exception:
        return 1.45, 0.20, 0.0, 2.0, 50.0, 0.15, []

def parse_valid_round_values(history_data) -> list:
    """Parse submitted multipliers, newest first when provided by round_history."""
    values = []
    for value in history_data:
        try:
            number = float(str(value).replace("x", "").strip())
            if math.isfinite(number) and number >= 1.0:
                values.append(number)
        except (TypeError, ValueError):
            continue
    return values


def weighted_quantile(values, weights, quantile: float) -> float:
    """Return an observed quantile with explicit per-round weights."""
    data = np.asarray(values, dtype=float)
    sample_weights = np.asarray(weights, dtype=float)
    order = np.argsort(data)
    sorted_data = data[order]
    sorted_weights = sample_weights[order]
    cumulative = np.cumsum(sorted_weights)
    cutoff = min(max(float(quantile), 0.0), 1.0) * cumulative[-1]
    index = min(int(np.searchsorted(cumulative, cutoff, side="left")), len(sorted_data) - 1)
    return float(sorted_data[index])


def generate_signal(history_data, strategy_name: str):
    """Return the department's historical reference; it does not forecast the next round."""
    values = parse_valid_round_values(history_data)
    if len(values) < MIN_REFERENCE_ROUNDS:
        return None

    sample = np.asarray(values, dtype=float)
    if strategy_name == "PREDICTOR":
        # Lower quartile: a conservative threshold descriptive of the full sample.
        reference = float(np.quantile(sample, 0.25))
    elif strategy_name == "AVI10":
        # Weighted median: recent rounds carry higher descriptive weight.
        weights = np.power(0.96, np.arange(len(sample), dtype=float))
        reference = weighted_quantile(sample, weights, 0.50)
    elif strategy_name == "MR CRUSHER":
        # Blend upper quartile and 90th percentile to expose a higher-variance tail.
        q75, q90 = np.quantile(sample, [0.75, 0.90])
        reference = float(0.70 * q75 + 0.30 * q90)
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    strategy = STRATEGIES[strategy_name]
    return float(max(strategy["min_target"], min(strategy["max_target"], reference)))


def estimate_historical_target_rate(history_data, target: float) -> dict:
    """Describe how often submitted historical rounds reached a reference target."""
    values = parse_valid_round_values(history_data)
    total = len(values)
    if not total:
        return {"hits": 0, "total": 0, "rate": 0.0, "low": 0.0, "high": 0.0}
    hits = sum(value >= target for value in values)
    low, high = wilson_interval(hits, total)
    return {
        "hits": hits,
        "total": total,
        "rate": hits / total * 100,
        "low": low * 100,
        "high": high * 100,
    }


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
    sample_depth_text = str(int(confidence)) if confidence else "0"
    hits = accuracy["hits"]
    total = accuracy["total"]
    rate = accuracy["rate"]
    signal_age = max(0, time.time() - generated_at) if generated_at else 0
    initial_elapsed = max(0, int(time.time() - last_round_at)) if last_round_at else -1
    signal_state = "REFERENCE UPDATED" if generated_at else "AWAITING REFERENCE"
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
          <div class="dial-core"><div class="dial-kicker">HISTORICAL REFERENCE</div><div class="dial-value">{display_target}</div><div class="dial-label">MULTIPLIER</div></div>
          <div class="dial-stat left">EMPIRICAL QUANTILE</div><div class="dial-stat right">ROUND SYNC</div>
        </div>
        <div class="telemetry">
          <div class="telemetry-box">
            <div class="telemetry-label">TIME SINCE LAST RESULT</div>
            <div class="telemetry-value"><span id="round-age">{"—" if initial_elapsed < 0 else f"{initial_elapsed:02d}"}</span><em> SEC</em></div>
            <div class="window-track"><div class="sync-fill"></div></div>
          </div>
          <div class="telemetry-box"><div class="telemetry-label">INPUT SAMPLE DEPTH</div><div class="telemetry-value">{sample_depth_text}<em> / ROUNDS</em></div></div>
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

def _admin_auth_client():
    if not SUPABASE_ADMIN_KEY:
        raise RuntimeError("Account administration is not configured. Add SUPABASE_SECRET_KEY to Streamlit Secrets.")
    return create_client(SUPABASE_URL, SUPABASE_ADMIN_KEY)


def _auth_user_attr(user, name, default=None):
    return user.get(name, default) if isinstance(user, dict) else getattr(user, name, default)


def _list_auth_users(admin_client) -> list:
    response = admin_client.auth.admin.list_users(page=1, per_page=1000)
    if isinstance(response, list):
        return response
    if isinstance(response, dict):
        return response.get("users") or response.get("data") or []
    return getattr(response, "users", None) or getattr(response, "data", None) or []


def _username_candidates(email: str, admin_client) -> list:
    local = email.split("@", 1)[0].lower()
    base = re.sub(r"[^a-z0-9_]", "", local).strip("_")[:18] or "member"
    existing = set()
    for user in _list_auth_users(admin_client):
        metadata = _auth_user_attr(user, "user_metadata", {}) or {}
        if isinstance(metadata, dict) and isinstance(metadata.get("username"), str):
            existing.add(metadata["username"].lower())
    suffixes = list(range(100))
    secrets.SystemRandom().shuffle(suffixes)
    choices = [f"{base}{n:02d}" for n in suffixes if f"{base}{n:02d}".lower() not in existing]
    if len(choices) < 3:
        raise RuntimeError("No available two-digit username choices remain for this email name.")
    return choices[:3]



def _username_available(username: str, current_user_id: str) -> bool:
    for user in _list_auth_users(_admin_auth_client()):
        if str(_auth_user_attr(user, "id", "")) == str(current_user_id):
            continue
        metadata = _auth_user_attr(user, "user_metadata", {}) or {}
        if isinstance(metadata, dict) and str(metadata.get("username", "")).lower() == username.lower():
            return False
    return True


def _email_for_username(username: str) -> str:
    """Resolve exactly one username to its email for server-side password sign-in."""
    wanted = username.strip().casefold()
    matches = []
    for user in _list_auth_users(_admin_auth_client()):
        metadata = _auth_user_attr(user, "user_metadata", {}) or {}
        candidate = metadata.get("username") if isinstance(metadata, dict) else None
        if isinstance(candidate, str) and candidate.strip().casefold() == wanted:
            email = _auth_user_attr(user, "email", "")
            if isinstance(email, str) and email.strip():
                matches.append(email.strip().lower())
    return matches[0] if len(matches) == 1 else ""

def _new_strong_password() -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%*-_"
    chars = [secrets.choice(string.ascii_lowercase), secrets.choice(string.ascii_uppercase),
             secrets.choice(string.digits), secrets.choice("!@#$%*-_")]
    chars.extend(secrets.choice(alphabet) for _ in range(28))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def _create_pending_member(email: str, username: str, password: str):
    client = _admin_auth_client()
    response = client.auth.admin.create_user({
        "email": email, "password": password, "email_confirm": True,
        "user_metadata": {"username": username},
    })
    user = getattr(response, "user", None) or (response.get("user") if isinstance(response, dict) else None)
    user_id = _auth_user_attr(user, "id")
    if not user_id:
        raise RuntimeError("Supabase did not return the new account ID.")
    try:
        client.auth.admin.update_user_by_id(user_id, {"app_metadata": {"aviator_access_approved": False}})
    except Exception:
        try:
            client.auth.admin.delete_user(user_id)
        except Exception:
            pass
        raise


def _credential_reveal_html(username: str, email: str, password: str) -> str:
    import json
    username_js, email_js, password_js = map(json.dumps, (username, email, password))
    return f"""
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{{box-sizing:border-box}}body{{margin:0;background:transparent;color:#ecf7ff;font:14px system-ui,sans-serif}}
.card{{padding:18px;border:1px solid #27d3c0;border-left:4px solid #25d366;background:linear-gradient(135deg,#0b1c2b,#08111d);box-shadow:0 0 26px #08d9c433}}
.kicker{{color:#6ee7d8;font:800 10px ui-monospace,monospace;letter-spacing:2px}}
.warning{{margin:12px 0;padding:10px;border:1px solid #ef4444;background:#3b1015;color:#fecaca;font-weight:800}}
.label{{color:#99adc0;font:700 10px ui-monospace,monospace;letter-spacing:1px;margin-top:12px}}
.value{{display:block;overflow-wrap:anywhere;margin-top:4px;padding:9px;background:#040912;border:1px solid #26394a;color:#fff;font:700 15px ui-monospace,monospace;user-select:all}}
.timer{{margin-top:12px;color:#fcd34d;font-weight:800}}.pending{{display:none;color:#d8f4ff;line-height:1.65}}
</style></head><body><div class="card"><div class="kicker" id="stage">STEP 3 OF 4 · SAVE CREDENTIALS</div><p>Sign in with the email address and password; your username is your profile name.</p><div id="secret">
<div class="warning">⚠ Save these details now. This reveal disappears after 30 seconds. Do not share your details with anyone.</div>
<div class="label">USERNAME</div><span id="username" class="value"></span><div class="label">EMAIL</div><span id="email" class="value"></span>
<div class="label">RANDOM PASSWORD</div><span id="password" class="value"></span><div class="timer">Credentials hide in <span id="seconds">30</span> seconds.</div></div>
<div id="pending" class="pending"><strong>Credentials hidden.</strong><br>Contact the admin using Contact Support/Admin or the email shown on this page for verification, then wait for approval before logging in.</div>
</div><script>
document.getElementById("username").textContent={username_js};
document.getElementById("email").textContent={email_js};
document.getElementById("password").textContent={password_js};
let remaining=30;const timer=setInterval(()=>{{remaining--;document.getElementById("seconds").textContent=remaining;
if(remaining<=0){{clearInterval(timer);document.getElementById("secret").remove();document.getElementById("stage").textContent="STEP 4 OF 4 · ADMIN VERIFICATION";document.getElementById("pending").style.display="block";}}}},1000);
</script></body></html>"""


def _set_profile_metadata(updates: dict):
    response = supabase.auth.update_user({"data": updates})
    user = getattr(response, "user", None)
    if not user:
        raise RuntimeError("Supabase did not confirm the profile update.")
    metadata = getattr(user, "user_metadata", {}) or {}
    st.session_state["user"] = metadata.get("username") or st.session_state.get("user", "")
    st.session_state["profile_theme"] = metadata.get("app_theme") or st.session_state.get("profile_theme", "Neon Cyan")
    st.session_state["user_metadata"] = metadata


def show_profile_sidebar():
    email, username = st.session_state.get("user_email", ""), st.session_state.get("user", "")
    metadata = st.session_state.get("user_metadata", {}) or {}
    with st.sidebar:
        st.markdown("### MEMBER PROFILE")
        st.caption("Only you can see these profile details. Passwords cannot be read by the app or admin.")
        st.caption("EMAIL ADDRESS")
        st.code(email, language=None)
        st.caption("USERNAME")
        st.code(username, language=None)
        st.caption("PASSWORD · HIDDEN")
        st.code("••••••••••••••••", language=None)
        avatar_path = metadata.get("avatar_path")
        if avatar_path:
            try:
                signed = supabase.storage.from_("member-avatars").create_signed_url(avatar_path, 3600)
                signed_url = signed.get("signedURL") if isinstance(signed, dict) else getattr(signed, "signed_url", "")
                if signed_url:
                    st.image(signed_url, width=112)
            except Exception:
                st.caption("Profile picture is unavailable until the avatar storage migration is applied.")

        with st.expander("PROFILE SETTINGS", expanded=False):
            with st.form("edit_member_username"):
                new_username = st.text_input("EDIT USERNAME", value=username, max_chars=28)
                save_username = st.form_submit_button("SAVE USERNAME", use_container_width=True)
            if save_username:
                proposed = new_username.strip()
                valid_name = len(proposed) >= 3 and proposed[-2:].isdigit() and all(c.isalnum() or c == "_" for c in proposed[:-2])
                if not valid_name:
                    st.error("Use letters, numbers, or underscores followed by exactly two digits.")
                elif proposed.lower() != username.lower():
                    try:
                        if not _username_available(proposed, st.session_state.get("user_id", "")):
                            st.error("That username is already in use. Choose a different one.")
                        else:
                            _set_profile_metadata({"username": proposed})
                            st.success("Username updated in Supabase.")
                            st.rerun()
                    except Exception:
                        st.error("Supabase could not update the username. Please try again.")

            themes = ["Neon Cyan", "Electric Violet", "Ember"]
            saved_theme = st.session_state.get("profile_theme", "Neon Cyan")
            with st.form("edit_member_theme"):
                theme = st.selectbox("THEME", themes, index=themes.index(saved_theme) if saved_theme in themes else 0)
                save_theme = st.form_submit_button("SAVE THEME", use_container_width=True)
            if save_theme:
                try:
                    _set_profile_metadata({"app_theme": theme})
                    st.success("Theme preference saved to Supabase.")
                    st.rerun()
                except Exception:
                    st.error("Supabase could not save your theme. Please try again.")

            uploaded = st.file_uploader("EDIT PROFILE PICTURE", type=["png", "jpg", "jpeg", "webp"], key="member_avatar_upload", help="Private image, maximum 2 MB.")
            if uploaded and st.button("SAVE PROFILE PICTURE", use_container_width=True):
                if len(uploaded.getvalue()) > 2 * 1024 * 1024:
                    st.error("Choose an image no larger than 2 MB.")
                else:
                    ext = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}.get(uploaded.type)
                    if not ext:
                        st.error("Choose a PNG, JPG, or WEBP image.")
                    else:
                        path = f"{st.session_state['user_id']}/avatar.{ext}"
                        try:
                            supabase.storage.from_("member-avatars").upload(path, uploaded.getvalue(), {"content-type": uploaded.type, "upsert": "true"})
                            _set_profile_metadata({"avatar_path": path})
                            st.success("Profile picture uploaded privately and linked to your profile.")
                            st.rerun()
                        except Exception:
                            st.error("Could not save the picture. Apply the member-avatar storage migration and try again.")

            st.markdown("**RESET PASSWORD**")
            with st.form("member_password_reset"):
                current_password = st.text_input("CURRENT PASSWORD", type="password")
                new_password = st.text_input("NEW STRONG PASSWORD", type="password")
                confirm_password = st.text_input("CONFIRM NEW PASSWORD", type="password")
                reset_password = st.form_submit_button("UPDATE PASSWORD", use_container_width=True)
            if reset_password:
                is_strong = (
                    len(new_password) >= 12
                    and any(c.islower() for c in new_password)
                    and any(c.isupper() for c in new_password)
                    and any(c.isdigit() for c in new_password)
                    and any(not c.isalnum() for c in new_password)
                )
                if not current_password or not is_strong or new_password != confirm_password:
                    st.error("Enter your current password and a matching password with 12+ characters, upper- and lowercase letters, a number, and a symbol.")
                else:
                    try:
                        verified = supabase.auth.sign_in_with_password({"email": email, "password": current_password})
                        if not getattr(verified, "user", None):
                            raise RuntimeError("Current password was not verified.")
                        changed = supabase.auth.update_user({"password": new_password})
                        if not getattr(changed, "user", None):
                            raise RuntimeError("Supabase did not confirm the password update.")
                        st.success("Password updated in Supabase. The app cannot read it afterward.")
                        st.rerun()
                    except Exception:
                        st.error("Password reset failed. Verify your current password and try again.")



def show_login():
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div class="login-container"><div class="padlock-wrapper">🔐</div>
    <h1 class="title-aviator">AVIATOR <span class="title-signals">SIGNALS</span></h1>
    <p class="subtext">NO RISK NO GAIN</p></div>
    """, unsafe_allow_html=True)
    mode = st.session_state.get("auth_mode", "login")
    if mode == "login":
        _, main_column, _ = st.columns([1, 4, 1])
    else:
        _, main_column, _ = st.columns([0.2, 10, 0.2])
    with main_column:
        signup_steps = {
            "signup_email": (1, "EMAIL ADDRESS"),
            "signup_username": (2, "CHOOSE USERNAME"),
            "signup_credentials": (3, "SAVE CREDENTIALS"),
        }
        if mode in signup_steps:
            step_number, step_name = signup_steps[mode]
            st.progress(step_number / 4, text=f"CREATE ACCOUNT · STEP {step_number} OF 4 · {step_name}")
        if mode == "login":
            login_identifier_input = st.text_input("EMAIL OR USERNAME", placeholder="ENTER EMAIL OR USERNAME", label_visibility="collapsed")
            password_input = st.text_input("PASSWORD", type="password", placeholder="ENTER PASSWORD", label_visibility="collapsed")
            if st.session_state.get("auth_notice"):
                st.info(st.session_state["auth_notice"])
                st.session_state["auth_notice"] = ""
            if st.button("INITIALIZE NEURAL MATRIX", use_container_width=True):
                identifier = login_identifier_input.strip()
                if not identifier or not password_input:
                    st.error("Enter your email or username and password.")
                    return
                if "@" in identifier:
                    email = identifier.lower()
                    valid_email = email.count("@") == 1 and not any(c.isspace() for c in email) and "." in email.split("@", 1)[1]
                    if not valid_email:
                        st.error("Sign-in failed. Check your email or username, password, and account approval status.")
                        return
                else:
                    valid_username = (
                        len(identifier) <= 64
                        and all(character.isalnum() or character in "._-" for character in identifier)
                    )
                    if not valid_username or not SUPABASE_ADMIN_KEY:
                        st.error("Sign-in failed. Check your email or username, password, and account approval status.")
                        return
                    try:
                        email = _email_for_username(identifier)
                    except Exception:
                        email = ""
                    if not email:
                        st.error("Sign-in failed. Check your email or username, password, and account approval status.")
                        return
                try:
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password_input})
                    user = getattr(response, "user", None)
                    if not user:
                        raise RuntimeError("Supabase did not return the authenticated account.")
                    actual_email = getattr(user, "email", None) or email
                    app_meta = getattr(user, "app_metadata", {}) or {}
                    if app_meta.get("aviator_access_approved") is not True:
                        try:
                            supabase.auth.sign_out()
                        except Exception:
                            pass
                        st.session_state["auth_notice"] = "Your account is awaiting admin verification. Contact Support/Admin by email and wait for approval before signing in."
                        st.rerun()
                    metadata = getattr(user, "user_metadata", {}) or {}
                    st.session_state["pass"] = True
                    st.session_state["user"] = metadata.get("username") or actual_email.split("@", 1)[0]
                    st.session_state["user_email"] = actual_email
                    st.session_state["user_id"] = getattr(user, "id", "")
                    st.session_state["user_metadata"] = metadata
                    st.session_state["profile_theme"] = metadata.get("app_theme", "Neon Cyan")
                    st.session_state["onboarding_complete"] = metadata.get(ONBOARDING_TERMS_KEY) == ONBOARDING_TERMS_VERSION
                    st.session_state["onboarding_step"] = 0
                    st.session_state["onboarding_consent_checkbox"] = False
                    st.session_state["session_started_at"] = time.time()
                    st.session_state["session_signals_generated"] = 0
                    st.session_state["session_rounds_logged"] = 0
                    st.session_state["session_spend_amount"] = 0.0
                    st.session_state["session_budget_limit"] = 0.0
                    st.session_state["session_time_limit_minutes"] = 30
                    st.rerun()
                except Exception:
                    st.error("Sign-in failed. Check your email or username, password, and account approval status.")
            if st.button("CREATE ACCOUNT", use_container_width=True):
                st.session_state["auth_mode"] = "signup_email"
                st.rerun()

        elif mode == "signup_email":
            st.markdown("### CREATE A PRIVATE ACCOUNT")
            st.caption("Enter your email address. Choose one of three usernames based on its name; the system generates a one-time password.")
            email_value = st.text_input("EMAIL ADDRESS", value=st.session_state.get("signup_email", ""), placeholder="name@example.com")
            left, right = st.columns(2)
            with left:
                continue_signup = st.button("CONTINUE", type="primary", use_container_width=True)
            with right:
                back = st.button("BACK TO LOGIN", use_container_width=True)
            if back:
                st.session_state["auth_mode"] = "login"
                st.rerun()
            if continue_signup:
                email = email_value.strip().lower()
                valid_email = email.count("@") == 1 and not any(c.isspace() for c in email) and "." in email.split("@", 1)[1]
                if not valid_email:
                    st.error("Enter a valid email address.")
                elif email == ADMIN_EMAIL.lower():
                    st.error("The administrator email is reserved. Use the private Admin Access page for administrator sign-in.")
                elif not SUPABASE_ADMIN_KEY:
                    st.error("Account creation is unavailable until the admin adds SUPABASE_SECRET_KEY to Streamlit Secrets.")
                else:
                    try:
                        st.session_state["signup_email"] = email
                        st.session_state["signup_username_options"] = _username_candidates(email, _admin_auth_client())
                        st.session_state["auth_mode"] = "signup_username"
                        st.rerun()
                    except Exception:
                        st.error("Could not prepare account options. Check the server-side Supabase admin configuration.")

        elif mode == "signup_username":
            email = st.session_state.get("signup_email", "")
            options = st.session_state.get("signup_username_options", [])
            if len(options) != 3:
                st.session_state["auth_mode"] = "signup_email"
                st.rerun()
            st.markdown("### CHOOSE YOUR USERNAME")
            st.caption("Each option uses the name before @ in your email and ends in exactly two digits.")
            username = st.radio("USERNAME OPTIONS", options, horizontal=True)
            st.warning("⚠ Save the username and password immediately when shown. Do not share your details with anyone.")
            if st.button("CREATE ACCOUNT", type="primary", use_container_width=True):
                password = _new_strong_password()
                try:
                    _create_pending_member(email, username, password)
                    st.session_state["signup_email"] = ""
                    st.session_state["signup_username_options"] = []
                    st.session_state["auth_mode"] = "signup_credentials"
                    st.markdown("### ACCOUNT CREATED · PENDING ADMIN VERIFICATION")
                    st.caption("This one-time password is not saved in the app's session state or shown to the admin.")
                    components.html(_credential_reveal_html(username, email, password), height=460, scrolling=False)
                except Exception:
                    st.error("Account creation failed. Check the Supabase admin key and whether this email is already registered.")

        elif mode == "signup_credentials":
            st.markdown("### CREDENTIAL REVEAL ENDED")
            st.warning("⚠ Contact the admin for verification and wait for approval before logging in. Use Contact Support/Admin or the email shown here.")
            if st.button("BACK TO LOGIN", use_container_width=True):
                st.session_state["auth_mode"] = "login"
                st.rerun()
        else:
            st.session_state["auth_mode"] = "login"
            st.rerun()

    st.markdown("""
    <style>
      .login-support-email { text-align:center;margin:1rem 0 .55rem;font-size:.9rem }
      .login-support-email a { color:#f3f4f6!important;text-decoration:none }
      .whatsapp-brand-icon { width:30px;height:30px;display:block;margin:.45rem auto }
      div[data-testid="stPopover"]>button { background:#fff!important;color:#111827!important;border:1px solid #d1d5db!important;border-radius:8px!important;min-height:44px;font-weight:700!important }
      .support-contact-email { margin:.25rem 0 .85rem }
      .support-whatsapp-link { display:flex;align-items:center;gap:.65rem;padding:.7rem .8rem;margin:.45rem 0;border:1px solid #2a2d33;border-radius:9px;color:#f9fafb!important;text-decoration:none!important;background:#17191f }
      .support-whatsapp-link .whatsapp-brand-icon { flex:0 0 24px;width:24px;height:24px;margin:0 }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="login-support-email"><a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a></div>', unsafe_allow_html=True)
    icon_col, support_col = st.columns([0.16, 1])
    with icon_col:
        st.markdown(WHATSAPP_ICON_HTML, unsafe_allow_html=True)
    with support_col:
        with st.popover("Contact Support/Admin", use_container_width=True):
            st.markdown(f'<div class="support-contact-email"><a href="mailto:{ADMIN_EMAIL}">{ADMIN_EMAIL}</a></div>', unsafe_allow_html=True)
            for phone, number in SUPPORT_WHATSAPP_CONTACTS:
                st.markdown(f'<a class="support-whatsapp-link" href="https://wa.me/{number}" target="_blank" rel="noopener noreferrer">{WHATSAPP_ICON_HTML}<span>WhatsApp · {phone}</span></a>', unsafe_allow_html=True)
    if st.button("LOGIN AS ADMIN  ↗", use_container_width=True, key="admin_portal_link"):
        st.switch_page("pages/admin_dashboard.py")
    st.link_button("DOWNLOAD ANDROID APP (APK)", "https://github.com/icetrextrades-pixel/Aviator-Utility/releases/latest/download/AviatorUtility.apk", use_container_width=True)


def logout_user():
    """End the Supabase session and clear signed-in dashboard state."""
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state["pass"] = False
    st.session_state["user"] = ""
    st.session_state["user_email"] = ""
    st.session_state["user_id"] = ""
    st.session_state.pop("user_metadata", None)
    st.session_state["profile_theme"] = "Neon Cyan"
    st.session_state["onboarding_complete"] = False
    st.session_state["onboarding_step"] = 0
    st.session_state["onboarding_consent_checkbox"] = False
    st.session_state["current_signal"] = None
    st.session_state["signal_generated_at"] = 0.0
    st.session_state["refresh_after_round"] = False
    started_at = st.session_state.get("session_started_at", 0.0)
    elapsed_seconds = max(0, int(time.time() - started_at)) if started_at else 0
    elapsed_minutes, elapsed_remainder = divmod(elapsed_seconds, 60)
    st.session_state["auth_mode"] = "login"
    st.session_state["auth_notice"] = (
        f"Session recap — {elapsed_minutes}m {elapsed_remainder}s, "
        f"{st.session_state.get('session_signals_generated', 0)} signals generated, "
        f"{st.session_state.get('session_rounds_logged', 0)} rounds logged."
    )
    st.session_state["session_started_at"] = 0.0
    st.session_state["session_signals_generated"] = 0
    st.session_state["session_rounds_logged"] = 0
    st.session_state["session_spend_amount"] = 0.0
    st.session_state["session_budget_limit"] = 0.0
    st.session_state["session_time_limit_minutes"] = 30
    st.rerun()


def show_responsible_play_panel():
    """Offer user-set session and budget reminders; values are self-reported."""
    if not st.session_state.get("session_started_at"):
        st.session_state["session_started_at"] = time.time()

    with st.expander("00 / RESPONSIBLE PLAY · SESSION GUARDRAILS", expanded=False):
        st.caption(
            "Set a break reminder and an optional spending cap. Amounts are self-reported; "
            "this app does not read casino wallets or bets and cannot restrict activity on casino sites."
        )
        user_key = str(st.session_state.get("user_id", "member"))[:16]
        session_key = str(int(st.session_state.get("session_started_at", 0)))
        with st.form("responsible_play_limits"):
            limit_col, budget_col = st.columns(2)
            with limit_col:
                time_limit = st.select_slider(
                    "Break reminder",
                    options=[15, 30, 45, 60, 90],
                    value=int(st.session_state.get("session_time_limit_minutes", 30)),
                    format_func=lambda minutes: f"{minutes} minutes",
                    key=f"play_time_limit_{user_key}",
                )
            with budget_col:
                budget_limit = st.number_input(
                    "Optional spend cap · your currency",
                    min_value=0.0,
                    value=float(st.session_state.get("session_budget_limit", 0.0)),
                    step=1.0,
                    key=f"play_budget_limit_{user_key}",
                    help="Leave at 0 to turn the spend reminder off.",
                )
            spent = st.number_input(
                "Amount spent this session · self-reported",
                min_value=0.0,
                value=float(st.session_state.get("session_spend_amount", 0.0)),
                step=1.0,
                key=f"play_spent_{user_key}_{session_key}",
            )
            if st.form_submit_button("SAVE MY REMINDERS", use_container_width=True):
                st.session_state["session_time_limit_minutes"] = int(time_limit)
                st.session_state["session_budget_limit"] = float(budget_limit)
                st.session_state["session_spend_amount"] = float(spent)

        @st.fragment(run_every="30s")
        def update_session_reminders():
            started_at = st.session_state.get("session_started_at", 0.0)
            elapsed_minutes = (time.time() - started_at) / 60 if started_at else 0
            time_limit_value = int(st.session_state.get("session_time_limit_minutes", 30))
            progress_col, spend_col = st.columns(2)
            with progress_col:
                st.metric("TIME IN SESSION", f"{int(elapsed_minutes)} / {time_limit_value} min")
                st.progress(min(elapsed_minutes / max(time_limit_value, 1), 1.0))
                if elapsed_minutes >= time_limit_value:
                    st.warning("Your break reminder is due. Consider stepping away from the app and casino.")
            with spend_col:
                cap = float(st.session_state.get("session_budget_limit", 0.0))
                amount = float(st.session_state.get("session_spend_amount", 0.0))
                if cap > 0:
                    st.metric("SELF-REPORTED SPEND", f"{amount:.2f} / {cap:.2f}")
                    st.progress(min(amount / cap, 1.0))
                    if amount >= cap:
                        st.warning("You reached your chosen spend cap. Consider stopping for this session.")
                else:
                    st.metric("SELF-REPORTED SPEND", f"{amount:.2f}")
                    st.caption("Add a spend cap above to turn on the reminder.")

        update_session_reminders()


def show_signal_lab(casino_name: str, strategy: str):
    with st.expander("02A / SIGNAL LAB · TARGETS VS RESULTS", expanded=False):
        st.caption(f"Latest resolved records for {casino_name} · {strategy}. A hit means the logged result met or exceeded the saved target.")
        try:
            rows = fetch_signal_lab_rows(casino_name, strategy, limit=100)
        except Exception:
            st.info("Signal history is not available for this selection yet.")
            return

        total = len(rows)
        hits = sum(1 for row in rows if row.get("hit") is True)
        rate = round(hits / total * 100) if total else 0
        stat_a, stat_b, stat_c = st.columns(3)
        stat_a.metric("RESOLVED SAMPLE", total)
        stat_b.metric("HITS IN SAMPLE", hits)
        stat_c.metric("SAMPLE HIT RATE", f"{rate}%")
        if total >= 2:
            chart_rows = []
            for index, row in enumerate(rows, start=1):
                try:
                    chart_rows.append({
                        "Round": index,
                        "Signal target": float(row["predicted_multiplier"]),
                        "Actual result": float(row["actual_multiplier"]),
                    })
                except (TypeError, ValueError, KeyError):
                    continue
            if chart_rows:
                st.line_chart(chart_rows, x="Round", y=["Signal target", "Actual result"], use_container_width=True)
        else:
            st.info("Log more rounds to build a historical comparison.")
        st.caption("Historical data is descriptive only and does not guarantee or predict future results.")


def show_community_round_pulse():
    st.markdown('<div class="section-label">05 / COMMUNITY ROUND PULSE</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="feed-note">Latest member-submitted results across casinos. Entries are unverified and are not an official operator feed.</div>',
        unsafe_allow_html=True,
    )

    @st.fragment(run_every="15s")
    def refresh_round_pulse():
        try:
            latest = fetch_recent_round_pulse()
        except Exception:
            st.info("Community round pulse is unavailable right now.")
            return
        if not latest:
            st.info("No community round results have been logged yet.")
            return

        display_rows = []
        for row in latest:
            timestamp = row.get("created_at") or ""
            try:
                timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).astimezone(pytz.UTC).strftime("%d %b %H:%M:%S UTC")
            except (TypeError, ValueError):
                timestamp = str(timestamp)
            try:
                multiplier = f"{float(row.get('multiplier')):.2f}x"
            except (TypeError, ValueError):
                multiplier = str(row.get("multiplier", ""))
            display_rows.append({
                "Casino": row.get("casino") or "Unknown",
                "Result": multiplier,
                "Logged": timestamp,
            })
        st.dataframe(display_rows, hide_index=True, use_container_width=True)

    refresh_round_pulse()


TUTORIAL_VIDEO_HTML = """
<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box} body{margin:0;background:#07101a;color:#eff6ff;font-family:Arial,sans-serif}
.frame{height:148px;padding:16px 18px;border:1px solid #24465c;border-left:3px solid #10b981;
background:radial-gradient(ellipse at 85% 0%,rgba(16,185,129,.23),transparent 48%),linear-gradient(135deg,#0b1724,#07101a);
position:relative;overflow:hidden}
.kicker{font:800 9px monospace;letter-spacing:2px;color:#6ee7b7}
.title{font-size:18px;font-weight:900;margin-top:13px}
.copy{font:12px/1.45 Arial;color:#aab8c9;margin-top:5px;max-width:390px}
.track{position:absolute;bottom:0;left:0;height:3px;width:100%;background:#162736}
.fill{height:100%;width:0;background:#34d399;box-shadow:0 0 12px #34d399;animation:progress 5s linear infinite}
@keyframes progress{to{width:100%}}
.fade{animation:fade .5s ease}@keyframes fade{from{opacity:.15;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
@media(prefers-reduced-motion:reduce){.fade,.fill{animation:none}}
</style></head><body><div class="frame"><div id="scene" class="fade">
<div id="kicker" class="kicker"></div><div id="title" class="title"></div><div id="copy" class="copy"></div>
</div><div class="track"><div class="fill"></div></div></div>
<script>
const scenes=[
["01 / SELECT","Choose your analysis mode","PREDICTOR P25 · AVI10 weighted P50 · MR CRUSHER P75/P90."],
["02 / RECORD","Log the real result","Enter the actual multiplier after the round. 1.00x is valid."],
["03 / BUILD","Start with five rounds","References under 20 results are provisional."],
["04 / REVIEW","Press PREDICT","It summarizes your history; it cannot know the next crash."],
["05 / PLAY SAFE","Set limits and take breaks","Never chase losses or treat a reference as guaranteed."]
];
let i=0;const scene=document.getElementById("scene");
function show(){const s=scenes[i];document.getElementById("kicker").textContent=s[0];
document.getElementById("title").textContent=s[1];document.getElementById("copy").textContent=s[2];
scene.classList.remove("fade");void scene.offsetWidth;scene.classList.add("fade");i=(i+1)%scenes.length}
show();setInterval(show,5000);
</script></body></html>
"""


@st.dialog("FIRST-USE SETUP · TUTORIAL & TERMS", width="small")

def show_member_onboarding():
    """Guide each member through the app and record their current terms consent."""
    steps = [
        ("01 / WHAT THIS APP DOES", "Aviator Utility stores outcomes you enter and summarizes that history. It is not connected to a live casino result feed."),
        ("02 / CHOOSE YOUR ANALYSIS MODE", "PREDICTOR uses a conservative lower-quartile P25. AVI10 uses a recency-weighted median P50. MR CRUSHER blends upper-tail P75/P90 for higher variance; it does not improve the next round's odds. Each member's history is separate."),
        ("03 / LOG REAL OUTCOMES", "After a round ends, enter its actual multiplier and choose LOG ROUND RESULT. A 1.00x result is valid. Never guess or invent results. Five rounds unlock an early reference; fewer than 20 makes it provisional."),
        ("04 / READ REFERENCES CAREFULLY", "Each mode shows an observed historical target rate with a 95% Wilson uncertainty range. This summarizes submitted results only, not the probability of the next round. PREDICT remains a historical reference, not a forecast or promise of a win."),
        ("05 / TERMS, RISK & ACCOUNT PRIVACY", "Use the app only where lawful and only if you meet the legal age requirement. You are responsible for your choices and any losses. Set a time and spending limit, never borrow or chase losses, and stop if play is causing harm. Use the app at your own risk. Your password is private: Supabase verifies it, but neither the admin directory nor your profile can read it.")
    ]
    step = max(0, min(int(st.session_state.get("onboarding_step", 0)), len(steps) - 1))
    title, body = steps[step]
    st.progress((step + 1) / len(steps), text=f"SETUP {step + 1} / {len(steps)}")
    st.markdown(f"**{title}**\n\n{body}")

    if step == 0:
        st.caption("QUICK AUTOPLAY WALKTHROUGH · about 25 seconds")
        components.html(TUTORIAL_VIDEO_HTML, height=152, scrolling=False)

    if step == len(steps) - 1:
        st.markdown("---")
        st.markdown("**TERMS & CONDITIONS**")
        st.markdown(
            "This app provides historical summaries for information only. It has no live casino feed, "
            "cannot predict independent outcomes, and makes no claim of accuracy or profit. Gambling "
            "can cause financial and personal harm. You remain responsible for following local laws, "
            "setting limits, and every decision you make."
        )
        agreed = st.checkbox(
            "I have read the tutorial and terms. I agree to use this app at my own risk.",
            key="onboarding_consent_checkbox",
        )
        if st.button("I AGREE — CONTINUE", type="primary", use_container_width=True, disabled=not agreed):
            try:
                accepted_at = datetime.now(pytz.UTC).isoformat()
                response = supabase.auth.update_user({
                    "data": {
                        ONBOARDING_TERMS_KEY: ONBOARDING_TERMS_VERSION,
                        "aviator_terms_accepted_at": accepted_at,
                    }
                })
                updated_user = getattr(response, "user", None)
                if not updated_user:
                    raise RuntimeError("Supabase did not confirm the terms update.")
                st.session_state["onboarding_complete"] = True
                st.session_state["onboarding_step"] = 0
                st.rerun()
            except Exception:
                st.error("Could not save your consent to your account. Please try again; you must agree before entering the app.")
        st.caption("You can review this guide again any time by logging in again.")
    else:
        back_col, next_col = st.columns(2)
        with back_col:
            if step > 0 and st.button("← BACK", use_container_width=True):
                st.session_state["onboarding_step"] = step - 1
                st.rerun()
        with next_col:
            if st.button("NEXT STEP →", type="primary", use_container_width=True):
                st.session_state["onboarding_step"] = step + 1
                st.rerun()


def show_dashboard():
    active_tab = st.session_state["active_tab"]
    strat = STRATEGIES[active_tab]
    accent = strat["accent_color"]
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    show_profile_sidebar()
    theme_accents = {"Neon Cyan": "#06d6c7", "Electric Violet": "#a855f7", "Ember": "#fb7185"}
    profile_accent = theme_accents.get(st.session_state.get("profile_theme"), "#06d6c7")
    st.markdown(f"<style>:root {{ --accent: {profile_accent}; --accent-soft: color-mix(in srgb, {profile_accent} 20%, transparent); }}</style>", unsafe_allow_html=True)
    st.markdown(f"<style>:root {{ --accent: {accent}; --accent-soft: color-mix(in srgb, {accent} 20%, transparent); }}</style>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="top-nav">
      <span>AVI10 / NEURAL MATRIX &nbsp;•&nbsp; MEMBER: {st.session_state['user'].upper()}</span>
      <span><span class="live">● SECURE SESSION</span> &nbsp; / &nbsp; ZIMBABWE STANDARD TIME</span>
    </div>
    """, unsafe_allow_html=True)

    _, logout_col = st.columns([5, 1.4])
    with logout_col:
        if st.button("LOG OUT", icon=":material/logout:", use_container_width=True, key="logout_button"):
            logout_user()

    show_responsible_play_panel()

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
        # Zimbabwe operators with official online platforms.
        "AFRICABET": "https://www.africabet.com/",
        "BEZBETS - ZIMBABWE": "https://bezbets.co.zw/",
        "BEULABET - ZIMBABWE": "https://beulabet.com/",
        "BET247 - ZIMBABWE": "https://www.bet247.co.zw/",
        "BOLABET - ZIMBABWE": "https://www.bolabet.co.zw/",
        "BESHSPORT - ZIMBABWE": "https://beshsport.bet/",
        "JUMBOBETS - ZIMBABWE": "https://jumbobets.co.zw/",
        "LUCKYBETS - ZIMBABWE": "https://luckybets.co.zw/",
        "MEGABET - ZIMBABWE": "https://megabet.co.zw/",
        "MWOS - ZIMBABWE": "https://betting.co.zw/",
        "PRIDEBET - ZIMBABWE": "https://pridebet.co.zw/",
        "WINBUCKS - ZIMBABWE": "https://winbucks.co.zw/",
        # Regional and international operators. Availability varies by country.
        "1XBET": "https://www.1xbet.com/",
        "BET365": "https://www.bet365.com/",
        "BETFAIR": "https://www.betfair.com/",
        "PREMIER BET": "https://www.premierbet.com/",
        "STAKE": "https://stake.com/",
        "DAFABET": "https://www.dafabet.com/",
        "BETIKA - KENYA": "https://www.betika.com/en-ke/",
        "BETIKA - ZAMBIA": "https://www.betika.co.zm/",
        "SPORTPESA - KENYA": "https://www.ke.sportpesa.com/",
        "BET9JA - NIGERIA": "https://www.bet9ja.com/",
        "HOLLYWOODBETS - SOUTH AFRICA": "https://www.hollywoodbets.net/",
        "BETWAY - ZAMBIA": "https://www.betway.co.zm/",
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
        signal = generate_signal(live_history, active_tab)
        if signal is not None:
            st.session_state["session_signals_generated"] = st.session_state.get("session_signals_generated", 0) + 1
            st.session_state["current_signal"] = signal
            st.session_state["signal_generated_at"] = time.time()
            st.session_state["signal_casino"] = selected_casino
            st.session_state["signal_mode"] = active_tab
            save_prediction(selected_casino, active_tab, signal)
        else:
            st.session_state["current_signal"] = None
        st.session_state["refresh_after_round"] = False

    st.markdown('<div class="section-label">02 / LIVE HISTORY REFERENCE</div>', unsafe_allow_html=True)
    gen_col, band_col = st.columns([2.3, 1.3])
    with gen_col:
        if st.button("PREDICT", use_container_width=True, type="primary", key="generate_signal", disabled=len(live_history) < MIN_REFERENCE_ROUNDS):
            signal = generate_signal(live_history, active_tab)
            if signal is None:
                st.warning(f"Log at least {MIN_REFERENCE_ROUNDS} valid round results before generating an early historical reference.")
            else:
                st.session_state["session_signals_generated"] = st.session_state.get("session_signals_generated", 0) + 1
                st.session_state["current_signal"] = signal
                st.session_state["signal_generated_at"] = time.time()
                st.session_state["signal_casino"] = selected_casino
                st.session_state["signal_mode"] = active_tab
                save_prediction(selected_casino, active_tab, signal)
                st.rerun()
    with band_col:
        st.metric("TARGET BAND", f"{strat['min_target']:.1f}–{strat['max_target']:.1f}x")
        st.caption(strat["method_note"])

    accuracy = get_accuracy_stats(selected_casino, active_tab)
    recent_signals = get_recent_signals(selected_casino, active_tab)
    current_signal = st.session_state.get("current_signal")
    matching_signal = (st.session_state.get("signal_casino") == selected_casino and st.session_state.get("signal_mode") == active_tab)
    if current_signal is not None and not matching_signal:
        current_signal = None
    if current_signal is None:
        if len(live_history) < MIN_REFERENCE_ROUNDS:
            st.info(f"Log {MIN_REFERENCE_ROUNDS - len(live_history)} more real round result(s) to generate an early historical reference. You can refine it as more rounds are added.")
        else:
            st.info("Generate a reference for this casino and department using the PREDICT button above.")
        render_signal_card(active_tab, 0.0, confidence, recent_signals, accuracy, last_round_at=get_latest_round_timestamp(selected_casino))
    else:
        render_signal_card(
            active_tab, current_signal, confidence, recent_signals, accuracy,
            st.session_state.get("signal_generated_at", 0.0),
            get_latest_round_timestamp(selected_casino),
        )
    if MIN_REFERENCE_ROUNDS <= len(live_history) < MATURE_REFERENCE_ROUNDS:
        st.warning(f"EARLY SAMPLE: {len(live_history)} rounds recorded. Treat this reference as provisional until at least {MATURE_REFERENCE_ROUNDS} rounds are available.")
    if current_signal is not None:
        target_stats = estimate_historical_target_rate(live_history, current_signal)
        probability_col, interval_col = st.columns(2)
        probability_col.metric(
            "HISTORICAL TARGET RATE",
            f"{target_stats['rate']:.1f}%",
            f"{target_stats['hits']} / {target_stats['total']} logged rounds reached target",
        )
        interval_col.metric(
            "95% WILSON UNCERTAINTY RANGE",
            f"{target_stats['low']:.1f}–{target_stats['high']:.1f}%",
        )
        st.caption("Observed sample frequency and its 95% Wilson interval only. This is not the probability of the next round.")
    st.caption("Every logged result, including 1.00x, resolves the previous reference check. New references summarize logged history; they do not sync to a casino feed or forecast the next independent round.")

    show_signal_lab(selected_casino, active_tab)

    show_historical_odds_lab(selected_casino)

    st.markdown('<div class="section-label">03 / ROUND DATA & ACCURACY</div>', unsafe_allow_html=True)
    round_col, submit_col, stats_col = st.columns([1.5, 1, 2])
    with round_col:
        round_multiplier = st.number_input("ACTUAL MULTIPLIER", min_value=1.00, max_value=100.00, value=1.50, step=0.05, format="%.2f", key="round_multiplier")
    with submit_col:
        st.write("")
        if st.button("LOG ROUND RESULT", use_container_width=True, key="log_round"):
            if insert_round_result(selected_casino, float(round_multiplier), active_tab):
                st.session_state["session_rounds_logged"] = st.session_state.get("session_rounds_logged", 0) + 1
                st.session_state["refresh_after_round"] = True
                st.success(f"Logged {round_multiplier:.2f}x to {selected_casino}; refreshing from the updated history.")
                st.rerun()
            else:
                st.error("Could not save the round. Open the diagnostic details below and share them with the administrator.")
                save_error = st.session_state.get("round_save_error", "")
                if save_error:
                    with st.expander("ROUND SAVE DIAGNOSTICS"):
                        st.caption("These details are visible only in your signed-in session. Do not share passwords or API keys.")
                        st.code(save_error)
                        error_upper = save_error.upper()
                        if "PGRST205" in error_upper or "42P01" in error_upper:
                            st.warning("The round_history table may be missing or absent from Supabase's API schema cache. Apply the round-history migration from this repository, then reload the app.")
                        elif "42501" in error_upper or "ROW LEVEL SECURITY" in error_upper or "PERMISSION DENIED" in error_upper:
                            st.warning("Supabase rejected the insert. Check that the signed-in user has the authenticated INSERT grant and the insert_own_rounds policy on public.round_history.")
                        elif "23503" in error_upper:
                            st.warning("Supabase rejected the user ID reference. Confirm the logged-in user's ID exists in auth.users and that round_history.user_id references auth.users(id).")

    with stats_col:
        st.metric("ROUNDS STORED", round_count)
    st.markdown("""
    <div class="feed-note">
      <b>DATA SOURCE STATUS</b><br>
      The selected operator button opens its website. This build has no official operator result feed connected.
      Round values entered here are saved to Supabase and are then used for that operator's history and signal calculations.
      References are empirical quantiles of logged data, not forecasts. Crash rounds remain unpredictable.
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
    show_community_round_pulse()

    st.markdown('<div class="footer-line">AVI10 NEURAL MATRIX &nbsp;•&nbsp; EDGE SYSTEMS / SESSION ACTIVE</div>', unsafe_allow_html=True)

# ==============================================================================
# 8. APP NAVIGATION
# ==============================================================================
def run_predictor_page():
    if not st.session_state["pass"]:
        show_login()
    elif not st.session_state.get("onboarding_complete", False):
        show_member_onboarding()
    else:
        show_dashboard()


predictor_page = st.Page(
    run_predictor_page,
    title="Predictor",
    url_path="predictor",
    default=True,
)
admin_page = st.Page(
    "pages/admin_dashboard.py",
    title="Admin Access",
    url_path="admin",
    visibility="hidden",
)
current_page = st.navigation([predictor_page, admin_page], position="hidden")
if current_page.url_path != admin_page.url_path:
    prior_admin_client = st.session_state.get("admin_supabase_client")
    if st.session_state.get("admin_authenticated") and prior_admin_client:
        try:
            prior_admin_client.auth.sign_out()
        except Exception:
            pass
    for key in ("admin_authenticated", "admin_email", "admin_supabase_client"):
        st.session_state.pop(key, None)
current_page.run()
