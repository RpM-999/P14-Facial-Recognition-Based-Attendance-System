from .connection import get_db_connection
from datetime import datetime

def mark_attendance(student_id):
    now = datetime.now()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance (student_id, date, time, status) VALUES (%s, %s, %s, %s)",
        (student_id, now.date(), now.time(), "Present")
    )
    conn.commit()
    conn.close()

def get_attendance_report(start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.name, s.roll_number, a.date, a.time, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        WHERE a.date BETWEEN %s AND %s
        ORDER BY a.date DESC
    """, (start_date, end_date))
    data = cursor.fetchall()
    conn.close()
    return data
