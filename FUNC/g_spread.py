import streamlit as st
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import json

SHEET_NAME = "STUDENT DETAILS"


# ----------------------------------------------------- CONNECT TO GOOGLE SHEET ----------------------------------------------------------

@st.cache_resource(ttl=60)
def connect_to_gsheet():
    try:
        creds_dict = st.secrets["gcp_service_account"]

        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        client = gspread.authorize(creds)

        sheet = client.open(SHEET_NAME).sheet1
        return sheet

    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None


# ----------------------------------------------------------- WRITE DATA ----------------------------------------------------------

def write_to_sheet(sheet, data_row: dict):
    try:
        headers = sheet.row_values(1)

        if "S_live_face_photos" in data_row:
            data_row["S_live_face_photos"] = json.dumps(data_row["S_live_face_photos"])

        if "S_dob" in data_row:
            data_row["S_dob"] = str(data_row["S_dob"])

        ordered_data = [data_row.get(h, "") for h in headers]
        sheet.append_row(ordered_data)

        return True, "Data saved to sheet successfully."

    except Exception as e:
        return False, f"Error writing to sheet: {e}"


# ------------------------------------------------------------ READ DATA ----------------------------------------------------------

def read_from_sheet(sheet):
    try:
        raw_rows = sheet.get_all_records()

        mapped_rows = []
        for row in raw_rows:
            mapped_row = {
                "S_name": row.get("STUDENT_NAME", ""),
                "S_mail": row.get("STUDENT_MAIL", ""),
                "S_phone": str(row.get("STUDENT_PHONE", "")),
                "S_dob": row.get("STUDENT_DOB", ""),
                "S_Address": row.get("STUDENT_ADDRESS", ""),
                "dep_id": row.get("DEPARTMENT_ID", ""),
                "S_admisionYear": row.get("STUDENT_ADMISSION_YEAR", ""),
                "S_live_face_photos": row.get("STUDENT_PHOTO_EMBEDDING", "[]"),
            }
            mapped_rows.append(mapped_row)

        return mapped_rows

    except Exception as e:
        st.error(f"Error reading from sheet: {e}")
        return []


# ------------------------------------------------------------- CLEAR SHEET (FULL) ----------------------------------------------------------

def clear_sheet(sheet):
    try:
        row_count = sheet.row_count

        if row_count > 1:
            sheet.delete_rows(2, row_count)

        return True

    except Exception as e:
        st.error(f"Error clearing sheet: {e}")
        return False

