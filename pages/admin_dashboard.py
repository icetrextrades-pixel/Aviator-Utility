import hmac
import os
from datetime import datetime, timezone

import streamlit as st
from supabase import create_client

ADMIN_EMAIL = "icetrextrades@gmail.com"


def config_value(*names: str) -> str:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()
    try:
        for name in names:
            value = st.secrets.get(name)
            if value:
                return str(value).strip()
    except Exception:
        pass
    return ""


SUPABASE_URL = config_value("SUPABASE_URL", "VITE_SUPABASE_URL")
SUPABASE_PUBLIC_KEY = config_value(
    "SUPABASE_KEY", "SUPABASE_ANON_KEY", "SUPABASE_PUBLISHABLE_KEY", "VITE_SUPABASE_ANON_KEY"
)
SUPABASE_ADMIN_KEY = config_value("SUPABASE_SECRET_KEY", "SUPABASE_SERVICE_ROLE_KEY")
ADMIN_ACCESS_CODE = config_value("ADMIN_ACCESS_CODE")


ADMIN_CSS = """
<style>
[data-testid="stAppViewContainer"] {
  background:
    radial-gradient(ellipse at 18% 8%, rgba(33, 101, 255, .16), transparent 32%),
    radial-gradient(ellipse at 86% 72%, rgba(0, 232, 203, .12), transparent 30%),
    linear-gradient(145deg, #050817, #080d1d 48%, #040610);
  color: #e6f1ff;
  overflow: hidden;
}
[data-testid="stAppViewContainer"]::before {
  content: ""; position: fixed; inset: -25%; pointer-events: none; z-index: 0;
  background:
    radial-gradient(circle at 22% 35%, rgba(38, 120, 255, .14), transparent 25%),
    radial-gradient(circle at 72% 58%, rgba(0, 255, 214, .10), transparent 23%);
  filter: blur(18px);
  animation: admin-aurora 18s ease-in-out infinite alternate;
}
[data-testid="stAppViewContainer"]::after {
  content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0; opacity: .16;
  background-image: linear-gradient(rgba(115, 167, 220, .15) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(115, 167, 220, .15) 1px, transparent 1px);
  background-size: 44px 44px;
  mask-image: linear-gradient(to bottom, black, transparent 92%);
}
.block-container { position: relative; z-index: 1; max-width: 1120px; padding-top: 2.4rem; }
.admin-kicker { color:#65e7dc; letter-spacing:3px; font:800 10px ui-monospace,monospace; }
.admin-hero {
  position:relative; overflow:hidden; padding:26px 28px; margin:8px 0 22px;
  border:1px solid rgba(91,160,255,.28); border-top:2px solid #36d8d2;
  background:linear-gradient(120deg,rgba(10,22,45,.88),rgba(8,17,31,.72));
  box-shadow:0 24px 75px rgba(0,0,0,.34), inset 0 0 38px rgba(42,141,255,.06);
  clip-path:polygon(0 0,97% 0,100% 12%,100% 100%,3% 100%,0 88%);
}
.admin-hero::after {
  content:""; position:absolute; width:34%; height:220%; top:-60%; left:-40%;
  background:linear-gradient(90deg,transparent,rgba(56,220,228,.11),transparent);
  transform:rotate(20deg); animation:admin-scan 9s linear infinite;
}
.admin-title { margin:6px 0 4px; color:#f2f8ff; font-size:clamp(28px,5vw,43px); font-weight:900; letter-spacing:-1.5px; }
.admin-subtitle { color:#97abc5; font:600 12px ui-monospace,monospace; letter-spacing:1px; }
.admin-card {
  padding:20px; border:1px solid rgba(118,163,219,.2);
  background:linear-gradient(145deg,rgba(12,23,42,.92),rgba(7,13,25,.92));
  box-shadow:0 14px 44px rgba(0,0,0,.22);
}
.admin-chip { color:#5eead4; font:800 9px ui-monospace,monospace; letter-spacing:2px; }
.admin-note { color:#96a9c1; font:500 12px/1.7 ui-monospace,monospace; }
@keyframes admin-aurora { from { transform:translate3d(-2%,1%,0) scale(.96); } to { transform:translate3d(3%,-2%,0) scale(1.07); } }
@keyframes admin-scan { from { left:-48%; } to { left:130%; } }
@media (prefers-reduced-motion: reduce) {
  [data-testid="stAppViewContainer"]::before,.admin-hero::after { animation:none; }
}
</style>
"""


def authenticate_admin(email: str, password: str, access_code: str):
    if not ADMIN_ACCESS_CODE:
        st.error("The private admin gate is not configured yet. Add ADMIN_ACCESS_CODE in Streamlit server-side Secrets.")
        return
    if not SUPABASE_URL or not SUPABASE_PUBLIC_KEY:
        st.error("Supabase authentication is not configured for this deployment.")
        return
    if email.strip().lower() != ADMIN_EMAIL.lower():
        st.error("This account is not on the administrator allowlist.")
        return
    if not hmac.compare_digest(access_code.encode("utf-8"), ADMIN_ACCESS_CODE.encode("utf-8")):
        st.error("The administrator access code is incorrect.")
        return

    try:
        client = create_client(SUPABASE_URL, SUPABASE_PUBLIC_KEY)
        response = client.auth.sign_in_with_password({
            "email": email.strip().lower(),
            "password": password,
        })
        user = getattr(response, "user", None)
        actual_email = (getattr(user, "email", "") or "").strip().lower()
        if not user or actual_email != ADMIN_EMAIL.lower():
            st.error("Supabase did not authenticate the allowlisted admin account.")
            return
        st.session_state["admin_authenticated"] = True
        st.session_state["admin_email"] = actual_email
        st.session_state["admin_supabase_client"] = client
        st.rerun()
    except Exception:
        st.error("Admin sign-in failed. Check the email, password, and Supabase approval status.")


def fetch_members(limit: int = 1000) -> list:
    if not SUPABASE_ADMIN_KEY:
        raise RuntimeError("SUPABASE_SECRET_KEY is not configured in Streamlit Secrets.")
    client = create_client(SUPABASE_URL, SUPABASE_ADMIN_KEY)
    response = client.auth.admin.list_users(page=1, per_page=limit)
    if isinstance(response, list):
        users = response
    elif isinstance(response, dict):
        users = response.get("users") or response.get("data") or []
    else:
        users = getattr(response, "users", None) or getattr(response, "data", None) or []

    rows = []
    for user in users:
        def value(name, default=None):
            return user.get(name, default) if isinstance(user, dict) else getattr(user, name, default)

        email = value("email", "") or ""
        app_metadata = value("app_metadata", {}) or {}
        approved = app_metadata.get("aviator_access_approved") is True or email.lower() == ADMIN_EMAIL.lower()
        banned_until = value("banned_until")
        restricted = bool(banned_until) and str(banned_until).lower() != "none"
        rows.append({
            "_user_id": value("id", ""),
            "_app_metadata": app_metadata,
            "Email": email,
            "Status": "Restricted" if restricted else ("Approved" if approved else "Pending approval"),
        })
    return rows

def show_admin_login():
    st.markdown(
        '<div class="admin-hero"><div class="admin-kicker">PRIVATE CONTROL PLANE / ACCESS GATE</div>'
        '<div class="admin-title">Administrator Console</div>'
        '<div class="admin-subtitle">IDENTITY CHECK · SECOND FACTOR · SERVER-SIDE AUTHORIZATION</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="admin-card"><div class="admin-chip">RESTRICTED SIGN-IN</div>'
                '<p class="admin-note">Use the allowlisted Supabase administrator account and the private access code configured only in Streamlit Secrets.</p></div>',
                unsafe_allow_html=True)
    if not ADMIN_ACCESS_CODE:
        with st.expander("SET UP THE PRIVATE ADMIN ACCESS CODE", expanded=True):
            st.write("In Streamlit Community Cloud, open this app’s Settings → Secrets and add a unique, long code. Do not add it to GitHub or share it in chat.")
            st.code('ADMIN_ACCESS_CODE = "paste-a-unique-random-code-here"', language="toml")
    with st.form("private_admin_login"):
        email = st.text_input("ADMIN EMAIL")
        password = st.text_input("SUPABASE PASSWORD", type="password")
        code = st.text_input("PRIVATE ADMIN ACCESS CODE", type="password")
        submitted = st.form_submit_button("VERIFY ADMIN ACCESS", use_container_width=True)
    if submitted:
        authenticate_admin(email, password, code)
    st.markdown('<a href="/" style="color:#a8bdd7;text-decoration:none;font:700 11px ui-monospace,monospace">↩ RETURN TO MAIN APP</a>', unsafe_allow_html=True)


def show_admin_dashboard():
    st.markdown(ADMIN_CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="admin-hero"><div class="admin-kicker">PRIVATE CONTROL PLANE / AUTHORIZED SESSION</div>'
        '<div class="admin-title">Administrator Console</div>'
        '<div class="admin-subtitle">ACCOUNT OVERSIGHT · MEMBER ACCESS · SECURE OPERATIONS</div></div>',
        unsafe_allow_html=True,
    )
    email = st.session_state.get("admin_email", "")
    top_left, top_right = st.columns([4, 1])
    top_left.markdown(f'<div class="admin-chip">VERIFIED ADMIN&nbsp;&nbsp; / &nbsp;&nbsp;{email}</div>', unsafe_allow_html=True)
    if top_right.button("SIGN OUT", use_container_width=True):
        client = st.session_state.get("admin_supabase_client")
        try:
            if client:
                client.auth.sign_out()
        except Exception:
            pass
        for key in ("admin_authenticated", "admin_email", "admin_supabase_client"):
            st.session_state.pop(key, None)
        st.rerun()

    try:
        members = fetch_members()
    except Exception as exc:
        st.error("The private member list could not be loaded.")
        if email.lower() == ADMIN_EMAIL.lower():
            st.caption(f"Admin data service: {type(exc).__name__}: {str(exc)[:300]}")
        return

    pending = [row for row in members if row["Status"] == "Pending approval"]
    approved_count = sum(row["Status"] == "Approved" for row in members)
    restricted = sum(row["Status"] == "Restricted" for row in members)
    m1, m2, m3 = st.columns(3)
    m1.metric("AUTH ACCOUNTS", len(members))
    m2.metric("APPROVED", approved_count)
    m3.metric("PENDING", len(pending))
    st.markdown('<div class="admin-card"><div class="admin-chip">MEMBER ACCESS DIRECTORY</div>'
                '<p class="admin-note">Email and approval state only. Passwords are never viewable. Usernames are not shown here.</p></div>',
                unsafe_allow_html=True)
    if members:
        st.dataframe([{"Email": row["Email"], "Status": row["Status"]} for row in members],
                     use_container_width=True, hide_index=True)
    else:
        st.info("No provisioned Supabase Auth accounts were returned.")

    if pending:
        labels = {row["Email"]: row for row in pending}
        with st.form("approve_member_account"):
            selected_email = st.selectbox("PENDING EMAIL", list(labels.keys()))
            approve = st.form_submit_button("APPROVE ACCOUNT", type="primary", use_container_width=True)
        if approve:
            row = labels[selected_email]
            if not SUPABASE_ADMIN_KEY:
                st.error("SUPABASE_SECRET_KEY is not configured in Streamlit Secrets.")
            else:
                try:
                    admin_client = create_client(SUPABASE_URL, SUPABASE_ADMIN_KEY)
                    app_metadata = dict(row.get("_app_metadata") or {})
                    app_metadata["aviator_access_approved"] = True
                    admin_client.auth.admin.update_user_by_id(
                        row["_user_id"],
                        {"app_metadata": app_metadata, "email_confirm": True},
                    )
                    st.success(f"Approved {selected_email}. The member can now sign in.")
                    st.rerun()
                except Exception:
                    st.error("Supabase could not approve this account. Check the admin service key and try again.")


def main():
    st.markdown(ADMIN_CSS, unsafe_allow_html=True)
    st.markdown('<div class="admin-kicker">PRIVATE ADMIN GATE</div>', unsafe_allow_html=True)
    if (
        st.session_state.get("admin_authenticated") is True
        and st.session_state.get("admin_email", "").lower() == ADMIN_EMAIL.lower()
    ):
        show_admin_dashboard()
    else:
        st.session_state["admin_authenticated"] = False
        show_admin_login()


main()
