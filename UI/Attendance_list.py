import streamlit as st
from BACKEND.RDB_connection_OP import supabase 
from FUNC.navigation import go_to
from FUNC.attendance_gspread import connect_to_gsheet, read_attendance_sheet
from BACKEND.department_OP import get_departments_with_hod
from BACKEND.report_OP import generate_and_send_reports
import datetime
import pandas as pd 

# ----------------------------------- CONNECT TO THE ATTENDANCE SHEET---------------------------------



attendance_sheet = connect_to_gsheet()


def attendance_list(): 

    
    # ------------------------------- Authentication check -------------------------------------------
    
    
    if not st.session_state.get("logged_in"):
        st.warning("You must be logged in to view this page.")
        if st.button("Go to Login"):
            go_to("Admin_login")
            st.rerun()
        return


#----------------------------------------------------------------------------------------------------



    st.title("📊 Attendance List & Reporting")
    
    

    # ---------------------------- SELECT FIRST AND THE LAST DATE  ---------------------------------
    
    
    st.header("Select Reporting Period")

    today = datetime.date.today()
    start_of_month = today.replace(day=1)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅Start Date (inclusive)", value=start_of_month, max_value=today, key="att_start_date")
    with col2:
        end_date = st.date_input("📅End Date (inclusive)", value=today, min_value=start_date, max_value=today, key="att_end_date")
        

    # --------------------------------- NUMBER OF WORKING DAYS ------------------------------------
    
    
    
    total_working_days = 0 
    potential_working_days = 0
    num_holidays = 0
    try:

        date_range = pd.date_range(start_date, end_date)

        working_days_df = date_range[date_range.dayofweek < 5]
        potential_working_days = len(working_days_df)


#-------------------------- NO OF HOLIDAYS EXCEPT FROM SATARDAY AND SUNDAY--------------------------


        if potential_working_days > 0:
            num_holidays = st.slider(
                "Number of Additional Holidays (excluding weekends)",
                min_value=0,
                max_value=potential_working_days,
                value=0,
                key="att_holidays_slider",
                help=f"Select official holidays within {start_date} and {end_date}. Weekends are already excluded."
            )
            
            
            total_working_days = potential_working_days - num_holidays
            if total_working_days < 0: 
                total_working_days = 0 
        else:
             num_holidays = 0 # No potential working days, so 0 holidays
             total_working_days = 0
             st.info("Selected date range contains no weekdays.")

        # Display calculation result
        st.info(f"Selected Period: {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}\n"
                f"Calculated Working Days: **{total_working_days}** ({potential_working_days} weekdays - {num_holidays} holidays)")

    except Exception as e:
        st.error(f"Error calculating working days: {e}")
        total_working_days = -1 # Indicate an error occurred

    st.markdown("---")




    # ------------------------------ SEND THE LIST TO HODs --------------------------------------
    
    
    
    
    
    st.header("Send Attendance Report to HODs")

    departments = get_departments_with_hod()
    
    if not departments:
        st.warning("No departments found in the database. Cannot send reports.")
    else:
        st.write("Select departments to include in the report:")

        selected_departments_info = [] 
        
        
        for dept in departments:
            
            is_selected = st.checkbox(
                f"{dept.get('dep_name', 'N/A')} (HOD: {dept.get('dep_hod_mail', 'N/A')})",
                key=f"dept_select_{dept.get('dep_id')}" 
            )
            if is_selected:
                selected_departments_info.append(dept)

        send_button_disabled = total_working_days < 0 or not departments

        if st.button("✉️ Generate & Send Reports", type="primary", disabled=send_button_disabled, key="send_report_btn"):
            
            
            if not selected_departments_info:
                st.warning("Please select at least one department.")
            elif attendance_sheet is None:
                 st.error("Cannot connect to the attendance log sheet.")
            else:
                
                
                
# ----------------------------------------- Trigger Backend Logic --------------------------------------------------
                
                
                with st.spinner("Fetching attendance data and processing reports..."):
                    try:
                        all_attendance_records = read_attendance_sheet(attendance_sheet)
                        if not all_attendance_records:
                             st.warning("No attendance records found in the temporary log.")
                             st.stop() 

                        df_attendance = pd.DataFrame(all_attendance_records)
                        
                        if 'Date' not in df_attendance.columns:
                             st.error("Attendance log sheet is missing the 'Date' column.")
                             st.stop()
                        df_attendance['Date'] = pd.to_datetime(df_attendance['Date'], errors='coerce').dt.date
                        df_attendance.dropna(subset=['Date'], inplace=True) 



#------------------------------------ONLY RETRIVE THOSE DEPARTMENT THOSE ARE SELECTED-------------------------------
                        
                        
                        
                        df_filtered = df_attendance[
                            (df_attendance['Date'] >= start_date) &
                            (df_attendance['Date'] <= end_date)
                        ].copy()

                        if df_filtered.empty:
                            st.warning(f"No attendance records found between {start_date} and {end_date}.")
                            st.stop() 
                            
                            
                            
                      
# --------------------- CALL THE FUNCTION THAT CALCULATE THE PERCENTAGE OF ATTENDENCE AND SEND MAIL --------------------


                      
                        success_count, fail_count = generate_and_send_reports(
                            attendance_df=df_filtered,
                            selected_departments_info=selected_departments_info,
                            total_working_days=total_working_days,
                            start_date=start_date,
                            end_date=end_date
                        )
                        
                        
# --------------------------------------------------------------------------------------------------------------------



                        if success_count > 0:
                            st.success(f"Successfully generated and attempted sending reports for {success_count} departments.")
                        if fail_count > 0:
                             st.warning(f"Failed to process or send reports for {fail_count} departments. Check logs or HOD emails.")

                    except Exception as e:
                        st.error(f"An error occurred during report processing: {e}")



    # --------------------------------------------- Back Button ---------------------------------------
    
    
    st.markdown("---")
    if st.button("⬅️ Back to Admin Menu", key="back_admin_btn"):
        go_to("Admin_option")
        st.rerun()