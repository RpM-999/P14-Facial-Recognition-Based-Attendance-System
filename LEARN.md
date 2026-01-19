# 🎓 Facial Recognition Based Attendance System

A comprehensive attendance management system that leverages facial recognition technology to automate student attendance tracking. Built with Streamlit, FaceNet-PyTorch, and integrated with Supabase, Qdrant Vector Database, and Google Sheets for efficient data management.

---

## 🎯 Overview

The **Facial Recognition Based Attendance System** is an automated solution designed to streamline attendance management in educational institutions. By utilizing advanced facial recognition technology, the system eliminates manual attendance processes, reduces proxy attendance, and provides real-time attendance tracking with comprehensive reporting capabilities.

### Key Highlights

- ✅ **Real-time Facial Recognition** using FaceNet deep learning model
- ✅ **Multi-user Admin Panel** for system management
- ✅ **Department-wise Student Management**
- ✅ **Automated Email Notifications** for registration and reports
- ✅ **Google Sheets Integration** for attendance logging
- ✅ **Vector Database** for fast and accurate face matching
- ✅ **Comprehensive Reporting** with attendance analytics

---

## ✨ Features

### 👨‍💼 Admin Features

- **Secure Admin Authentication**: Role-based access control with email and password authentication
- **Department Management**: Add, update, and manage departments with HOD information
- **Student Management**: 
  - Add new students with facial data registration
  - Update student information
  - Remove students from the system
  - View student profiles by department
- **Admin Management**: Add and remove admin users
- **Attendance Reports**: Generate and email department-wise attendance reports to HODs

### 📸 Attendance Features

- **Live Facial Recognition**: Capture and match faces in real-time
- **Automatic Attendance Logging**: Records attendance with timestamp to Google Sheets
- **High Accuracy Matching**: Uses FaceNet embeddings with cosine similarity for precise identification
- **Duplicate Prevention**: Prevents multiple check-ins on the same day
- **Attendance List View**: View and filter attendance records

### 📧 Notification System

- **Registration Emails**: Automatic welcome emails to students upon registration
- **Report Emails**: Periodic attendance reports sent to department HODs

---

## 🛠 Technology Stack

### Frontend
- **Streamlit**: Web application framework for the user interface

### Machine Learning
- **FaceNet-PyTorch**: Pre-trained FaceNet model for face embeddings
- **PyTorch**: Deep learning framework
- **MTCNN**: Multi-task Cascaded Convolutional Networks for face detection

### Databases
- **Supabase**: Relational database for structured data (students, departments, admins)
- **Qdrant**: Vector database for storing and querying face embeddings

### Integrations
- **Google Sheets API**: Real-time attendance logging via gspread
- **SMTP Email**: Automated email notifications

### Additional Libraries
- **Pillow (PIL)**: Image processing
- **Pandas**: Data manipulation and analysis
- **pytz**: Timezone handling

---

## 🏗 System Architecture

|**1. Student Registration**| 
|------|
| <img src="IMAGES\01.png" width="1200" height="600" style="object-fit:cover;"> |

|**2. Give Attendance**|
|------|
| <img src="IMAGES\02.png" width="1200" height="600" style="object-fit:cover;"> | 

|**3. Generate Attendance & send to HOD's mail**|
|------|
| <img src="IMAGES\03.png" width="1200" height="600" style="object-fit:cover;"> | 

---
## 🏗 Database Architecture

|**1. Relational Database**|
|------|
| <img src="IMAGES\04.png" width="1200" height="600" style="object-fit:cover;"> |


|**2. Vector Database**|
|------|
| <img src="IMAGES\06.png" width="1200" height="600" style="object-fit:cover;"> |

---


## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Python package installer
- **Git**: Version control system
- **Virtual Environment**: venv or conda

### Required Accounts

1. **Supabase Account**: For MySQL database ([Sign up](https://supabase.com))
2. **Qdrant Cloud** or Local Instance: For vector database ([Documentation](https://qdrant.tech))
3. **Google Cloud Console**: For Google Sheets API ([Console](https://console.cloud.google.com))
4. **SMTP Email Service**: Gmail or other SMTP provider

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/facial-recognition-attendance-system.git
cd facial-recognition-attendance-system
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment

venv\Scripts\activate       # On Windows

source venv/bin/activate    # On macOS/Linux:
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Requirements include:**
- streamlit
- facenet-pytorch
- torch
- supabase
- pillow
- gotrue
- qdrant-client
- gspread
- google-auth
- pytz

---

## ⚙️ Configuration

### 1. Database Configuration

#### Supabase Setup

Create a file `BACKEND/RDB_connection_OP.py` with your Supabase credentials:

```python
import supabase

SUPABASE_URL = "your_supabase_url"
SUPABASE_KEY = "your_supabase_anon_key"

def get_supabase_client():
    return supabase.create_client(SUPABASE_URL, SUPABASE_KEY)
```

#### Qdrant Vector Database Setup

Create a file `BACKEND/VDB_connection_OP.py` with your Qdrant configuration:

```python
from qdrant_client import QdrantClient

QDRANT_URL = "your_qdrant_url"
QDRANT_API_KEY = "your_qdrant_api_key"

def get_qdrant_client():
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
```

### 2. Google Sheets API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select an existing one
3. Enable Google Sheets API
4. Create service account credentials
5. Download the JSON key file
6. Share your Google Sheet with the service account email
7. Place the JSON file in the `FUNC/` directory and reference it in your code

### 3. Email Configuration

Configure SMTP settings in `FUNC/send_email.py`:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use app-specific password for Gmail
```

### 4. Database Tables

Create the following tables in your Supabase database:

**App Controls Table**
```sql
CREATE TABLE app_controls (
    is_registration_open BOOLEAN NOT NULL DEFAULT FALSE
);

```

**Departments Table:**
```sql
CREATE TABLE department (
    dep_id TEXT PRIMARY KEY,
    dep_name TEXT NOT NULL,
    dep_hod TEXT NOT NULL,
    dep_hod_mail TEXT NOT NULL
);
```

**Students Table:**
```sql
CREATE TABLE students (
    s_id TEXT PRIMARY KEY,
    s_name TEXT NOT NULL,
    s_mail TEXT UNIQUE NOT NULL,
    s_phone TEXT NOT NULL,
    s_address TEXT,
    dep_id TEXT NOT NULL,
    s_admissionyear INT NOT NULL,
    s_dob DATE NOT NULL,

    CONSTRAINT fk_department
        FOREIGN KEY (dep_id)
        REFERENCES department(dep_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
```



---

## 📁 Project Structure

```
P14-Facial-Recognition-Based-Attendance-System-main/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── project details.md              # Additional project information
│
├── BACKEND/                        # Backend operations and database connections
│   ├── admin_OP.py                 # Admin authentication and operations
│   ├── attendance_OP.py            # Attendance logging and identification
│   ├── department_OP.py            # Department CRUD operations
│   ├── RDB_connection_OP.py        # Relational database (Supabase) connection
│   ├── report_OP.py                # Report generation and email dispatch
│   ├── student_OP.py               # Student CRUD operations
│   └── VDB_connection_OP.py        # Vector database (Qdrant) connection
│
├── FUNC/                           # Functional modules and utilities
│   ├── attendance_gspread.py       # Google Sheets attendance operations
│   ├── face_embedding_OP.py        # Face detection and embedding generation
│   ├── g_spread.py                 # General Google Sheets operations
│   ├── navigation.py               # Page navigation helper
│   └── send_email.py               # Email notification service
│
├── UI/                             # Streamlit UI pages
│   ├── Home.py                     # Landing page
│   ├── Admin_login.py              # Admin authentication page
│   ├── Admin_option.py             # Admin dashboard
│   ├── Add_new_department.py       # Department creation page
│   ├── Update_department_info.py   # Department update page
│   ├── Add_new_student.py          # Student registration page
│   ├── Update_student_info.py      # Student update page
│   ├── Remove_student.py           # Student removal page
│   ├── Give_attendance.py          # Live attendance capture page
│   ├── Attendance_list.py          # Attendance records viewer
│   ├── Add_admin.py                # Admin creation page
│   └── Remove_admin.py             # Admin removal page
│
├── LICENSE
└── IMAGES/                         # Static images and assets
```

---

## 🎮 Usage

### Starting the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Admin Workflow

1. **Login**: Navigate to Admin Login and enter credentials
2. **Manage Departments**:
   - Add new departments with HOD details
   - Update existing department information
3. **Manage Students**:
   - Register new students with facial data 
   - Update student information
   - Remove students when needed
4. **View Attendance**: Check attendance records by date and department
5. **Generate Reports**: Create and email attendance reports to HODs

### Student Attendance Workflow

1. Navigate to **Give Attendance** page
2. Allow camera access
3. Capture live image
4. System automatically identifies and logs attendance
5. Confirmation message displayed upon successful check-in

---

## 🔑 Key Modules

### Face Embedding Module (`FUNC/face_embedding_OP.py`)

- Uses **MTCNN** for face detection
- Generates **512-dimensional embeddings** using FaceNet
- Handles image preprocessing and normalization

### Student Operations (`BACKEND/student_OP.py`)

- **process_and_upload_students()**: Batch student registration with face embeddings
- **get_student_by_id()**: Retrieve student information
- **update_student_info()**: Update student details
- **find_student_by_embedding()**: Facial recognition matching using Qdrant
- **delete_student()**: Remove student and associated embeddings

### Attendance Operations (`BACKEND/attendance_OP.py`)

- **identify_student_from_image()**: Real-time face recognition
- **log_attendance_to_sheet()**: Record attendance in Google Sheets
- Uses **cosine similarity** with threshold for accurate matching

### Report Generation (`BACKEND/report_OP.py`)

- **generate_and_send_reports()**: Create attendance reports with statistics
- Calculates attendance percentage
- Sends HTML-formatted emails to department HODs

---

## 💾 Database Schema

### Students Collection (RDB - supabase )
- Student ID (Primary Key)
- Name
- Email
- Phone no.
- Address
- Department ID (Foreign Key)
- Admision year
- date od birth

### Departments (RDB - supabase )
- Department ID (Primary Key)
- Department Name
- HOD Name
- HOD Email

### Student Registratio App Control (RDB- supabase )
- is registration open (Primary Key)
  
|**1. Relational Database**|
|------|
| <img src="IMAGES\05.png" width="1200" height="600" style="object-fit:cover;"> |


### Face Embeddings (VDB - Qdrant)
- Vector ID
- Student ID (payload)
- 512-dimensional face embedding vector
- Metadata (name, department)

|**2. Vector Database**|
|------|
| <img src="IMAGES\07.png" width="1200" height="600" style="object-fit:cover;"> |


### Attendance Log (Google Sheets)
- Date
- Student ID
- Department ID

|**3. Attendance Log**|
|------|
| <img src="IMAGES\21.png" width="1200" height="600" style="object-fit:cover;"> |

---

## 🔗 API Integration

### Supabase REST API
- Student and department CRUD operations
- Admin authentication

### Qdrant Vector Search API
- Face embedding storage
- Cosine Similarity search for face matching

### Google Sheets API
- Real-time attendance logging
- Data retrieval for reports

---

## 🔒 Security

- **Password Hashing**: Admin passwords should be hashed (implement bcrypt)
- **Environment Variables**: Store sensitive credentials in `.env` file (not in source code)
- **Session Management**: Streamlit session state for authentication
- **API Keys**: Secure API keys for external services
- **Input Validation**: Sanitize all user inputs
- **HTTPS**: Use HTTPS in production for data transmission

### Recommended .env Structure

```
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Qdrant
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Google Sheets
GOOGLE_SHEETS_CREDS=path/to/credentials.json
```

---

## 🐛 Troubleshooting

### Common Issues

**1. Camera Access Denied**
- Check browser permissions for camera access
- Ensure HTTPS is used in production

**2. Face Not Detected**
- Ensure proper lighting conditions
- Face should be clearly visible and frontal
- Check if MTCNN model is loaded correctly

**3. Database Connection Error**
- Verify database credentials in configuration files
- Check internet connection
- Ensure database services are running

**4. Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

**5. Email Not Sending**
- Verify SMTP credentials
- Enable "Less secure app access" or use app-specific password for Gmail
- Check firewall settings


---
## 🖼️ Screenshots



### **Fig-1 : Home Page**
|**Landing Page Admin Choose Admin Login and Student Choose Give Attendence Section**|
|------|
| <img src="IMAGES\08.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-2 : Admin Login**
|**Admin login interface for authorized access to administrative privileges.**|
|------|
| <img src="IMAGES\09.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-3 : Admin Panel**
|**Admin panel dashboard providing centralized access to system management features.**|
|------|
| <img src="IMAGES\10.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-4 : Student Registration Control**
|<span style="color: green;"><b>Open Form:</b></span> Enables student registration and stores data in Google Sheets.<br><span style="color: red;"><b>Close Form:</b></span> Disables student registration to prevent new submissions.|
|------|
| <img src="IMAGES\11.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-5 : Student data upload to database**
|**Student information from Google Sheet upload to RDB( Supabase ) and student Face Embedding upload to VDB( Quadrant )**|
|------|
| <img src="IMAGES\12.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-6 : Student registration confirmation**
|**Confirmation email received after successful student registration, including system-generated Student ID (email ID hidden for security purposes)**|
|------|
| <img src="IMAGES\13.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-7 : Update student information and face embedding**
|**Students can update personal information and regenerate face embeddings by uploading three clear images in cases where initial registration images were unclear or face recognition fails**|
|------|
| <img src="IMAGES\14.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-8 : Remove student from system**
|**Admin confirmation interface for permanently deleting a student’s records when the student leaves the institution, including removal of data from RDB (Supabase) and facial embeddings from VDB (Qdrant)**|
|------|
| <img src="IMAGES\15.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-9 : Add a new department**
|**Admin interface for adding a new department by entering department ID, department name, Head of Department (HOD) details, and official email information**|
|------|
| <img src="IMAGES\16.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-10 : Update department information**
|**Admin interface for modifying existing department details, including department name,  Head of Department (HOD) information, and official email address**|
|------|
| <img src="IMAGES\22.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-11 : Attendance list and reporting**
|**Interface for generating attendance reports within a selected date range, calculating effective working days, and automatically sending department-wise reports to the respective HODs via email**|
|------|
| <img src="IMAGES\17.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-12 : Attendance report email notification**
|**Automatically generated attendance report emailed to the respective Head of Department (HOD), including reporting period, total working days, student-wise attendance details, and attendance percentage**|
|------|
| <img src="IMAGES\18.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-13 : Face-Recognition based attendance marking**
|**Student attendance interface using real-time face capture, where attendance can be marked only within a predefined time window configured by college administrators**|
|------|
| <img src="IMAGES\19.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-14 : Attendance confirmation before write in attendance-log**
|**Confirmation interface displayed after successful face recognition, allowing the student to verify their identity before final attendance is logged into the system**|
|------|
| <img src="IMAGES\20.png" width="1200" height="600" style="object-fit:cover;"> |

### **Fig-15 : Attendance data storage**
|**Student attendance records stored in Google Sheets, including date-wise entries with student ID and department ID for further reporting and analysis
|------|
| <img src="IMAGES\21.png" width="1200" height="600" style="object-fit:cover;"> |

---

## 📊 Project Status

🚧 **Active Development** - This project is actively maintained and open for contributions.

### Roadmap

- [ ] Multi-language support
- [✅] Mobile application
- [ ] Advanced analytics dashboard
- [ ] Biometric integration
- [ ] Cloud deployment guide
- [ ] Docker containerization
- [ ] API documentation
- [ ] Unit test coverage

---

## 🙏 Acknowledgments

- **FaceNet**: For the pre-trained facial recognition model
- **Streamlit**: For the amazing web framework
- **Qdrant**: For the efficient vector database
- **Supabase**: For the database infrastructure
- **Google**: For Sheets API integration

---


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


## 📧 Contact

**Project Maintainer**: [Rupam Mondal]

- 📧 Email: [Mail](rupam.mondal2022@uem.edu.in)
- 🐙 GitHub: [Link](https://github.com/RpM-999)
- 💼 LinkedIn: [Link](https://linkedin.com/in/rupam-mondal-data-science )

**Project Link**: [https://github.com/yourusername/facial-recognition-attendance-system](https://github.com/yourusername/facial-recognition-attendance-system)

---

**⭐ If you find this project helpful, please consider giving it a star ⭐**

---

*Last Updated: December 2025*

