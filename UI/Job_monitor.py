import streamlit as st
import time
from FUNC.navigation import go_to
from BACKEND.databricks_connection_OP import trigger_databricks_job, get_job_status


def job_monitor_page():

    job_type = st.session_state.get("job_type")

    if not job_type:
        st.error("No job selected")
        return

    st.caption("IMPORTANT: Do not refresh page while job is running")

    # ---------------- SESSION STATE INIT ----------------

    if "job_started" not in st.session_state:
        st.session_state.job_started = False

    if "job_status" not in st.session_state:
        st.session_state.job_status = "Not Started"

    if "progress" not in st.session_state:
        st.session_state.progress = 0

    st.title(f"Running {job_type.upper()} Pipeline")

    # ---------------- TRIGGER JOB ----------------

    if not st.session_state.job_started:

        st.info("Triggering Databricks job...")

        success, msg = trigger_databricks_job(job_type)

        if not success:
            st.error(msg)
            return

        st.session_state.job_started = True
        st.session_state.job_status = "Running"
        st.success("Job triggered successfully!")

    # ---------------- STATUS CHECK ----------------

    status = get_job_status(job_type)
    st.session_state.job_status = status

    # ---------------- PROGRESS BAR ----------------

    if "Success" in status:
        st.session_state.progress = 100

    elif "Failed" in status:
        st.session_state.progress = 100

    else:
        st.session_state.progress = min(st.session_state.progress + 10, 90)

    st.progress(st.session_state.progress)
    st.info(f"Current Status: {status}")

    # ---------------- AUTO REFRESH ----------------

    if "Success" not in status and "Failed" not in status:
        time.sleep(3)
        st.rerun()

    # ---------------- FINAL STATUS ----------------

    st.divider()

    if "Success" in status:
        st.success(f"{job_type.upper()} pipeline completed successfully!")

    elif "Failed" in status:
        st.error(f"{job_type.upper()} pipeline failed!")

    # ---------------- BACK BUTTON ----------------

    st.divider()

    if st.button("⬅️ Back to Admin Panel", use_container_width=True):

        # Reset state
        st.session_state.job_started = False
        st.session_state.progress = 0
        st.session_state.job_status = "Not Started"

        go_to("Admin_option")