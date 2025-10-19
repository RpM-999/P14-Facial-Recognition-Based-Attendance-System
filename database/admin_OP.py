import streamlit as st
from supabase import create_client
from gotrue.errors import AuthApiError

from supabase import Client
import streamlit as st

def admin_verification(email: str, password: str, supabase: Client):
    try:
        auth_res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_res.user
        if not user:
            return False, "❌ Invalid email or password"
        
        return True, f"✅ Logged in as {user.email}"

    except Exception as e:
        return False, f"⚠️ Login failed: {e}"
