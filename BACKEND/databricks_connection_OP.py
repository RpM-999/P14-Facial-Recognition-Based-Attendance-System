import requests
import streamlit as st

def trigger_databricks_job(job_type):
    try:
        host = st.secrets["databricks"]["host"]
        token = st.secrets["databricks"]["token"]

        job_map = {
            "student": st.secrets["databricks"]["student_job_id"],
            "department": st.secrets["databricks"]["department_job_id"],
            "attendance": st.secrets["databricks"]["attendance_job_id"]
        }

        job_id = job_map[job_type]

        url = f"{host}/api/2.1/jobs/run-now"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        payload = {
            "job_id": int(job_id)
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return True, f" {job_type} pipeline triggered successfully"
        else:
            return False, f" Failed: {response.text}"

    except Exception as e:
        return False, str(e)
    




def get_job_status(job_type):
    try:
        host = st.secrets["databricks"]["host"]
        token = st.secrets["databricks"]["token"]

        job_map = {
            "student": st.secrets["databricks"]["student_job_id"],
            "department": st.secrets["databricks"]["department_job_id"],
            "attendance": st.secrets["databricks"]["attendance_job_id"]
        }

        job_id = int(job_map[job_type])

        url = f"{host}/api/2.1/jobs/runs/list?job_id={job_id}&limit=1"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return " Error"

        data = response.json()

        if not data.get("runs"):
            return " No Runs"

        state = data["runs"][0]["state"]

        life_cycle = state.get("life_cycle_state")
        result = state.get("result_state")

        if life_cycle == "RUNNING":
            return " .... Running....."
        elif result == "SUCCESS":
            return " Success"
        elif result == "FAILED":
            return " Failed"
        else:
            return " Unknown"

    except Exception as e:
        return f" {str(e)}"
    
    