import streamlit as st
from supabase import Client
from gotrue.errors import AuthApiError

def admin_verification(email: str, password: str, supabase: Client):
    try:
        auth_res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_res.user
        if not user:
            return False, "Invalid email or password"
        
        # --- MODIFICATION ---
        # Return the actual email, not a success message
        return True, user.email 

    except AuthApiError as e:
        # Give a clearer error message from Supabase
        return False, f"⚠️ {e.message}"
    except Exception as e:
        return False, f"⚠️ An unexpected error occurred: {e}"