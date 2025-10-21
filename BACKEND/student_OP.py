from .connection_OP import get_db_connection
import mysql.connector
import datetime

'''
            ------------> select all the student info

'''

def get_all_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return students



'''
            ------------> add a new student

'''

'''
            -------------> 120A-2025-0001
'''

def generate_roll_number(conn, join_year, university_code="120A"):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students WHERE join_year = %s", (join_year,))
    count = cursor.fetchone()[0] + 1  

    roll_number = f"{university_code}-{join_year}-{count:04d}"
    return roll_number

def get_departments(department_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT d_id FROM departments WHERE d_name = %s", (department_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        None


def insert_student(name, email, department, year, face_encoding, photo_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:

        join_year = datetime.now().year
        roll_number = generate_roll_number(conn, join_year)



        cursor.execute(
            """
            INSERT INTO students 
            (roll_number, student_name, email, department, year, join_year, face_encoding, photo_path) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (roll_number, name, email, department, year, join_year, face_encoding, photo_path)
        )
        conn.commit()
        return roll_number  ,join_year
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        raise
    finally:
        conn.close()
'''
def insert_student(name, roll, email, class_name, face_encoding, photo_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, roll_number, email, `class`, face_encoding, photo_path) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, roll, email, class_name, face_encoding, photo_path)
        )
        conn.commit()
    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        raise
    finally:
        conn.close()

'''

'''
            ------------> remove student

'''