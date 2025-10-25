import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

SHEET_NAME = "STUDENT-DETAILS" # <-- Make sure this is your exact sheet name

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

def write_to_sheet(sheet, data_row: dict):
    try:
        headers = sheet.row_values(1)
        
        if "S_live_face_photos" in data_row:
            data_row["S_live_face_photos"] = json.dumps(data_row["S_live_face_photos"])
        
        # Convert date to string
        if "S_dob" in data_row:
            data_row["S_dob"] = str(data_row["S_dob"])

        ordered_data = [data_row.get(h, "") for h in headers]
        sheet.append_row(ordered_data)
        
        return True, "✅ Data saved to sheet successfully."
    except Exception as e:
        return False, f"⚠️ Error writing to sheet: {e}"
    
def read_from_sheet(sheet):
    """
    Reads all data from the sheet (except the header row)
    and returns it as a list of dictionaries.
    """
    try:
        # get_all_records() is a powerful gspread function that
        # automatically uses row 1 as keys for the dictionaries.
        data = sheet.get_all_records()
        return data
    except Exception as e:
        st.error(f"⚠️ Error reading from sheet: {e}")
        # Return an empty list on failure
        return []

def clear_sheet(sheet):
    
    try:
        row_count = sheet.row_count
        
        
        if row_count > 1:
            print(f"Clear Sheet: Attempting to delete rows 2 to {row_count}.") # <-- Add Print
            sheet.delete_rows(2, row_count)
            print("Clear Sheet: Deletion command sent.") # <-- Add Print
            return True
        else:
            print("Clear Sheet: No rows to delete (only header exists).") # <-- Add Print
            return True
        
        
    except Exception as e:
        print(f"!!! Clear Sheet Error: {e}") # <-- Add Print
        st.error(f"⚠️ Error clearing sheet: {e}")
        return False