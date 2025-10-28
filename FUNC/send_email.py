
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#------------------------------------- SEND CONFIRMATION MAIL---------------------------------------


def send_registration_email(student_details: dict):
    try:
        sender_email = st.secrets["email_credentials"]["sender_email"]
        app_password = st.secrets["email_credentials"]["app_password"]
        

        recipient_email = student_details.get("S_mail")
        if not recipient_email:
            st.warning(f"Skipping email for {student_details.get('S_name', 'Unknown')}: Missing email address.")
            return False, "Missing recipient email"

# ---------------------------------- Email Content -----------------------------------------------


        student_name = student_details.get("S_name", "Student")
        student_id = student_details.get("S_id", "Not Assigned")
        
        subject = "Registration Confirmation - Student Attendance System"
        
        # Create a more detailed HTML body
        body_html = f"""
        <html>
        <body>
            <h2>Welcome, {student_name}!</h2>
            <p>Your registration for the Student Attendance System is complete.</p>
            <p>Your unique Student ID is: <strong>{student_id}</strong></p>
            <p>Please keep this ID safe. You may need it for future reference.</p>
            <hr>
            <h4>Your Registered Details:</h4>
            <ul>
                <li><strong>Name:</strong> {student_details.get('S_name', 'N/A')}</li>
                <li><strong>Email:</strong> {student_details.get('S_mail', 'N/A')}</li>
                <li><strong>Phone:</strong> {student_details.get('S_phone', 'N/A')}</li>
                <li><strong>DOB:</strong> {student_details.get('S_dob', 'N/A')}</li>
                <li><strong>Address:</strong> {student_details.get('S_Address', 'N/A')}</li>
                <li><strong>Department ID:</strong> {student_details.get('dep_id', 'N/A')}</li>
                <li><strong>Admission Year:</strong> {student_details.get('S_admisionYear', 'N/A')}</li>
            </ul>
            <p>Thank you!</p>
        </body>
        </html>
        """

# ---------------------------------------- Construct Email -------------------------------------



        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        # Attach HTML part
        part_html = MIMEText(body_html, "html")
        message.attach(part_html)

# ------------------------------------------- Send Email using Gmail SMTP ----------------------------


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
            
        return True, f"Email sent successfully to {recipient_email}"

    except Exception as e:
        st.error(f"Failed to send email to {recipient_email}: {e}")
        return False, f"Failed to send email: {e}"
    
    
    
#------------------------------------------------------------------------------------------------------



def send_report_email(recipient_email: str, subject: str, body_html: str):
    try:

        sender_email = st.secrets["email_credentials"]["sender_email"]
        app_password = st.secrets["email_credentials"]["app_password"]

        if not recipient_email:
            return False, "Missing recipient email address for report."

        # --- Construct Email ---
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Attendance System <{sender_email}>" 
        message["To"] = recipient_email

        part_html = MIMEText(body_html, "html")
        message.attach(part_html)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        return True, "Report email sent successfully."

    except smtplib.SMTPAuthenticationError:
        print(f"!!! SMTP Auth Error sending report to {recipient_email}. Check sender email/app password.")
        return False, "Email server authentication failed. Check credentials."
    
    except Exception as e:
        print(f"!!! Failed to send report email to {recipient_email}: {e}")
        # Return a user-friendly message
        return False, f"Failed to send email due to system error: {e}"
    
    
    
# ---------------------------------------------------