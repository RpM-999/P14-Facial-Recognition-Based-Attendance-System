# 🎓 Facial Recognition Based Attendance System 🎓

A comprehensive, enterprise-grade attendance management system that leverages facial recognition technology to automate student attendance tracking. Built with **Streamlit**, **FaceNet-PyTorch**, and integrated with **Supabase**, **Qdrant** Vector Database, **Databricks** Data Warehouse, and **Google Sheets** for efficient data management and analytics.

---

## 🎯 Overview

The **Facial Recognition Based Attendance System** is an automated solution designed to streamline attendance management in educational institutions. By utilizing advanced facial recognition technology powered by deep learning models, the system eliminates manual attendance processes, reduces proxy attendance, and provides real-time attendance tracking with comprehensive reporting capabilities and data warehousing.

### Key Highlights

- ✅ **Real-time Facial Recognition** using FaceNet deep learning model with MTCNN face detection
- ✅ **Multi-user Admin Panel** with role-based access control for system management
- ✅ **Department-wise Student Management** with hierarchical organization
- ✅ **Automated Email Notifications** for registration and attendance reports
- ✅ **Google Sheets Integration** for live attendance logging and data export
- ✅ **Vector Database (Qdrant)** for fast and accurate face matching using cosine similarity
- ✅ **Databricks Data Warehouse** for advanced analytics and historical reporting
- ✅ **Secure Authentication** using Supabase Auth with email and password
- ✅ **Attendance Analytics** with department-wise reports and attendance percentage tracking

---

## ✨ Features


|**Admin Access Control**|

 <p align="center">
  <img src="IMAGES/00 DIAGRAM/03 ADMIN ACESS CONTROL.png" width="900">
</p> 

### **👨‍💼 Admin Features**

- **Secure Admin Authentication**: Email and password authentication via Supabase Auth with session management
- **Department Management**: 
  - Create new departments with HOD (Head of Department) details
  - Update department information including HOD contact details
  - Manage departmental structure and hierarchy
- **Student Management**: 
  - Add new students with facial data registration (face embeddings generated and stored)
  - Batch upload students via Google Sheets
  - Update student information and regenerate face embeddings
  - Remove students and clean up associated embeddings from vector database
  - View student profiles by department with detailed information
- **Admin Management**: Add and manage admin users with secure authentication
- **Registration Control**: Open/close student registration form to control enrollment periods
- **Attendance Reports**: 
  - Generate department-wise attendance reports with analytics
  - Calculate attendance percentages and present day statistics
  - Email comprehensive reports to HODs with formatted HTML
- **Job Monitoring**: Monitor and trigger Databricks pipeline jobs for data processing

### **📸 Attendance Features**

- **Live Facial Recognition**: Real-time face capture and identification using webcam
- **High-Speed Face Matching**: Cosine similarity search in Qdrant vector database (millisecond response)
- **Automatic Attendance Logging**: Records attendance with precise timestamp to Google Sheets
- **High Accuracy Identification**: 
  - Uses FaceNet 512-dimensional embeddings for robust face matching
  - Confidence threshold-based matching to reduce false positives
  - Multiple face embeddings per student for better accuracy
- **Duplicate Prevention**: Prevents multiple check-ins on the same day per student
- **Attendance List View**: Browse and filter attendance records by date and department
- **Instant Confirmation**: Shows student identity confirmation before finalizing attendance

### **📧 Notification System**

- **Registration Emails**: Automatic welcome emails with generated Student ID upon successful registration
- **Report Emails**: Periodic attendance reports sent to department HODs with detailed breakdown
- **System Notifications**: Real-time feedback messages for all user actions

### **📊 Data Management**

- **Relational Database (Supabase)**: Structured storage for students, departments, admins, and metadata
- **Vector Database (Qdrant)**: Distributed storage of face embeddings with semantic search capability
- **Data Warehouse (Databricks)**: Multi-layer architecture (Bronze/Silver/Gold) for analytics-ready data

---

## **🛠 Technology Stack**

### Platform Used in this Project
<p align="center">
  <img src="IMAGES/00 DIAGRAM/00 PLATFORM USED IN THIS PROJECT.png" width="900">
</p>


### **Frontend & Web Framework**
- **Streamlit**: Rapid web application development framework for data applications
- **Streamlit Session State**: Client-side state management for workflows
- **PIL (Pillow)**: Image processing and manipulation

### **Machine Learning & Computer Vision**
- **FaceNet-PyTorch**: Pre-trained FaceNet model for generating 512-dimensional face embeddings
- **PyTorch**: Deep learning framework for model inference
- **MTCNN**: Multi-task Cascaded Convolutional Networks for robust face detection
- **GPU Support**: CUDA acceleration for faster inference (CPU fallback available)

### **Databases & Data Storage**
- **Supabase**: 
  - PostgreSQL relational database for structured data (students, departments, admins)
  - Built-in authentication system (GoTrue) for secure admin login
  - Real-time data synchronization
- **Qdrant**: 
  - Vector database for storing and querying 512-dimensional face embeddings
  - Cosine similarity search for fast face matching
  - Payload-based filtering for student-specific queries
- **Databricks**: 
  - Unity Catalog for data governance
  - Multi-layer data warehouse (Bronze → Silver → Gold layers)
  - SQL analytics for attendance reporting
  - Job orchestration for automated data pipelines

### **Integrations & APIs**
- **Google Sheets API (gspread)**: Real-time attendance logging and data retrieval
- **SMTP Email**: Automated email notifications (supports Gmail with app-specific passwords)
- **Databricks SQL Connector**: Direct SQL queries to data warehouse
- **HTTPx**: HTTP client for API calls with HTTP/2 support

### **Additional Libraries**
- **Pandas**: Data manipulation, aggregation, and analysis
- **PyTZ**: Timezone handling for timestamp accuracy
- **UUID**: Unique identifier generation for vector points
- **Requests**: HTTP library for Databricks job triggering

---

## **🏗 System Architecture**
### **Data Flow Architecture**

**1. Student Registration Flow**

<p align="center">
  <img src="IMAGES/00 DIAGRAM/01 STUDENT REGISTRATION PROCESS.png" width="900">
</p>

#### **1. Student Registration Pipeline**

```
Student Registration Form
        ↓
   Google Sheets
        ↓
   Admin Approval
        ↓
✓ Extract Student Data → Face Embedding Generation (MTCNN + FaceNet)
✓ Store in Supabase (RDB) → Relational student data
✓ Store in Qdrant (VDB) → Face embeddings with student metadata
✓ Send Registration Email → Confirmation with Student ID
```
**2. Attendance Marking High Level Overview :** 

<p align="center">
  <img src="IMAGES/00 DIAGRAM/02 GIVING ATTENDANCE PROCESS.png" width="900">
</p>


#### **2. Attendance Marking Pipeline**

```
Student Attendance Page
        ↓
   Live Camera Capture
        ↓
   Face Detection (MTCNN)
        ↓
   Generate Face Embedding (FaceNet)
        ↓
   Search in Qdrant (Vector Similarity)
        ↓
   Identify Student → Confidence Check
        ↓
   Confirm Identity
        ↓
✓ Log to Google Sheets (Real-time) → Atomic timestamp record
```



#### **3. Report Generation & Distribution Pipeline**

```
Admin Triggers Report Generation
        ↓
   Query Google Sheets → All attendance records in date range
        ↓
   Load Databricks (Gold Layer) → Aggregated attendance data
        ↓
   Calculate Statistics:
   - Attendance percentage per student
   - Present days count
   - Department-wide metrics
        ↓
   Generate HTML Report → Professional formatting
        ↓
   Send via SMTP → Department HODs
```

**Report Generation Flow**

<p align="center">
  <img src="IMAGES/00 DIAGRAM/02 GIVING ATTENDANCE PROCESS.png" width="900">
</p>

### Database Architecture

#### **1. Relational Database (Supabase PostgreSQL)**

Core business data with structured schema and relationships:

```
┌─────────────────────────────────────────────┐
│         RELATIONAL DATABASE (RDB)           │
│          Supabase / PostgreSQL              │
└─────────────────────────────────────────────┘
         │
         ├─ DEPARTMENTS TABLE
         │  ├─ dep_id (PK)
         │  ├─ dep_name
         │  ├─ dep_hod
         │  └─ dep_hod_mail
         │
         ├─ STUDENTS TABLE
         │  ├─ s_id (PK)
         │  ├─ s_name
         │  ├─ s_mail (UNIQUE)
         │  ├─ s_phone
         │  ├─ s_address
         │  ├─ dep_id (FK → DEPARTMENTS)
         │  ├─ s_admissionyear
         │  └─ s_dob
         │
         ├─ ADMINS TABLE
         │  ├─ admin_id (PK)
         │  ├─ email (UNIQUE)
         │  ├─ password_hash
         │  ├─ department_assignment
         │  └─ created_at
         │
         └─ APP_CONTROLS TABLE
            └─ is_registration_open (Boolean)
```

**Relational Database Schema**

 <p align="center">
  <img src="IMAGES/00 DIAGRAM/16 RDB.png" width="900">
</p>
 <p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/05.png" width="900">
</p>

#### **2. Vector Database (Qdrant)**

High-performance similarity search for face recognition:

```
┌─────────────────────────────────────────────┐
│      VECTOR DATABASE (VDB) - Qdrant         │
│    Collection: "student_face_encodings"     │
└─────────────────────────────────────────────┘
         │
         └─ POINTS (Vector Records)
            ├─ Vector ID (UUID)
            ├─ Vector (512-dim embedding)
            │  └─ Generated by FaceNet-PyTorch
            │
            └─ PAYLOAD (Metadata)
               ├─ s_id (Student ID)
               ├─ s_name
               ├─ dep_id
               ├─ timestamp
               └─ quality_score
            
         Operations:
         ├─ Upsert: Store new/updated embeddings
         ├─ Search: Find nearest embeddings (cosine similarity)
         ├─ Filter: Query by student ID
         └─ Delete: Remove during student deletion
```

**Vector Database Schema**

 <p align="center">
  <img src="IMAGES/00 DIAGRAM/17 VDB.png" width="900">
</p>
 <p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/07.png" width="900">
</p>

#### **3. Data Warehouse (Databricks)**

**Multi-layer analytics platform with medallion architecture:**

 <p align="center">
  <img src="IMAGES/00 DIAGRAM/07 MEDILIAN ARCHITECTURE.png" width="900">
</p>

<p align="center">
  <img src="IMAGES/02 DATABRICKS IMAGES/01 CATALOG.png" width="900">
</p>

```
┌─────────────────────────────────────────────┐
│        DATA WAREHOUSE - Databricks          │
│       Medallion Architecture (Processed)    │
└─────────────────────────────────────────────┘

BRONZE LAYER (Raw Data)
   ├─ attendance_raw
   ├─ students_raw
   └─ departments_raw
          ↓
SILVER LAYER (Cleaned & Deduplicated)
   ├─ attendance_clean
   │  └─ Removed duplicates, normalized dates
   ├─ students_clean
   |  └─ rename columns , add columns
   ├─ department_clean
      └─ rename columns , add columns
          ↓
GOLD LAYER (Analytics Ready)
   ├─ FACT_ATTENDANCE
   │  ├─ attendance_date    ← (Partition Column)
   │  ├─ student_id
   │  ├─ department_id
   │  └─ timestamp
   │
   ├─ DIM_STUDENTS
   │  ├─ student_key
   │  ├─ student_id
   │  ├─ student_name
   │  ├─ student_email
   │  ├─ student_phone
   │  ├─ student_address
   │  ├─ department_id
   │  ├─ admission_year
   │  ├─ date_of_birth
   │  ├─ start_date
   │  ├─ end_date
   │  └─ is_current
   |
   ├─ DIM_DEPARTMENTS
   │  ├─ department_key
   │  ├─ department_id
   │  ├─ department_name
   │  ├─ hod_name
   │  ├─ hod_email
   │  ├─ start_date
   │  ├─ end_date
   │  └─ is_current

   
ANALYTICS & REPORTING
   └─ Pre-aggregated views for:
      ├─ Attendance percentages
      ├─ Department statistics
      ├─ Student trends
      └─ Historical analytics
```

#### **4. External Storage (Google Sheets)**

Real-time operational log for attendance:

```
GOOGLE SHEET: "STUDENT ATTENDANCE"
┌────────────────────────────────┐
│ Sheet1: Attendance Log         │
├──────────┬──────────┬──────────┤
│   Date   │ Student  │Department│
│          │   ID     │   ID     │
├──────────┼──────────┼──────────┤
│2025-04-01│260401-0001│ CS-001  │
│2025-04-01│260401-0002│ IT-001  │
│2025-04-01│260401-0001│ CS-001  │
└──────────┴──────────┴──────────┘
```

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/15 ATTENDENCE STOTE IN G-SHEET .png" width="900">
</p>

### System Communication Flow

```
FRONTEND (Streamlit UI)
        │
        ├─→ AUTH LAYER (Supabase Auth)
        │   └─ Validate admin credentials
        │
        ├─→ APPLICATION LOGIC
        │   │
        │   ├─→ RDB (Supabase)
        │   │   ├─ Read: Student, Department, Admin data
        │   │   └─ Write: Update records, create entries
        │   │
        │   ├─→ VDB (Qdrant)
        │   │   ├─ Store: Face embeddings (MTCNN + FaceNet)
        │   │   └─ Search: Cosine similarity for face matching
        │   │
        │   ├─→ GCP (Google Sheets)
        │   │   ├─ Write: Real-time attendance logging
        │   │   └─ Read: Batch student registration data
        │   │
        │   ├─→ ML MODELS (MTCNN + FaceNet)
        │   │   └─ Process: Face detection & embedding generation
        │   │
        │   └─→ EMAIL SERVICE (SMTP)
        │       ├─ Send: Registration confirmations
        │       └─ Send: Attendance reports to HODs
        │
        └─→ DATA WAREHOUSE (Databricks)
            ├─ Query: Aggregated attendance data
            ├─ Trigger: ETL pipeline jobs
            └─ Analytics: Generate reports
```


## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/) [ we use 3.12 ]
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
# -------------------------------->  Using venv

python -m venv venv

# --------------------------------> Activate virtual environment

venv\Scripts\activate       # ----> On Windows

source venv/bin/activate    # ----> On macOS/Linux:
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Requirements include:**
- databricks-sql-connector
- databricks
- streamlit
- facenet-pytorch
- torch
- supabase
- pillow
- gotrue
- qdrant-client
- httpx[http2]
- gspread
- google-auth
- pytz

---

## ⚙️ Configuration

### **1. Environment Setup**

Create a `.streamlit/secrets.toml` file in the project root with all required credentials:

```toml
# ====================== SUPABASE CONFIGURATION ======================

[supabase_api]
url = "https://your-project.supabase.co"
anon_key = "your_anon_key_here"

[supabase_db]
host = "db. < ---- > .supabase.co"
port = 5432
database = "postgres"
user = "postgres"
password = " your password "

# ====================== QDRANT CONFIGURATION =======================

[qdrant]
url = "https://your-qdrant-instance.com"
api_key = "your_qdrant_api_key"

# ====================== DATABRICKS CONFIGURATION ====================

[databricks]
host = "https://your-workspace.cloud.databricks.com"
token = "your_databricks_token"
http_path = "sql/1.0/warehouses/your_warehouse_id"
# Job IDs for automated pipelines
student_job_id = "123456789"
department_job_id = "123456790"
attendance_job_id = "123456791"

# ====================== GOOGLE CLOUD CREDENTIALS ====================

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your_key_id"
private_key = "your_private_key"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your_client_id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your_cert_url"

# ====================== SMTP EMAIL CONFIGURATION ====================

[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "your_app_specific_password"  # NOT your Gmail password!
```

### 2. Supabase (Relational Database) Setup

#### Create Tables

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

**Departments Table:**
```sql
CREATE TABLE department (
    dep_id TEXT PRIMARY KEY,
    dep_name TEXT NOT NULL UNIQUE,
    dep_hod TEXT NOT NULL,
    dep_hod_mail TEXT NOT NULL,
);
```


**App Controls Table:**
```sql
CREATE TABLE app_controls (
    is_registration_open BOOLEAN NOT NULL,
    CONSTRAINT app_controls_pkey PRIMARY KEY (is_registration_open)
    
);

-- Insert initial record

INSERT INTO app_controls (is_registration_open) VALUES (FALSE);
```
**Create RLS (Row Level Security) Policy**
```sql
-- APP CONTROLS

CREATE POLICY "full_access_app_controls"
ON app_controls
FOR ALL
USING (true)
WITH CHECK (true);

-----> STUDENTS (add row / update row / delete row)

CREATE POLICY "full_access_students"
ON students
FOR ALL
USING (true)
WITH CHECK (true);

-----> DEPARTMENT (add row / update row / delete row)

CREATE POLICY "full_access_department"
ON department
FOR ALL
USING (true)
WITH CHECK (true);
```

#### Configure Authentication
1. Go to Supabase Dashboard → Authentication → Providers
2. Enable Email/Password provider
3. Configure email templates for password recovery
4. Set JWT expiration policies

### 3. Qdrant (Vector Database) Setup

#### Create Collection via SQL Management Console

```python
# This is done automatically by VDB_connection_OP.py
# But can also be done manually:

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

client = QdrantClient(url="your_qdrant_url", api_key="your_api_key")

# Create collection for face embeddings

client.create_collection(
    collection_name="student_face_encodings_",
    vectors_config=VectorParams(
        size=512,                 # FaceNet embedding dimension
        distance=Distance.COSINE  # Similarity metric
    )
)

# Create payload index for filtering by student ID

client.create_payload_index(
    collection_name="student_face_encodings_",
    field_name="S_id",
    field_schema=PayloadSchemaType.KEYWORD
)
```

#### Point Structure
```python
PointStruct(
    id=str(uuid.uuid4()),        # Unique point ID
    vector=embedding_list,       # 512-dimensional FaceNet embedding
    payload={
        "S_id": "260401-0001",   # Student ID
        "S_name": "John Doe",
        "dep_id": "CS-001",
        "timestamp": "2025-04-01T10:30:00Z"
    }
)
```

### 4. Databricks Data Warehouse Setup

#### Step 1: Create Unity Catalog Structure
Run the SQL from `PIPELINE/01_CREATE_CATALOG_AND_SCHEMA.SQL`:

```sql
-- Create Catalog
CREATE CATALOG IF NOT EXISTS college_dw;

-- Create Schemas (Bronze/Silver/Gold layers)

CREATE SCHEMA IF NOT EXISTS college_dw.bronze;
CREATE SCHEMA IF NOT EXISTS college_dw.silver;
CREATE SCHEMA IF NOT EXISTS college_dw.gold;
```

#### Step 2: Create ETL Jobs
Upload and schedule the Jupyter notebooks from `PIPELINE/` folder:
- `02_Student_Pipeline.ipynb` - Process student dimension
- `03_Department_Pipeline.ipynb` - Process department dimension
- `04_Fact_Attendance_Pipeline.ipynb` - Process attendance facts

#### Step 3: Configure Job Triggers
Set schedule or event-based triggers:
- Student job: Daily at 2:00 AM
- Department job: Weekly on Monday
- Attendance job: Daily at 3:00 AM

### 5. Google Sheets API Setup

#### Step 1: Create Service Account
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable **Google Sheets API** and **Google Drive API**
4. Create a **Service Account**:
   - Service account name: `attendance-system`
   - Grant editor role
5. Create a **JSON key** and save to `secrets.toml`

#### Step 2: Create Spreadsheets
Create two Google Sheets:

**Sheet 1: Student Registration Form** (`STUDENT REGISTRATION`)
```
| Student Name | Email | Phone | Address | Department | Admission Year | DOB |[[ Face-Embedding-1 ],[ Face-Embedding-2 ],[ Face-Embedding-3 ]] |
```

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/" width="900">
</p>

**Sheet 2: Attendance Log** (`STUDENT ATTENDANCE`)
```
| Date | Student ID | Department ID |
```

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/15 ATTENDENCE STOTE IN G-SHEET .png" width="900">
</p>

#### Step 3: Share Sheets
1. Open each Google Sheet
2. Share with service account email from `secrets.toml`
3. Grant "Editor" permission

### 6. SMTP Email Configuration

#### Gmail Setup (Recommended)
1. Enable **2-Factor Authentication** in your Google Account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** and **Windows Computer** (or your OS)
4. Google generates a 16-character password
5. Add this to `secrets.toml`:

```toml
[email]
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "your-email@gmail.com"
sender_password = "xxxx xxxx xxxx xxxx"  # 16-char app password
```

### 7. Python Virtual Environment

```bash
# --------> Create virtual environment
python -m venv env

# --------> Activate (Windows)
.\env\Scripts\activate

# --------> Activate (Linux/Mac)
source env/bin/activate

# --------> Install dependencies
pip install -r requirements.txt
```



---

## 📁 Project Structure & Components

```
P14-Facial-Recognition-Based-Attendance-System-main/
│
├── 📄 app.py
│   └─ Main Streamlit entry point with page routing and session management
│      • Handles page navigation
│      • Manages login state
│      • Routes to appropriate UI components
│
├── 📄 requirements.txt
│   └─ Python package dependencies (streamlit, torch, supabase, etc.)
│
├── 📋 LEARN.md
│   └─ Comprehensive project documentation 
│
├── 📋 README.md
│   └─ Quick start and basic usage guide
│
├── 📋 LICENSE
│   └─ MIT License
│
├── 📁 BACKEND/ (Database & Business Logic)
│   │
│   ├── admin_OP.py
│   │   └─ Admin authentication using Supabase Auth
│   │      • admin_verification(email, password, supabase)
│   │      • Email/password validation
│   │      • Session token management
│   │
│   ├── RDB_connection_OP.py
│   │   └─ Supabase PostgreSQL connection management
│   │      • Initialize Supabase client
│   │      • Connection pooling via session state
│   │      • Error handling
│   │
│   ├── VDB_connection_OP.py
│   │   └─ Qdrant vector database client setup
│   │      • Initialize Qdrant client with API credentials
│   │      • Create collection if not exists (512-dim vectors)
│   │      • Payload index creation for filtering
│   │
│   ├── databricks_connection_OP.py
│   │   └─ Databricks SQL connection and job management
│   │      • trigger_databricks_job(job_type) - Start ETL pipelines
│   │      • get_job_status(job_type) - Monitor job execution
│   │      • Supports: student, department, attendance jobs
│   │
│   ├── student_OP.py
│   │   └─ Student CRUD operations and face recognition
│   │      • process_and_upload_students() - Batch registration
│   │      • get_students_by_department() - Retrieve department students
│   │      • find_student_by_embedding() - Face matching via vector search
│   │      • update_student_info() - Modify student records
│   │      • delete_student() - Remove from RDB and VDB
│   │
│   ├── department_OP.py
│   │   └─ Department management operations
│   │      • get_departments_with_hod() - Retrieve all departments
│   │      • add_department() - Create new department
│   │      • update_department() - Modify department info
│   │
│   ├── report_OP.py
│   │   └─ Attendance analytics and email reporting
│   │      • get_attendance_from_gold() - Query Databricks Gold layer
│   │      • generate_and_send_reports() - Create and email reports
│   │      • Calculate attendance percentages and statistics
│   │
│   └── supabase_connection_OP.py
│       └─ Legacy Supabase connection (superceded by RDB_connection_OP)
│
├── 📁 FUNC/ (Functional Modules & Utilities)
│   │
│   ├── face_embedding_OP.py
│   │   └─ Face detection and embedding generation
│   │      • load_models() - Load MTCNN and FaceNet models (cached)
│   │      • get_face_embedding() - Generate 512-dim embedding from image
│   │      • GPU/CPU acceleration support
│   │      • Error handling for no-face detection
│   │
│   ├── attendance_gspread.py
│   │   └─ Google Sheets integration
│   │      • connect_to_gsheet() - Establish connection
│   │      • write_to_sheet() - Log attendance record
│   │      • read_from_sheet() - Batch read student data
│   │      • clear_sheet() - Reset registration data
│   │
│   ├── g_spread.py
│   │   └─ General Google Sheets operations
│   │      • Helper functions for spreadsheet manipulation
│   │
│   ├── send_email.py
│   │   └─ Email notification service
│   │      • send_registration_email() - Confirmation with Student ID
│   │      • send_report_email() - Attendance reports to HODs
│   │      • HTML formatting and SMTP configuration
│   │
│   └── navigation.py
│       └─ Streamlit page routing utility
│          • go_to() - Navigate between pages via session state
│
├── 📁 UI/ (Streamlit Interface Pages)
│   │
│   ├── Home.py
│   │   └─ Landing page with login buttons
│   │      • Two-column layout: Admin Login / Student Attendance
│   │      • Entry point for all users
│   │
│   ├── Admin_login.py
│   │   └─ Admin authentication page
│   │      • Email and password input
│   │      • Session state login tracking
│   │      • Error handling with Supabase Auth
│   │
│   ├── Admin_option.py
│   │   └─ Admin dashboard and main menu
│   │      • Navigation buttons to all admin features
│   │      • Conditional routing based on login status
│   │
│   ├── Add_new_department.py
│   │   └─ Department creation interface
│   │      • Input form for department details
│   │      • HOD information collection
│   │      • Validation and Supabase write
│   │
│   ├── Update_department_info.py
│   │   └─ Department information update interface
│   │      • Select existing department
│   │      • Modify name, HOD, email
│   │      • Update in Supabase
│   │
│   ├── Add_new_student.py
│   │   └─ Student registration form management
│   │      • Open/Close registration form (app control)
│   │      • Read from Google Sheets
│   │      • Trigger face embedding generation
│   │      • Batch upload to Supabase + Qdrant
│   │
│   ├── Update_student_info.py
│   │   └─ Student information modification interface
│   │      • Search and select student
│   │      • Update personal information
│   │      • Regenerate face embeddings if needed
│   │
│   ├── Remove_student.py
│   │   └─ Student deletion interface
│   │      • Confirmation dialog
│   │      • Delete from RDB and VDB
│   │      • Clean up associated data
│   │
│   ├── Attendance_list.py
│   │   └─ Attendance reporting interface
│   │      • Date range selection
│   │      • Department filtering
│   │      • Query Databricks Gold layer
│   │      • Generate and email reports
│   │
│   ├── Job_monitor.py
│   │   └─ Databricks pipeline job monitoring
│   │      • Trigger ETL jobs (student/department/attendance)
│   │      • Monitor job status and logs
│   │
│   └── __pycache__/
│       └─ Python compiled bytecode cache
│
├── 📁 PIPELINE/ (Databricks ETL Notebooks)
│   │
│   ├── 01_CREATE_CATALOG_AND_SCHEMA.SQL
│   │   └─ Initialize Databricks catalog structure
│   │      • Create Unity Catalog
│   │      • Define Bronze/Silver/Gold schemas
│   │
│   ├── 02_Student_Pipeline.ipynb
│   │   └─ Student data ETL from Supabase to Databricks
│   │      • Extract from RDB (Supabase)
│   │      • Transform and validate
│   │      • Load to Gold layer fact table
│   │
│   ├── 03_Department_Pipeline.ipynb
│   │   └─ Department dimension table processing
│   │      • Extract from Supabase
│   │      • Create slowly changing dimension
│   │
│   ├── 04_Fact_Attendance_Pipeline.ipynb
│   │   └─ Core attendance fact table processing
│   │      • Extract from Google Sheets
│   │      • Transform with date dimensions
│   │      • Aggregate for analytics
│   │
│   └── 05_Clean_Google_Sheet_Weakly_Basis.ipynb
│       └─ Weekly cleanup and archival of Google Sheets
│          • Remove processed records
│          • Archive to backup sheet
│
├── 📁 IMAGES/ (Visual Assets & Documentation)
│   │
│   ├── 00 DIAGRAM/
│   │   └─ Architecture and flow diagrams
│   │
│   ├── 01 WEBSITE IMAGES/
│   │   └─ UI screenshots and mockups
│   │
│   └── 02 DATABRICKS IMAGES/
│       └─ Data warehouse and pipeline screenshots
│
└── 📁 env/ (Python Virtual Environment)
    └─ Isolated Python dependencies and packages
```
---

## 🎮 Usage & Workflows

### Starting the Application

```bash
# Activate virtual environment
.\env\Scripts\activate  # Windows
# or
source env/bin/activate  # Linux/Mac

# Run Streamlit application
streamlit run app.py

# Application starts at: http://localhost:8501
```

### Admin Workflow

#### 1. Admin Login
- Navigate to home page → Click "Admin Login"
- Enter email and password (credentials stored in Supabase Auth)
- Authentication via Supabase → JWT token stored in session state
- Redirects to Admin Dashboard

```
Email:    admin@college.edu
Password: ••••••••
         [Login Button]
```

#### 2. Department Management

**Add New Department**:
1. Admin Dashboard → "Add Department"
2. Fill form:
   - Department ID: CS-001 (unique identifier)
   - Department Name: Computer Science
   - HOD Name: Dr. Raj Verma
   - HOD Email: raj@college.edu
3. Submit → Record created in Supabase
4. Confirmation message displayed

**Update Department Info**:
1. Admin Dashboard → "Update Department"
2. Select existing department from dropdown
3. Modify fields (name, HOD, email)
4. Save → Update in Supabase

#### 3. Student Management

**Add New Students (Batch)**:
1. Open registration form: Admin Dashboard → "Student Registration Management"
2. Click "Open Registration Form"
   - Enables external student registration via Google Form/Sheets
   - Students fill: Name, Email, Phone, Address, Department, DOB
   - Students upload 3 photos for face registration
3. Admin clicks "Upload Student Data"
   - Reads from Google Sheets
   - For each student:
     ```
     ✓ Generate Face Embeddings (3 photos → 3 vectors)
     ✓ Generate Student ID (YYMMDD-XXXX format)
     ✓ Store in Supabase (RDB)
     ✓ Store embeddings in Qdrant (VDB)
     ✓ Send registration email with Student ID
     ```
4. Click "Close Form" to stop new registrations

**Student Registration Flow**

<p align="center">
  <img src="IMAGES/00 DIAGRAM/01 STUDENT REGISTRATION PROCESS.png" width="900">
</p>


**Update Student Information**:
1. Admin Dashboard → "Update Student Information"
2. Search by Student ID or email
3. Modify fields: Name, phone, address, etc.
4. Optionally regenerate face embeddings (if photos changed)
5. Save → Update to Supabase and Qdrant

**Update Student Info**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/06 UPDATE STUDENT INFORMATION.png" width="900">
</p>


**Remove Student**:
1. Admin Dashboard → "Remove Student"
2. Confirm student details
3. Confirmation dialog: "Are you sure?"
4. Click confirm → 
   ```
   ✓ Delete from students table (Supabase)
   ✓ Delete embeddings by S_id (Qdrant)
   ✓ Remove from attendance records
   ```

**Remove Student**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/07 REMOVE STUDENT.png" width="900">
</p>

#### 4. Monitor Data Pipelines

**Manual Trigger Databricks Jobs :**
1. Admin Dashboard → "Job Monitor"
2. Available jobs:
   - Student Pipeline: Process student dimension table
   - Department Pipeline: Update department dimension
   - Attendance Pipeline: Process attendance facts
3. Click "Trigger [Job Name]"
   - Sends request to Databricks API
   - Job starts running in background
4. View Job Status:
   - Shows: Running / Completed / Failed
   - Log output if available
   - Last run timestamp


<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/12 RUNNING PIPELINE MANUALLY.png" width="900">
</p>

#### 5. Generate & Send Reports

**Generate Attendance Reports**:
1. Admin Dashboard → "Attendance List & Reporting"
2. Select date range:
   - Start Date: 2025-04-01
   - End Date: 2025-04-30
3. System calculates:
   - Total working days (excludes weekends + extra holidays)
   - Working hours filter (if configured)
4. Select departments to include
5. Click "Generate Report"
   - Queries Databricks Gold layer
   - Creates HTML-formatted report
6. Click "Send Reports"
   - Sends via SMTP to each HOD
   - Email includes:
     ```
     Subject: Attendance Report - April 2025
     
     Department: Computer Science
     Reporting Period: April 1-30, 2025
     Working Days: 20
     
     Student-wise Attendance:
     260401-0001 | Rajesh Kumar | 18/20 | 90.00%
     260401-0002 | Priya Singh  | 19/20 | 95.00%
     260401-0003 | Arun Patel   | 17/20 | 85.00%
     
     Department Average: 90.00%
     Generated: 2025-05-01 10:30 AM
     ```

**Attendance Report Interface**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/10 GENERATE REPORT AND MAIL TO HOD.png" width="900">
</p>

**Report Email to HOD**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/16 ATTENDANCE MAIl TO HOD.png" width="900">
</p>

### Student Attendance Workflow

#### 1. Navigate to Attendance Page (Local Machine)
- Home page → "Give Attendance"
- Camera will on within a particular duration 

#### 2. Capture Photo
- Click "Capture Image"
- System accesses webcam
- Capture clear frontal face image
- Good lighting recommended
- confirm your identity

```
Image Requirements:
✓ Face clearly visible (no tilt > 15°)
✓ No occlusions (glasses OK, masks NO)
✓ Good lighting (no shadows on face)
✓ Minimum face size: 20px
```

#### 3. Face Recognition Process
```
Captured Image
    ↓
Face Detection (MTCNN)
├─ Error → "No face detected, please try again"
└─ Success → Align face (160x160)
    ↓
Generate Embedding (FaceNet)
├─ Output: 512-dimensional vector
└─ Processing: ~100-200ms (GPU)
    ↓
Vector Search (Qdrant)
├─ Search: Cosine similarity > 0.60 threshold
├─ Filter: Active students only
└─ Top match: Most similar student
    ↓
Confidence Check
├─ High (0.85-1.0): Proceed to confirmation
└─ Medium (0.60-0.85): Show match, ask confirmation
    ↓
Confirm Identity
├─ ✓ Yes → Log attendance
└─ ✗ No/Not you → Try again
    ↓
Log to Google Sheets
├─ Record: Date, Student ID, Department ID
├─ Timestamp: server time (UTC)
└─ Update: Real-time visible in sheet
    ↓
Success Message
└─ "Attendance marked successfully!"
```

**Real-Time Face Recognition**

<p align="center">
  <img src="IMAGES/00 DIAGRAM/02 GIVING ATTENDANCE PROCESS.png" width="900">
</p>


**Attendance Confirmation**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/14 CONFIRM ITS YOU .png" width="900">
</p>


#### 4. Duplicate Prevention
- System checks: Did student already mark today?
- If YES:
  ```
  ⚠️ Already marked attendance today!
  Previous mark time: 10:30 AM
  ```
- If NO: Proceed with marking


**Attendance Log**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/15 ATTENDENCE STOTE IN G-SHEET .png" width="900">
</p>

---  

### **Face Embedding Generation Principle (Background)**

#### ***MTCNN** ( Multi Task Cascaded Convolutional Networks ) + InceptionResnetV1*

<p align="center">
  <img src="IMAGES/00 DIAGRAM/11 FACE EMBEDDING ARCHITECTURE.png" width="900">
</p>

#### **MTCNN Workflow**

<p align="center">
  <img src="IMAGES/00 DIAGRAM/12 MTCNN WORKFLOW.png" width="900">
</p>

#### *MTCNN Architecture*

<p align="center">
  <img src="IMAGES/00 DIAGRAM/13 MTCNN ARCHITECTURE.png" width="900">
</p>

#### *Example*


<p align="center">
  <img src="IMAGES/00 DIAGRAM/14 MTCNN EXAMPLE.png" width="900">
</p>

#### *VGGface2*

<p align="center">
  <img src="IMAGES/00 DIAGRAM/15 VGGFACE2.png" width="900">
</p>



### Data Pipeline Workflow (Background)

#### **Daily Process**
```
Student Pipeline --> Once a day
    ↓
Databricks Student Job Triggers
├─1. Extract: Read from Supabase RDB → Bronze layer
├─2. Transform: Deduplicate, validate  → Silver layer
├─3. Load: Create/update dim_students → Gold layer
└─4. Index: Rebuild analytics views
    ↓
If Pipeline Fail --> Notification
```
```
Department Pipeline --> Once a day
    ↓
Databricks Department Job Triggers
├─1. Extract: Read from Supabase RDB → Bronze layer
├─2. Transform: Deduplicate, validate  → Silver layer
├─3. Load: Create/update dim_department → Gold layer
└─4. Index: Rebuild analytics views
    ↓
If Pipeline Fail --> Notification
```
#### **Daily Attendance Processing**
```
Attendance Pipeline --> Daily (9:00 - 10:59)-->15 min. interval
    ↓
Databricks Attendance Job Triggers
├─1. Extract: Read from Google Sheets → Bronze layer
├─2. Transform: Parse dates, deduplicate → Silver layer
├─3. Aggregate: Group by student/dept → Gold layer
├─4. Calculate: Attendance percentages, metrics
└─5. Create: Pre-aggregated view tables
    ↓
Report Views Ready
└─ Admin can generate reports instantly
```

<p align="center">
<img src="IMAGES/00 DIAGRAM/05 DATA PIPELINE WITH SCHEDULING .png" width="900">
</p>



## 🔑 Key Modules & Core Functions

### Face Recognition Pipeline (`FUNC/face_embedding_OP.py`)

**Purpose**: Generate 512-dimensional face embeddings for student identification

```python
# Load Models (Cached on Startup)
mtcnn, resnet = load_models()
# MTCNN: Detects face regions in images
# ResNet: Generates 512-dim embeddings from aligned faces

# Generate Embedding from Image
embedding_list, message = get_face_embedding(image)
# Input: PIL Image object
# Output: 512-dimensional embedding vector | Error message
# Process:
#  1. Convert to RGB
#  2. Detect face using MTCNN
#  3. Align face (160x160)
#  4. Generate embedding using ResNet
#  5. Normalize to list
```

**Key Parameters**:
- MTCNN image size: 160x160 pixels (FaceNet standard)
- Margin: 0 pixels (no padding)
- Min face size: 20 pixels
- Device: GPU (CUDA) if available, else CPU
- Output vector dimension: 512

### Student Operations (`BACKEND/student_OP.py`)

**Function 1: Register New Students**
```python
process_and_upload_students(student_records: list)
# Batch processing from Google Sheets
# For each student:
#  1. Generate unique ID (date + counter)
#  2. Extract face photos
#  3. Generate embeddings for each photo
#  4. Upsert to Supabase (students table)
#  5. Upsert to Qdrant (face vectors)
#  6. Send registration confirmation email
# Returns: List of processed students with generated IDs
```

**Function 2: Find Student by Face**
```python
find_student_by_embedding(embedding_vector)
# Search in Qdrant with cosine similarity
# Uses vector search: similarity > threshold (typically 0.6)
# Payload filter: Group by student (handle multiple photos)
# Returns: Most similar student with confidence score
```

**Function 3: Manage Student Records**
```python
get_student_by_id(student_id)  # Retrieve full student details
update_student_info(student_id, new_data)  # Modify record
delete_student(student_id)  # Remove from RDB and VDB
```

### Attendance Operations (`BACKEND/student_OP.py`) - Integrated with Core Logic

**Real-time Classification**:
```
Capture Image → Detect Face (MTCNN)
    ↓
Generate Embedding (FaceNet)
    ↓
Search Qdrant (Cosine Similarity)
    ↓
Retrieve Student Info → Confidence Check
    ↓
Manual Confirmation → Log to Google Sheets
```

**Duplicate Prevention**:
- Check attendance log for today's date
- Flag if student already marked present
- Prevent same-day multiple entries

### Report Generation (`BACKEND/report_OP.py`)

**Query Attendance Data**:
```python
get_attendance_from_gold(start_date, end_date, total_working_days)
# Queries Databricks Gold layer
# Groups by department and student
# Calculates:
#  - Present days count
#  - Attendance percentage = (present_days / total_working_days) * 100
# Returns: DataFrame with aggregated statistics
```

**Generate & Send Reports**:
```python
generate_and_send_reports(attendance_df, departments, total_working_days, ...)
# For each department:
#  1. Extract department students
#  2. Create HTML email template
#  3. Include attendance breakdown
#  4. Send via SMTP to HOD email
# HTML includes:
#  - Department name and period
#  - Student-wise attendance with percentages
#  - Department average attendance
#  - Working days count
```

### Email Service (`FUNC/send_email.py`)

**Registration Email**:
```python
send_registration_email(student_email, student_id, student_name)
# Template: Confirmation with generated Student ID
# Includes: Instructions for first attendance
# SMTP: TLS encryption, authentication
```

**Report Email**:
```python
send_report_email(hod_email, department, html_content, period)
# Template: Formatted attendance report
# Includes: Student list with attendance %
# Footer: Generated timestamp and system info
```

### Google Sheets Integration (`FUNC/attendance_gspread.py`)

**Write Attendance**:
```python
write_to_sheet(sheet, data_row: dict)
# Input: {"Date": "2025-04-01", "Student ID": "260401-0001", "Department ID": "CS-001"}
# Appends to next available row
# Handles: Column ordering, data formatting
# Returns: Success/failure status
```

**Read Student Data**:
```python
read_from_sheet(sheet)
# Batch read all rows
# Returns: List of dictionaries (one per student)
# Used for: Student registration workflow
```

### Authentication (`BACKEND/admin_OP.py`)

**Admin Verification**:
```python
admin_verification(email: str, password: str, supabase: Client)
# Uses Supabase Auth service
# Process:
#  1. Call supabase.auth.sign_in_with_password()
#  2. Validate credentials against Supabase Auth DB
#  3. Return JWT token on success
#  4. Store token in Streamlit session state
# Returns: (success: bool, message: str or email: str)
```

### Navigation System (`FUNC/navigation.py`)

**Page Routing**:
```python
go_to(page_name: str)
# Updates Streamlit session state
# Triggers re-run to render new page
# Maintains login state across navigation
```

---

## 💾 Database Schema & Data Models

### Relational Database (Supabase / PostgreSQL)

#### STUDENTS Collection
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| S_id | TEXT | PRIMARY KEY | Generated format: YYMMDD-0001 |
| S_name | TEXT | NOT NULL | Full student name |
| S_mail | TEXT | UNIQUE, NOT NULL | Student email address |
| S_phone | TEXT | NOT NULL | Contact phone number |
| S_address | TEXT | - | Residential address |
| dep_id | TEXT | FK → department, NOT NULL | Department assignment |
| S_admissionyear | INT | NOT NULL | Year of admission (e.g., 2023) |
| S_dob | DATE | NOT NULL | Date of birth |


**Sample Data**:
```
S_id: "260401-0001"
S_name: "Rajesh Kumar"
S_mail: "rajesh.k@college.edu"
S_phone: "9876543210"
S_address: "123 Main Street, City"
dep_id: "CS-001" (References department table)
S_admissionyear: 2023
S_dob: "2004-05-15"
```

#### DEPARTMENTS Collection
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| dep_id | TEXT | PRIMARY KEY | Department identifier (e.g., CS-001) |
| dep_name | TEXT | NOT NULL, UNIQUE | Department full name |
| dep_hod | TEXT | NOT NULL | Head of Department name |
| dep_hod_mail | TEXT | NOT NULL | HOD email address |


**Sample Data**:
```
dep_id: "CS-001"
dep_name: "Computer Science"
dep_hod: "Dr. Raj Verma"
dep_hod_mail: "raj.verma@college.edu"

```

### Vector Database (Qdrant)

#### Collection: "student_face_encodings_"

**Configuration**:
- Vector Size: 512 dimensions (FaceNet embedding)
- Distance Metric: Cosine similarity
- Payload Index: S_id (KEYWORD)

**Point Structure**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "vector": [
    -0.0234, 0.1456, -0.0789, ..., 0.2345  // 512 dimensions
  ],
  "payload": {
    "S_id": "260401-0001",
    "S_name": "Rajesh Kumar",
    "dep_id": "CS-001",
    "status": "active",
    "embedded_at": "2025-04-01T10:35:25Z"
  }
}
```

**Multiple Embeddings Per Student**:
```
Student "260401-0001" has 3 points:
├─ Point 1: photo_1.jpg embedding
├─ Point 2: photo_2.jpg embedding
└─ Point 3: photo_3.jpg embedding

All share same payload S_id but different vectors
Helps improve matching reliability
```

**Search Operation**:
```pseudocode
Query Vector: [live_capture_embedding] (512-dim)

Search with cosine_similarity score > 0.60

Matching Points (filtered by S_id):
├─ Score: 0.89 (S_id: 260401-0001) ✓ MATCH
├─ Score: 0.54 (S_id: 260401-0002) ✗ NO MATCH
└─ Score: 0.71 (S_id: 260401-0001) ✓ MATCH (same student)

Result: Student 260401-0001 (confidence: 0.89)
```

### **Data Warehouse (Databricks)**


### *1. Data Ingesion from Sourse Systems*


<p align="center">
<img src="IMAGES/00 DIAGRAM/04 MOVE DAT FROM TDB TO DWH.png" width="900">
</p>

### *2. Student Schema Through ETL Pipeline*


<p align="center">
<img src="IMAGES/00 DIAGRAM/08 PIPELINE -STUDENT.png" width="900">
</p>


### *3. Department Schema Through ETL Pipeline*


<p align="center">
<img src="IMAGES/00 DIAGRAM/09 PIPELINE - DEPARTMENT.png" width="900">
</p>


### *4. Attendance Schema Through ETL Pipeline*


<p align="center">
<img src="IMAGES/00 DIAGRAM/10 PIPELINE ATTENDANCE.png" width="900">
</p>


### *Scheduling of the ETL jobs*


<p align="center">
<img src="IMAGES/00 DIAGRAM/05 DATA PIPELINE WITH SCHEDULING .png" width="900">
</p>


### *Student Pipeline job overview*


<p align="center">
<img src="IMAGES/02 DATABRICKS IMAGES/02  STUDENT PIPELINE.png" width="900">
</p>

### *Department Pipeline job overview*


<p align="center">
<img src="IMAGES/02 DATABRICKS IMAGES/03 DEPARTMENT PIPELINE.png" width="900">
</p>

### *Attendance Pipeline job overview*


<p align="center">
<img src="IMAGES/02 DATABRICKS IMAGES/04 ATTENDANCE PIPELINE.png" width="900">
</p>

### Google Sheets Data Storage

#### Sheet: "STUDENT ATTENDANCE"

```
Headers: [Date, Student ID, Department ID]

Data Format:
┌─────────────┬──────────────┬────────────────┐
│    Date     │  Student ID  │ Department ID  │
├─────────────┼──────────────┼────────────────┤
│ 2025-04-01  │ 260401-0001  │    CS-001      │
│ 2025-04-01  │ 260401-0002  │    IT-001      │
│ 2025-04-01  │ 260401-0001  │    CS-001      │  ← Duplicate (same day)
│ 2025-04-02  │ 260401-0002  │    IT-001      │
│ 2025-04-02  │ 260401-0003  │    ECE-001     │
└─────────────┴──────────────┴────────────────┘

Daily Volume:
- College with 5000 students
- Expected daily marks: 450-480 (90% attendance)
- Growth: +0.5-1% per month

Data Retention:
- Current term: In Sheet (live)
- Previous term: Archive sheet (05_Clean_Google_Sheet_Weakly_Basis.ipynb)
- Historical: In Databricks (permanent)
```

### *Clean Google Sheet Weakly*


<p align="center">
<img src="IMAGES/02 DATABRICKS IMAGES/05 CREAR SHEET PIPELINE.png" width="900">
</p>

---

## 🔗 API Integration & External Services

### Supabase API

**Authentication Endpoint**:
```python
# Sign in with password
response = supabase.auth.sign_in_with_password({
    "email": "admin@college.edu",
    "password": "secure_password"
})

# Returns: User object with JWT token
user = response.user  # UUID, email
token = response.session.access_token
```

**Table Operations (RPC)**:
```python
# Read
students = supabase.table("students") \
    .select("*") \
    .eq("dep_id", "CS-001") \
    .execute()

# Create
supabase.table("students") \
    .insert(student_data) \
    .execute()

# Update
supabase.table("students") \
    .update({"s_phone": "9876543210"}) \
    .eq("s_id", "260401-0001") \
    .execute()

# Delete
supabase.table("students") \
    .delete() \
    .eq("s_id", "260401-0001") \
    .execute()
```

### Qdrant Vector API

**Search Endpoint** (HTTP/gRPC):
```python
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

# Search with filtering
results = qdrant_client.search(
    collection_name="student_face_encodings_",
    query_vector=embedding_vector,  # 512 dimensions
    query_filter=Filter(
        must=[
            FieldCondition(
                key="S_id",
                match=MatchValue(value="260401-0001")  # Filter by student
            )
        ]
    ),
    limit=5,  # Top 5 matches
    score_threshold=0.60  # Confidence threshold
)

# Results: [ScoredPoint, ...] with scores (0-1)
```

**Upsert Endpoint** (Batch register embeddings):
```python
from qdrant_client.http.models import PointStruct

points = [
    PointStruct(
        id="uuid1",
        vector=embedding_1,
        payload={"S_id": "260401-0001", "S_name": "Rajesh"}
    ),
    PointStruct(
        id="uuid2",
        vector=embedding_2,
        payload={"S_id": "260401-0001", "S_name": "Rajesh"}
    )
]

qdrant_client.upsert(
    collection_name="student_face_encodings_",
    points=points
)
```

### Google Sheets API (via gspread)

**Connect & Read**:
```python
import gspread
from google.oauth2.service_account import Credentials

creds = Credentials.from_service_account_file(
    "path/to/credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open("STUDENT ATTENDANCE").sheet1

# Read all rows
rows = sheet.get_all_values()

# Append row
sheet.append_row(["2025-04-01", "260401-0001", "CS-001"])
```

### Databricks SQL API

**Query Endpoint**:
```python
from databricks import sql

with sql.connect(
    server_hostname="workspace-id.cloud.databricks.com",
    http_path="sql/1.0/warehouses/warehouse-id",
    access_token="dapi..."
) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT attendance_date, COUNT(*) as mark_count
        FROM college_dw.gold.fact_attendance
        WHERE attendance_date = '2025-04-01'
        GROUP BY attendance_date
    """)
    results = cursor.fetchall()
```

**Job Management API**:
```python
import requests

# Trigger job
response = requests.post(
    f"{host}/api/2.1/jobs/run-now",
    headers={"Authorization": f"Bearer {token}"},
    json={"job_id": 123456}
)

# Get run status
response = requests.get(
    f"{host}/api/2.1/jobs/runs/get?run_id={run_id}",
    headers={"Authorization": f"Bearer {token}"}
)
```

### SMTP Email API

**Send Email**:
```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)

message = MIMEMultipart("alternative")
message["Subject"] = "Attendance Report"
message["From"] = SENDER_EMAIL
message["To"] = recipient

html_body = """
<h2>Attendance Report - April 2025</h2>
<p>Department: Computer Science</p>
...
"""
part = MIMEText(html_body, "html")
message.attach(part)

server.sendmail(SENDER_EMAIL, recipient, message.as_string())
server.quit()
```

---

## 🔒 Security Best Practices

### Authentication & Authorization

**Admin Authentication**:
- ✅ Use Supabase Auth (OAuth2, JWT tokens)
- ✅ Enforce strong passwords (min 8 chars, mixed case, numbers, symbols)
- ✅ Implement session timeout (30 minutes inactivity)
- ✅ Store JWT token in Streamlit session state (not localStorage)
- ❌ Never store passwords in plaintext
- ❌ Avoid hardcoding credentials in source code

**Code Example**:
```python
# ✅ CORRECT: Credentials from secrets

if "supabase" in st.session_state:
    supabase = st.session_state.supabase
else:
    url = st.secrets["supabase_api"]["url"]
    key = st.secrets["supabase_api"]["anon_key"]
    supabase = create_client(url, key)
    st.session_state.supabase = supabase

# ✅ CORRECT: Session-based login

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    show_admin_panel()
else:
    show_login_form()
```

### Data Protection

**API Keys & Credentials**:
- ✅ Store secrets in `.streamlit/secrets.toml` (git ignored)
- ✅ Use environment variables in production
- ✅ Rotate API keys every 3 months
- ✅ Restrict API key permissions (minimal scope)
- ✅ Enable IP whitelisting for sensitive services
- ❌ Never commit secrets to git repository
- ❌ Avoid printing/logging API keys

**Database Security**:
- ✅ Use Row-Level Security (RLS) in Supabase:
  ```sql
  -- Example: Students can only see their own records
  CREATE POLICY "Students see their own record"
    ON students FOR SELECT
    USING (auth.uid() = user_id);
  ```
- ✅ Enable encryption at rest in Supabase
- ✅ Use SSL/TLS for all database connections
- ✅ Regular backups with point-in-time recovery
- ✅ Audit logging for sensitive operations

### Application Security

**Input Validation**:
```python
# ✅ CORRECT: Validate user input
import email_validator
import phonenumbers

def validate_student_input(name, email, phone):
    # Validate email
    try:
        email_validator.validate_email(email)
    except email_validator.EmailNotValidError:
        st.error("Invalid email format")
        return False
    
    # Validate phone
    try:
        phonenumbers.parse(phone, "IN")
    except:
        st.error("Invalid phone number")
        return False
    
    # Validate name (no special chars)
    if not name.replace(" ", "").isalpha():
        st.error("Name contains invalid characters")
        return False
    
    return True
```

**SQL Injection Prevention**:
- ✅ Use parameterized queries (always):
  ```python
  # ✅ CORRECT: Parameterized
  supabase.table("students") \
      .select("*") \
      .eq("s_id", student_id) \
      .execute()
  ```
- ❌ NEVER use string concatenation:
  ```python
  # ❌ WRONG: Vulnerable to SQL injection
  query = f"SELECT * FROM students WHERE s_id = '{student_id}'"
  ```

**File Upload Security**:
- ✅ Validate file types (only images)
- ✅ Check file size (< 5MB)
- ✅ Scan for malware before processing
- ✅ Rename files (use UUID)
- ✅ Store separately from code

```python
# ✅ CORRECT: Secure file handling
import uuid
from PIL import Image

def validate_face_image(uploaded_file):
    # Check file type
    if uploaded_file.type not in ["image/jpeg", "image/png"]:
        st.error("Only JPEG/PNG images allowed")
        return None
    
    # Check file size (5MB)
    if uploaded_file.size > 5 * 1024 * 1024:
        st.error("Image too large (max 5MB)")
        return None
    
    # Check image resolution
    image = Image.open(uploaded_file)
    if image.size[0] < 100 or image.size[1] < 100:
        st.error("Image too small (min 100x100)")
        return None
    
    # Save with UUID name
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join("temp/", filename)
    image.save(filepath)
    
    return filepath
```

### Network Security

**HTTPS/TLS**:
- ✅ Use HTTPS in production (not HTTP)
- ✅ Install SSL certificate (Let's Encrypt free option)
- ✅ Enforce HTTPS redirects

**CORS & API Access**:
- ✅ Configure CORS headers for external APIs
- ✅ Use API rate limiting to prevent abuse
- ✅ Implement API authentication (Bearer token)

### Operational Security

**Logging & Monitoring**:
- ✅ Log all authentication attempts
- ✅ Log data access and modifications
- ✅ Monitor for suspicious patterns
- ✅ Alert on failed login attempts (> 5 in 10 min)
- ✅ Retention: 90 days minimum, 1 year for compliance

```python
# ✅ CORRECT: Audit logging
import logging
from datetime import datetime

logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_action(action, user_id, details):
    logging.info(f"User: {user_id} | Action: {action} | Details: {details}")
```

**Access Control**:
- ✅ Implement role-based access control (RBAC):
  - `super_admin`: All operations
  - `department_admin`: Only their department
  - `student`: Self-service attendance only
- ✅ Enforce principle of least privilege
- ✅ Regular access reviews


### Compliance & Legal

- ✅ **GDPR Compliance**: Implement data retention policies, user consent
- ✅ **Privacy**: Encrypt facial data, anonymize logs
- ✅ **Data Minimization**: Collect only necessary data
- ✅ **Transparency**: Clear privacy policy, data usage disclosure
- ✅ **Right to Erasure**: Implement "delete me" feature
- ✅ **Audit Trail**: Maintain immutable logs for compliance

---

## 🐛 Troubleshooting Guide

### Installation & Environment Issues

**Problem 1: ModuleNotFoundError (import error)**
```
Error: ModuleNotFoundError: No module named 'torch'

Solution:
1. Verify virtual environment is activated:
   Windows: .\env\Scripts\activate
   Linux/Mac: source env/bin/activate
2. Reinstall requirements:
   pip install --upgrade -r requirements.txt
3. Check Python version:
   python --version  # Should be 3.8+
```

**Problem 2: CUDA Not Available (GPU)**
```
Error: CUDA not available, using CPU
Warning: Face recognition will be slower

Solution 1 (Recommended):
1. Install NVIDIA CUDA Toolkit 12.1
2. Install cuDNN matching your CUDA version
3. Reinstall PyTorch:
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Solution 2 (CPU):
- System will automatically use CPU
- Performance will be slower (~1-2 sec per embedding)
- Still functional for small deployments (< 1000 students)
```

### Database Connection Issues

**Problem 3: Supabase Connection Error**
```
Error: Error connecting to Supabase: [error details]

Debugging:
1. Check credentials in .streamlit/secrets.toml
2. Verify URL format: https://xxx.supabase.co
3. Check API key permissions
4. Test connection:
   python -c "from supabase import create_client; 
   c = create_client('url', 'key'); 
   print(c.table('students').select('*').limit(1).execute())"
5. Check network/firewall
6. Ensure Supabase project is not paused
```

**Problem 4: Qdrant Connection Timeout**
```
Error: TimeoutError connecting to Qdrant

Solutions:
1. Check Qdrant URL and API key in secrets.toml
2. Verify Qdrant cluster status (running?)
3. Check network connectivity:
   curl https://your-qdrant-url/health
4. Try increasing timeout:
   # In VDB_connection_OP.py:
   qdrant_client = QdrantClient(
       url=qdrant_url,
       api_key=qdrant_api_key,
       timeout=30  # Increase from default
   )
5. Check rate limits (free tier has limits)
```

**Problem 5: Google Sheets API Error**
```
Error: Spreadsheet 'STUDENT ATTENDANCE' not found

Solutions:
1. Verify sheet name is EXACT:
   - Case-sensitive
   - No leading/trailing spaces
2. Check service account has editor access:
   - Share sheet with: your-service-account@xxx.iam.gserviceaccount.com
3. Verify credentials in secrets.toml:
   python -c "import gspread; 
   from google.oauth2.service_account import Credentials;
   creds_dict = {'type': 'service_account', ...};
   creds = Credentials.from_service_account_info(creds_dict);
   client = gspread.authorize(creds);
   print(client.list_spreadsheet_files())"
4. Check GCP quota limits
```

### Face Recognition Issues

**Problem 6: "No face detected. Please try again."**
```
Causes:
- Low lighting conditions
- Face too small in frame
- Face at excessive angle (> 30°)
- Face partially obscured (mask, hands)
- Poor image quality (blurry, out of focus)

Solutions:
1. Ensure good front lighting (not backlit)
2. Position face centered in camera view
3. Keep face 30-50cm from camera
4. Remove sunglasses, lower mask
5. Focus camera on face first
6. Try multiple captures

Testing:
- Test face detection: python FUNC/face_embedding_OP.py
- Check MTCNN confidence thresholds
```

**Problem 7: Low Face Matching Accuracy**
```
Symptoms:
- Student not recognized (false negative)
- Wrong student identified (false positive)
- Inconsistent matches for same student

Root Causes:
- Poor quality registration photos
- Similar looking students
- Different lighting during capture
- Face angle differences
- Threshold too low/high

Solutions:
1. Retake registration photos:
   - Same lighting as attendance location
   - Same angle (mostly frontal)
   - 3 different expressions
2. Adjust similarity threshold:
   # In student_OP.py:
   score_threshold=0.65  # Try 0.65-0.75 range
3. Add more training images
4. Update student embeddings:
   Admin → Update Student → Regenerate embeddings
5. Check for duplicate students with similar faces
```

**Problem 8: Embedding Generation Timeout**
```
Error: Face embedding generation taking > 30 seconds

Solutions:
1. Check GPU memory:
   nvidia-smi  # Should show > 1GB free
2. Reduce batch size (if batch processing):
   process_batch_size = 5  # Instead of 20
3. Restart Streamlit:
   Clear cache and reload
4. Check CPU load:
   htop  # CPU should be < 80%
5. Verify model loading:
   python -c "from FUNC.face_embedding_OP import load_models; 
   mtcnn, resnet = load_models(); print('Models loaded')"
```

### Attendance Marking Issues

**Problem 9: Duplicate Attendance Entries**
```
Problem:
- Student marked twice on same day
- Attendance sheet has duplicate rows

Causes:
- Duplicate prevention not working
- Multiple concurrent captures
- Network lag causing retry

Solutions:
1. Check duplicate prevention logic:
   # In attendance_gspread.py:
   # Verify date check is in place
2. Manual cleanup:
   - Open Google Sheet
   - Delete duplicate row
   - Verify in Databricks Gold layer
3. Add constraint in Supabase:
   CREATE UNIQUE INDEX idx_daily_attendance
   ON attendance(student_id, DATE(attendance_date))
```

**Problem 10: Attendance Not Saving to Sheet**
```
Error: Write to sheet failed

Debugging:
1. Check Google Sheet permissions:
   - Is it shared with service account?
   - Does service account have editor access?
2. Verify sheet headers:
   - Headers in row 1: Date, Student ID, Department ID
3. Check sheet is not read-only
4. Test write manually:
   from FUNC.attendance_gspread import connect_to_gsheet, write_to_sheet
   sheet = connect_to_gsheet()
   success = write_to_sheet(sheet, {"Date": "2025-04-01", ...})
5. Check quota limits (Google has 100k cell updates/day)
```

### Email Issues

**Problem 11: Registration Emails Not Sending**
```
Error: smtplib.SMTPAuthenticationError

Solutions:
1. Gmail - Use App Password (NOT regular password):
   - Enable 2FA: myaccount.google.com/security
   - Generate app password: myaccount.google.com/apppasswords
   - Use 16-char password in secrets
2. Verify SMTP settings:
   SMTP_SERVER = "smtp.gmail.com"  # Correct
   SMTP_PORT = 587  # TLS (not 465/SMTP)
3. Check firewall allows port 587
4. Test SMTP connection:
   python -c "import smtplib; 
   s = smtplib.SMTP('smtp.gmail.com', 587); 
   s.starttls(); 
   s.login('email', 'password'); 
   print('Connected')"
5. Check sender email in secrets.toml
```

**Problem 12: Report Emails Going to SPAM**
```
Problem:
- Emails sent to CCed SPAM folder

Solutions:
1. Add SPF record:
   v=spf1 include:sendgrid.net ~all
2. Add DKIM signature
3. Use professional sender name:
   From: "Attendance System" <attendance@college.edu>
4. Add unsubscribe link in footer
5. Test with MXToolbox: scan sender reputation
```

### Data Warehouse Issues

**Problem 13: Databricks Job Fails**
```
Error: Job execution failed

Debugging:
1. Check job logs in Databricks UI:
   - Workspace → Jobs → Select job → View logs
2. Check common errors:
   - Table not found: Run 01_CREATE_CATALOG_AND_SCHEMA.SQL
   - Permission denied: Check cluster permissions
   - Timeout: Increase cluster size
3. Verify data exists:
   SELECT COUNT(*) FROM college_dw.gold.fact_attendance
4. Check query syntax for your SQL version
5. Run manually first:
   Copy SQL from notebook → Execute in SQL editor
```

**Problem 14: Queries Returning No Results**
```
Problem:
- Report shows 0 attendance for date range

Causes:
- Wrong date range selected
- No attendance marked in Google Sheet
- Data not synced to Databricks yet
- Filter parameters too restrictive

Solutions:
1. Verify attendance in source:
   Google Sheet → STUDENT ATTENDANCE tab
2. Check if Databricks job ran:
   Workspace → Jobs → Check last run time
3. Wait for next job run (up to 24 hours)
4. Manually trigger job:
   Admin → Job Monitor → Trigger Attendance Job
5. Query Bronze layer directly:
   SELECT * FROM college_dw.bronze.attendance_raw LIMIT 10
```

### Performance Issues

**Problem 15: Application Running Slow**
```
Symptoms:
- Page takes > 5 seconds to load
- Face detection takes > 30 seconds
- Database queries timing out

Diagnostics:
1. Check network latency:
   ping your-supabase-url
2. Monitor resource usage:
   GPU: nvidia-smi
   CPU: top (Mac/Linux) or Task Manager (Windows)
   Memory: free -h (Linux) or Task Manager (Windows)
3. Check database query time:
   Add timestamps before/after queries
4. Profile with:
   streamlit run app.py --logger.level=debug

Solutions:
1. Increase Streamlit cache:
   @st.cache_resource(ttl=600)  # 10 minutes
2. Pre-load heavy models:
   In app.py startup
3. Optimize queries:
   Add indexes on frequently filtered columns
4. Scale infrastructure:
   Upgrade Supabase tier
   Increase Databricks cluster size
5. Enable query optimization:
   Supabase: Enable query plan analysis
```

### Debugging Tools & Commands

```bash
# Check environment
python --version
pip list | grep -E "streamlit|torch|supabase"

# Test individual components
python -c "import torch; print(torch.cuda.is_available())"
python -c "from facenet_pytorch import MTCNN; m = MTCNN()"
python -c "from supabase import create_client; print('OK')"

# Run with debug logging
streamlit run app.py --logger.level=debug

# Check port in use
netstat -an | grep 8501  # Windows
lsof -i :8501  # Mac/Linux

# Clear Streamlit cache
streamlit cache clear

# Test face detection
python FUNC/face_embedding_OP.py

# Verify database schema
python -c "from BACKEND.RDB_connection_OP import supabase; 
print(supabase.table('students').select('*').limit(1).execute())"
```


---
## 🖼️ Screenshots



### **Fig-1 : Home Page**
**Landing Page of Admin Choose Admin for Login**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/00 HOME PAGE.png" width="900">
</p>

### **Fig-2 : Admin Login**
**Admin login interface for authorized access to administrative privileges.**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/01 ADMIN LOGIN.png" width="900">
</p>


### **Fig-3 : Admin Panel**
**Admin panel dashboard providing centralized access to system management features.**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/02 ADMIN OPTIONS.png" width="900">
</p>


### **Fig-4 : Student Registration Control**
<span style="color: green;"><b>Open Form:</b></span> Enables student registration and stores data in Google Sheets.<br><span style="color: red;"><b>Close Form:</b></span> Disables student registration to prevent new submissions.

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/03 STUDENT REGISTRATION MANAGEMENT.png" width="900">
</p>


### **Fig-5 : Student data upload to database**
**Student information from Google Sheet upload to RDB( Supabase ) and student Face Embedding upload to VDB( Quadrant )**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/04 UPLOAD SNEW STUDENT DETAILS TO DATABASE.png" width="900">
</p>


### **Fig-6 : Student registration confirmation**
**Confirmation email received after successful student registration, including system-generated Student ID (email ID hidden for security purposes)**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/05 CONFIRMATION MAIL AFTER SUCESSFULLY REGISTRATION.png" width="900">
</p>


### **Fig-7 : Update student information and face embedding**
**Students can update personal information and regenerate face embeddings by uploading three clear images in cases where initial registration images were unclear or face recognition fails**|

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/06 UPDATE STUDENT INFORMATION.png" width="900">
</p>


### **Fig-8 : Remove student from system**
**Admin confirmation interface for permanently deleting a student’s records when the student leaves the institution, including removal of data from RDB (Supabase) and facial embeddings from VDB (Qdrant)**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/07 REMOVE STUDENT.png" width="900">
</p>


### **Fig-9 : Add a new department**
**Admin interface for adding a new department by entering department ID, department name, Head of Department (HOD) details, and official email information**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/08 ADD NEW DEPARTMENT.png" width="900">
</p>

### **Fig-10 : Update department information**
**Admin interface for modifying existing department details, including department name,  Head of Department (HOD) information, and official email address**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/09 UPDATE DEPARTMENT INFORMATION.png" width="900">
</p>

### **Fig-11 : Attendance list and reporting**
**Interface for generating attendance reports within a selected date range, calculating effective working days, and automatically sending department-wise reports to the respective HODs via email**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/10 GENERATE REPORT AND MAIL TO HOD.png" width="900">
</p>

### **Fig-12 : Attendance report email notification**
**Automatically generated attendance report emailed to the respective Head of Department (HOD), including reporting period, total working days, student-wise attendance details, and attendance percentage**

|<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/16 ATTENDANCE MAIL TO HOD.png" width="900">
</p>

### **Fig-13 : Face-Recognition based attendance marking**
**Student attendance interface using real-time face capture, where attendance can be marked only within a predefined time window configured by college administrators**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/13 GIVE ATTENDENCE.png" width="900">
</p>

### **Fig-14 : Attendance confirmation before write in attendance-log**
**Confirmation interface displayed after successful face recognition, allowing the student to verify their identity before final attendance is logged into the system**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/14 CONFIRM ITS YOU .png" width="900">
</p>

### **Fig-15 : Attendance data storage**

**Student attendance records stored in Google Sheets, including date-wise entries with student ID and department ID for further reporting and analysis**

<p align="center">
  <img src="IMAGES/01 WEBSITE IMAGES/15 ATTENDENCE STOTE IN G-SHEET .png" width="900">
</p>

## 🖼️ System Workflows Visualization

### Complete Student Registration Workflow
#### High Level Overview :

<p align="center">
<img src="IMAGES/00 DIAGRAM/01 STUDENT REGISTRATION PROCESS.png" width="900">
</p>


```
┌─────────────────────────────────────────────────────────────┐
│           STUDENT REGISTRATION DETAILED WORKFLOW                     │
└─────────────────────────────────────────────────────────────┘

STEP 1: Admin Opens Registration
└─→ Admin Dashboard → "Student Registration Management"
    └─→ Click "Open Registration Form"
        └─→ Updates app_controls.is_registration_open = TRUE
            └─→ Confirmation email sent to HODs

STEP 2: Students Fill Google Form
└─→ Students access registration link
    └─→ Fill: Name, Email, Phone, Address, Department, DOB
        └─→ Upload 3 facial photos (JPG/PNG)
            └─→ Form responses saved to Google Sheets
                └─→ All 3 photos stored with form row

STEP 3: Admin Reviews & Uploads
└─→ Admin checks "Student Registration Management"
    └─→ Click "View Pending Students" (from Google Sheet)
        └─→ Click "Upload Student Data"

STEP 4: Batch Processing
└─→ FOR each student in Google Sheet:
    │
    ├─ GENERATE Student ID: YYMMDD-0001 format
    │  └─ Today's date + sequential counter
    │     └─ Query Supabase for last ID todayto get counter
    │
    ├─ PROCESS Face Embeddings (3 photos):
    │  └─ For each photo:
    │     ├─ Download from Google Sheets
    │     ├─ Extract face with MTCNN (160x160 alignment)
    │     ├─ Generate 512-dim embedding with FaceNet
    │     └─ Create Qdrant point with student metadata
    │
    ├─ STORE in Supabase (RDB):
    │  └─ INSERT INTO students:
    │     ├─ s_id, s_name, s_mail, s_phone
    │     ├─ s_address, dep_id, s_admissionyear, s_dob
    │     └─ created_at = NOW()
    │
    ├─ STORE in Qdrant (VDB):
    │  └─ UPSERT 3 PointStruct objects:
    │     ├─ vector = embedding_vector (512-dim)
    │     ├─ payload.S_id = new_student_id
    │     └─ payload.S_name = student_name, etc.
    │
    └─ SEND Registration Email:
       └─ Template: "Welcome to Attendance System"
          ├─ Dear {Student Name},
          ├─ Your Student ID: {YYMMDD-0001}
          ├─ Username: {Email}
          ├─ First Attendance: {Link to app}
          └─ Signature: Attendance System Admin

STEP 5: Cleanup & Close
└─→ Admin clicks "Close Registration Form"
    └─→ Updates app_controls.is_registration_open = FALSE
        └─→ Clears Google Sheet (archives to backup)

COMPLETION
└─→ All students ready for attendance marking
    └─→ Embeddings indexed in Qdrant
        └─→ Real-time recognition ready
```

### Complete Attendance Marking Workflow
#### High Level Overview :

<p align="center">
<img src="IMAGES/00 DIAGRAM/02 GIVING ATTENDANCE PROCESS.png" width="900">
</p>

```
┌─────────────────────────────────────────────────────────────┐
│            ATTENDANCE MARKING DETAILED WORKFLOW             │
└─────────────────────────────────────────────────────────────┘

STEP 1: Student Initiates
└─→ Home Page → "Give Attendance"
    └─→ Browser prompts: "Allow camera access?"
        └─→ Student grants permission
            └─→ Streamlit camera widget loads

STEP 2: Capture Screenshot
└─→ Student clicks "Capture Image"
    └─→ Webcam frames streamed live
        └─→ Student positions face in center
            └─→ Click "Capture" button
                └─→ Image saved to memory (PIL Image)

STEP 3: Face Detection & Alignment
└─→ Process Image with MTCNN:
    ├─ Input: PIL Image (any resolution)
    ├─ Detect faces: (x, y, width, height, confidence)
    ├─ Check confidence > 0.95
    │
    ├─ IF no face:
    │  └─→ "No face detected. Please try again."
    │
    └─ IF face found:
       └─→ Align face to 160x160 (FaceNet standard)
           └─→ Continue to embedding generation

STEP 4: Generate Face Embedding
└─→ Process Aligned Face:
    ├─ Input: 160x160 RGB image
    ├─ Forward through FaceNet InceptionResNetV1
    ├─ Output: 512-dimensional embedding vector
    └─→ Normalize embedding

STEP 5: Search for Student (Vector Similarity)
└─→ Query Qdrant:
    ├─ vector = generated_embedding (512-dim)
    ├─ distance = COSINE (0.0 = same, 1.0 = opposite)
    ├─ score_threshold = 0.60
    ├─ limit = 1 (get best match)
    │
    ├─ Top Match Analysis:
    │  ├─ Match Score: 0.89 (89% similar)
    │  ├─ Student ID: 260401-0001
    │  ├─ Student Name: Rajesh Kumar
    │  └─ Department: CS-001
    │
    └─ Confidence Decision:
       ├─ IF score > 0.85: High confidence → Auto-confirm
       ├─ IF 0.70-0.85: Medium confidence → Show & ask
       └─ IF score < 0.60: NO MATCH → "Student not found"

STEP 6: Identity Confirmation
└─→ IF Medium Confidence:
    ├─ Show: "Is this you: Rajesh Kumar?"
    ├─ Display: Student photo (from registration)
    ├─ Buttons: "Yes, it's me" | "No, try again"
    │
    ├─ IF "Yes":
    │  └─→ Proceed to attendance logging
    │
    └─ IF "No":
       └─→ Return to capture stage

STEP 7: Duplicate Prevention Check
└─→ Query Google Sheet:
    ├─ Search: TODAY's date + student_id
    ├─ IF found:
    │  └─→ "Already marked attendance today!"
    │      └─→ Show previous mark time (10:30 AM)
    │          └─→ STOP (no duplicate marking)
    │
    └─ IF not found:
       └─→ Proceed to logging

STEP 8: Log Attendance
└─→ Prepare Record:
    ├─ date = TODAY (2025-04-01)
    ├─ Student_ID = 260401-0001
    ├─ Department_ID = CS-001
    ├─ timestamp = NOW() (UTC)
    └─ marking_time = current_time
    
└─→ Write to Google Sheet:
    ├─ sheet.append_row([date, student_id, dep_id])
    ├─ Transaction: Atomic (all or nothing)
    └─ Timestamp: Server-side for accuracy
    
└─→ Write to Databricks Bronze:
    ├─ Trigger ETL pipeline (async)
    └─ Silver/Gold layers updated (within hours)

STEP 9: Success Confirmation
└─→ Display: "✅ Attendance marked successfully!"
    ├─ Name: Rajesh Kumar
    ├─ Student ID: 260401-0001
    ├─ Marked At: 2025-04-01 10:30:45 AM
    └─ Message: "See you tomorrow!"

STEP 10: Log Trigger (Optional)
└─→ Databricks can query Google Sheet:
    ├─ Read new attendance records
    ├─ Append to Bronze layer table
    └─ Trigger silver/gold transformations

COMPLETION
└─→ Attendance saved with redundancy:
    ├─ Primary: Google Sheet (real-time view)
    ├─ Backup: Databricks Bronze (audit trail)
    └─→ HOD can see in report next day
```

### Report Generation Workflow



<p align="center">
<img src="IMAGES/00 DIAGRAM/06 GENERATION OF ATTENDENCE LIST.png" width="900">
</p>

```
┌─────────────────────────────────────────────────────────────┐
│          ATTENDANCE REPORT DETAILED WORKFLOW                         │
└─────────────────────────────────────────────────────────────┘

STEP 1: Admin Initiates Report
└─→ Admin Dashboard → "Attendance List & Reporting"
    └─→ Select: Start Date: 2025-04-01
                End Date: 2025-04-30

STEP 2: Calculate Working Days
└─→ Count working days (Mon-Fri):
    ├─ Exclude: Weekends
    ├─ Exclude: Public holidays (optional)
    ├─ Result: 20 working days (April 2025)
    └─→ Displ:ay calendar visualization

STEP 3: Select Departments
└─→ Checkbox list:
    ├─ ☑ Computer Science (CS-001)
    ├─ ☑ Information Technology (IT-001)
    ├─ ☑ Electronics (ECE-001)
    └─ Button: "Generate Report"

STEP 4: Query Attendance Data
└─→ Execute Databricks SQL:
    ├─ Query: college_dw.gold.fact_attendance
    ├─ WHERE attendance_date BETWEEN 2025-04-01 AND 2025-04-30
    ├─ GROUP BY department_id, student_id
    ├─ SELECT: COUNT(*) as present_days, percentage
    │
    └─ Result DataFrame:
       ┌────────┬──────────────┬──────────────┬────────┐
       │ dept   │  student_id  │ present_days │  pct   │
       ├────────┼──────────────┼──────────────┼────────┤
       │ CS-001 │ 260401-0001  │      18      │  90.0% │
       │ CS-001 │ 260401-0002  │      19      │  95.0% │
       │ CS-001 │ 260401-0003  │      17      │  85.0% │
       │ IT-001 │ 260401-0004  │      20      │ 100.0% │
       └────────┴──────────────┴──────────────┴────────┘

STEP 5: Prepare Report Content
└─→ FOR each department:
    ├─ Generate HTML template:
    │  ├─ Header: Department name, HOD name
    │  ├─ Period: April 1-30, 2025
    │  ├─ Working Days: 20
    │  └─ Table: Student attendance breakdown
    │
    └─ Calculate metrics:
       ├─ Dept Average: (90+95+85)/3 = 90.0%
       ├─ Total Students: 3
       ├─ Students < 75%: 0
       └─ Students < 90%: 1

STEP 6: Send via Email
└─→ FOR each department:
    ├─ TO: hod_email (dep_hod_mail from db)
    ├─ FROM: attendance-system@college.edu
    ├─ SUBJECT: "Attendance Report - April 2025"
    │
    ├─ EMAIL BODY (HTML):
    │  ┌───────────────────────────────────┐
    │  │ Attendance Report - April 2025    │
    │  │                                   │
    │  │ Department: Computer Science      │
    │  │ HOD: Dr. Raj Verma                │
    │  │ Period: April 1-30, 2025          │
    │  │ Working Days: 20                  │
    │  │ Reported: 2025-05-01 10:30 AM     │
    │  │                                   │
    │  │ Student Attendance:               │
    │  │ ──────────────────────────────────│
    │  │ ID        | Name      | Days | %  │
    │  │ 260401-01 | Rajesh   | 18   |90%  │
    │  │ 260401-02 | Priya    | 19   |95%  │
    │  │ 260401-03 | Arun     | 17   |85%  │
    │  │ ──────────────────────────────────│
    │  │ Department Average: 90.0%         │
    │  │                                   │
    │  │ Contact: admin@college.edu        │
    │  └───────────────────────────────────┘
    │
    ├─ PROTOCOL: SMTP (TLS on port 587)
    └─ STATUS: Sent ✓

STEP 7: Confirmation & Log
└─→ System displays:
    ├─ "✓ Report sent to 3 HODs"
    ├─ timestamp = 2025-05-01 10:30 AM
    └─ Audit log: Admin ID, action, department, timestamp

COMPLETION
└─→ HODs receive reports:
    ├─ Email in inbox (or spam folder!)
    ├─ Can view student attendance details
    ├─ Can identify students below 75%
    └─→ Can take follow-up actions
```


## 📊 Project Status

🚀 **Production Ready** - This project has been tested in live educational environments.

### Current Features
- ✅ Real-time facial recognition with 90%+ accuracy
- ✅ Multi-user admin panel with RBAC
- ✅ Department-wise student management
- ✅ Automated email notifications
- ✅ Google Sheets live logging
- ✅ Databricks data warehouse integration
- ✅ Department-wise attendance analytics
- ✅ Secure authentication via Supabase
- ✅ Vector database similarity search
- ✅ Batch student registration
- ✅ Attendance reports with percentages

### Roadmap


- [ ] Biometric integration (fingerprint, iris)
- [ ] Advanced analytics dashboard (Power BI / Tableau)
- [ ] Docker containerization
- [ ] Kubernetes deployment guide
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Blockchain audit trail (optional)

---

## 🤝 Contributing

Contributions are welcome! Process:

1. **Fork** the repository
2. **Create** feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** Pull Request with description

### Development Setup
```bash
git clone https://github.com/RpM-999/P14-Facial-Recognition-Based-Attendance-System
cd P14-Facial-Recognition-Based-Attendance-System
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

---

## 🙏 Acknowledgments

- **FaceNet**: Pre-trained facial recognition model by Google
- **Streamlit**: Amazing framework for data applications
- **Qdrant**: Efficient vector database for similarity search
- **Supabase**: PostgreSQL infrastructure and authentication
- **Databricks**: Data warehouse and analytics platform
- **Google**: Google Sheets API and cloud infrastructure
- **PyTorch**: Deep learning framework
- **MTCNN**: Face detection algorithm

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Terms
- ✅ You can use this project for educational purposes
- ✅ You can modify and distribute results
- ✅ You must include the license and copyright notice
- ❌ No warranty or liability provided

---

## 📧 Contact & Support

**Project Maintainer**: Rupam Mondal

- 📧 **Email**: rupam.mondal2022@uem.edu.in
- 🐙 **GitHub**: [LINK](https://github.com/RpM-999)
- 💼 **LinkedIn**: [Rupam Mondal](https://linkedin.com/in/rupam-mondal-data-science)

**Project Repository**: [GitHub](https://github.com/RpM-999/P14-Facial-Recognition-Based-Attendance-System)

### Support & Issues
- 📋 **Report Bugs**: GitHub Issues tab
- 💬 **Ask Questions**: GitHub Discussions
- 📚 **Documentation**: See LEARN.md (this file)
- 🔧 **Troubleshooting**: See Troubleshooting section above

---

## ⭐ Show Your Support

If you find this project helpful, please:
-  Give it a **GitHub ⭐**
-  **Fork** the repository
-  **Report issues** you encounter
-  **Suggest improvements**

Your support helps maintain and improve this project!

---

## 📝 Citation

If you use this project in academic work, please cite as:

```bibtex
@software{mondal2025facial,
  title = {Facial Recognition Based Attendance System},
  author = {Rupam Mondal},
  year = {2025-2026},
  url = {https://github.com/RpM-999/P14-Facial-Recognition-Based-Attendance-System},
  note = {Open-source educational attendance management system}
}
```

---

## 🔐 Security Notice

⚠️ **Important**: This project handles sensitive student data. Always:
- Use HTTPS in production
- Encrypt all sensitive data
- Follow GDPR compliance requirements
- Implement proper access controls
- Regular security audits
- Keep dependencies updated

See the Security section above for detailed recommendations.

---

**Last Updated**: April 3, 2026
**Project Status**: ✅ Active Development & Production Ready
**License**: MIT
**Python Version**: 3.8+
**Author**: Rupam Mondal (@RpM-999)

