import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json 



# ------------------------------------------------- GOOGLE SHEET CONFIG----------------------------------------------------



SHEET_NAME = "Student Attendance"


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
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Error: Spreadsheet '{SHEET_NAME}' not found. Please ensure the name is exact and the sheet has been shared.")
        return None
    except KeyError:
        st.error("Error: GCP service account credentials not found in st.secrets.toml.")
        return None
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None



#---------------------------------------------------- WRITE IN THE GOOGLE SHEET----------------------------------------------------------



def write_to_sheet(sheet, data_row: dict):
    if sheet is None:
        return False, "Sheet connection is not available."

    try:
        headers = sheet.row_values(1)
        if not headers:
            return False, "Could not read headers from the attendance sheet."

        if "Date" in data_row:
             data_row["Date"] = str(data_row["Date"])

        ordered_data = [data_row.get(h, "") for h in headers]

        sheet.append_row(ordered_data)

        return True, " Attendance data saved to sheet successfully."
    except Exception as e:
        print(f"!!! Error writing to attendance sheet: {e}") # Log detailed error server-side
        return False, f" Error writing attendance log: {e}"



#----------------------------------------- READ FROM THE GOOGLE SHEET-------------------------------



def read_attendance_sheet(sheet):
    if sheet is None: 
        return []
    try:
        data = sheet.get_all_records() 
        return data
    except Exception as e:
        st.error(f" Error reading attendance sheet: {e}")
        return []
    
    
    