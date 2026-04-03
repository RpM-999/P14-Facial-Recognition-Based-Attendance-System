import streamlit as st
from BACKEND.report_OP import get_attendance_from_gold, generate_and_send_reports
from BACKEND.department_OP import get_departments_with_hod
from FUNC.navigation import go_to
import datetime
import pandas as pd


def attendance_list():


    # ---------------- AUTH CHECK ----------------


    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return




    st.title(" Attendance List & Reporting")


    # ---------------- DATE SELECTION ----------------



    st.header("Select Reporting Period")

    today = datetime.date.today()
    start_of_month = today.replace(day=1)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            " Start Date",
            value=start_of_month,
            max_value=today,
            key="att_start_date"
        )
    with col2:
        end_date = st.date_input(
            " End Date",
            value=today,
            min_value=start_date,
            max_value=today,
            key="att_end_date"
        )

    # ---------------- WORKING DAYS ----------------



    total_working_days = 0

    try:
        date_range = pd.date_range(start_date, end_date)

        working_days_df = date_range[date_range.dayofweek < 5]
        potential_working_days = len(working_days_df)

        if potential_working_days > 0:
            num_holidays = st.slider(
                "Number of Additional Holidays",
                min_value=0,
                max_value=potential_working_days,
                value=0
            )

            total_working_days = potential_working_days - num_holidays
            total_working_days = max(total_working_days, 0)

        else:
            st.info("No weekdays in selected range.")
            total_working_days = 0

        st.info(
            f" {start_date} → {end_date} | "
            f"Working Days: **{total_working_days}**"
        )

    except Exception as e:
        st.error(f"Error calculating working days: {e}")
        return

    st.markdown("---")



    # ---------------- DEPARTMENT SELECTION ----------------



    st.header("Send Attendance Report to HODs")

    departments = get_departments_with_hod()

    if not departments:
        st.warning("No departments found.")
        return

    selected_departments_info = []

    for dept in departments:
        if st.checkbox(
            f"{dept['dep_name']} (HOD: {dept['dep_hod_mail']})",
            key=f"dept_{dept['dep_id']}"
        ):
            selected_departments_info.append(dept)



    # ---------------- BUTTON ----------------



    if st.button(" Generate & Send Reports", type="primary"):

        if not selected_departments_info:
            st.warning("Select at least one department.")
            return

        if total_working_days <= 0:
            st.warning("Working days must be > 0")
            return



        # ---------------- MAIN LOGIC ----------------



        with st.spinner("Fetching data from Data Warehouse..."):

            try:
                
                df_attendance = get_attendance_from_gold(
                    start_date=start_date,
                    end_date=end_date,
                    total_working_days=total_working_days
                )

                if df_attendance.empty:
                    st.warning("No attendance data found.")
                    return



                # ---------------- FILTER DEPARTMENTS ----------------




                selected_ids = [str(d["dep_id"]) for d in selected_departments_info]

                df_filtered = df_attendance[
                    df_attendance["department_id"].astype(str).isin(selected_ids)
                ].copy()

                if df_filtered.empty:
                    st.warning("No data for selected departments.")
                    return

                # ---------------- GENERATE REPORT ----------------




                success_count, fail_count = generate_and_send_reports(
                    attendance_df=df_filtered,
                    selected_departments_info=selected_departments_info,
                    total_working_days=total_working_days,
                    start_date=start_date,
                    end_date=end_date
                )

                if success_count > 0:
                    st.success(f" Reports sent for {success_count} departments")

                if fail_count > 0:
                    st.warning(f" Failed for {fail_count} departments")

            except Exception as e:
                st.error(f"Error: {e}")



    # ---------------- BACK BUTTON ----------------



    st.markdown("---")

    if st.button("⬅️ Back to Admin Panel"):
        go_to("Admin_option")
        st.rerun()