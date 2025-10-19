# app.py
import streamlit as st
from supabase import create_client
from typing import Optional, Dict, Any

# --- Load Supabase credentials from Streamlit secrets ---
# Put these in your .streamlit/secrets.toml:
# [supabase]
# url = "https://<YOUR-PROJECT>.supabase.co"
# anon_key = "<YOUR-ANON-KEY>"
SUPABASE_URL = st.secrets["supabase"]["url"]
SUPABASE_ANON_KEY = st.secrets["supabase"]["anon_key"]

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

st.set_page_config(page_title="Sign up (Supabase + Streamlit)")

st.title("Create an account")

with st.form("signup_form"):
    full_name = st.text_input("Full name", max_chars=100)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm password", type="password")
    use_magic_link = st.checkbox("Send magic link instead of password (email-only sign-in)")
    submitted = st.form_submit_button("Sign up")

def create_profile_record(user_id: str, email: str, full_name: Optional[str] = None):
    """Insert a profile row into `profiles` table. The table schema should allow `id` and `email` fields."""
    try:
        payload = {"id": user_id, "email": email}
        if full_name:
            payload["full_name"] = full_name
        resp = supabase.table("profiles").insert(payload).execute()
        return resp
    except Exception as e:
        # Don't crash the app; return error
        return {"error": str(e)}

if submitted:
    # Basic client-side validation
    if not email:
        st.error("Please enter an email.")
    elif not use_magic_link and (not password or not password_confirm):
        st.error("Please enter and confirm a password.")
    elif not use_magic_link and password != password_confirm:
        st.error("Passwords do not match.")
    else:
        try:
            if use_magic_link:
                # Sign up with email only — Supabase will send a magic link if your project is configured.
                # Different client versions may require different shapes — we handle common return formats below.
                result = supabase.auth.sign_up({
                    "email": email,
                    "password": "temporary-password"  # Required by newer Supabase versions
                })
            else:
                # Sign up with email + password
                result = supabase.auth.sign_up({
                    "email": email,
                    "password": password
                })

            # `result` shape depends on the supabase client version. Handle both common patterns.
            data = None
            error = None
            user = None

            # Pattern 1: dict-like with 'data' and 'error'
            if isinstance(result, dict) and "data" in result and "error" in result:
                data = result.get("data")
                error = result.get("error")
                # user might be in data['user'] or data.get('user')
                if isinstance(data, dict):
                    user = data.get("user") or data.get("user", None)
            # Pattern 2: object-like with properties
            else:
                # Some versions return an object with .user / .error
                user = getattr(result, "user", None)
                error = getattr(result, "error", None)
                data = getattr(result, "data", None)

            if error:
                st.error(f"Sign-up error: {error}")
            else:
                # If user found, create profile row
                user_id = None
                if user is not None:
                    if isinstance(user, dict):
                        user_id = str(user.get("id", ""))
                    elif hasattr(user, "id"):
                        user_id = str(getattr(user, "id", ""))

                # Show success message depending on sign-up flow
                if use_magic_link:
                    st.success("If your email is valid, Supabase has sent a magic link to sign in.")
                else:
                    st.success("Sign-up successful. Please check your email to confirm (if confirmation is enabled).")

                # Optionally create a `profiles` entry if we have a user id
                if user_id:
                    profile_resp = create_profile_record(user_id, email, full_name)
                    if isinstance(profile_resp, dict) and profile_resp.get("error"):
                        st.warning(f"Couldn't create profile row: {profile_resp['error']}")
                    else:
                        st.info("Profile saved (profiles table).")
                else:
                    st.info("User created but no user id returned by the client; skipping profile insert.")

                # For debugging / developer info (avoid showing sensitive tokens in production)
                st.write("---")
                st.write("Debug info (non-sensitive):")
                st.json({
                    "user_returned": bool(user),
                    "user_id": user_id
                })

        except Exception as exc:
            st.error(f"An exception occurred while signing up: {str(exc)}")
