
import streamlit as st
import requests
import re
import html
import base64

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"


# =========================================================
# SESSION STATE
# =========================================================

if "student_photos" not in st.session_state:
    st.session_state.student_photos = {}

if "editing_student_id" not in st.session_state:
    st.session_state.editing_student_id = None

if "editing_student_data" not in st.session_state:
    st.session_state.editing_student_data = None

if "registered_student" not in st.session_state:
    st.session_state.registered_student = None


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* Application background */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f7ff,
        #ffffff,
        #fdf2f8
    );
}

/* Main headings */
h1, h2, h3 {
    color: #312e81 !important;
    font-weight: 800 !important;
}

/* Main title */
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: #4338ca;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #475569 !important;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #312e81,
        #5b21b6,
        #7c3aed
    );
}

/* Sidebar text */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] small {
    color: #ffffff !important;
    opacity: 1 !important;
}

[data-testid="stSidebar"] h1 {
    font-size: 25px !important;
    font-weight: 900 !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #f5f3ff !important;
}

/* Sidebar radio */
[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255,255,255,0.08);
    border-radius: 9px;
    padding: 8px;
    margin-bottom: 5px;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.20);
}

/* Main application text */
.stApp p,
.stApp li,
.stApp [data-testid="stCaptionContainer"] {
    color: #334155;
}

/* Input labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stFileUploader label {
    color: #312e81 !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

/* Input fields */
.stTextInput input,
.stNumberInput input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    border: 1.5px solid #c7d2fe !important;
    border-radius: 10px !important;
    min-height: 43px;
}

/* Placeholder */
.stTextInput input::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* Input focus */
.stTextInput input:focus,
.stNumberInput input:focus {
    border: 2px solid #6366f1 !important;
    box-shadow: 0 0 0 3px #e0e7ff !important;
}

/* Select box */
.stSelectbox div[data-baseweb="select"] {
    background: #ffffff;
    border-radius: 10px;
}

/* Form */
div[data-testid="stForm"] {
    background: #ffffff !important;
    padding: 24px !important;
    border: 1px solid #e0e7ff !important;
    border-radius: 18px !important;
    box-shadow: 0 8px 25px rgba(79,70,229,0.08);
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(
        90deg,
        #4f46e5,
        #7c3aed
    ) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    min-height: 43px;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(
        90deg,
        #3730a3,
        #6d28d9
    ) !important;
    box-shadow: 0 5px 15px rgba(79,70,229,0.25);
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #ddd6fe;
    border-radius: 16px;
    padding: 20px 12px;
    text-align: center;
    box-shadow: 0 5px 18px rgba(79,70,229,0.08);
    margin-bottom: 15px;
}

.metric-icon {
    font-size: 28px;
}

.metric-value {
    font-size: 29px;
    font-weight: 900;
    color: #4f46e5;
}

.metric-label {
    font-size: 13px;
    color: #475569;
    font-weight: 600;
}

/* Form heading */
.form-heading {
    background: linear-gradient(
        90deg,
        #eef2ff,
        #faf5ff
    );
    border-left: 5px solid #6366f1;
    padding: 17px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.form-heading h2 {
    margin: 0;
    color: #312e81 !important;
}

.form-heading p {
    color: #475569 !important;
    margin: 6px 0 0 0;
}

/* Compact standard ID card */
.student-card {
    width: 100%;
    max-width: 330px;
    margin: 12px auto 22px auto;
    background: #ffffff;
    border: 1px solid #c7d2fe;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 5px 16px rgba(49,46,129,0.12);
    color: #1e293b;
}

/* ID card header */
.card-header {
    background: linear-gradient(
        120deg,
        #4338ca,
        #7c3aed
    );
    padding: 14px 10px;
    text-align: center;
}

.card-header h3 {
    color: #ffffff !important;
    margin: 0;
    font-size: 16px !important;
    line-height: 1.4;
}

.card-header p {
    color: #ffffff !important;
    margin: 6px 0 0 0;
    font-size: 9px;
    letter-spacing: 1px;
}

/* ID card body */
.card-body {
    padding: 16px 14px;
}

/* Student photograph */
.student-photo {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #a5b4fc;
    display: block;
    margin: 0 auto 12px auto;
}

/* Default avatar */
.avatar {
    width: 88px;
    height: 88px;
    border-radius: 50%;
    background: #ede9fe;
    border: 3px solid #c4b5fd;
    color: #5b21b6;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 32px;
    font-weight: 900;
    margin: 0 auto 12px auto;
}

/* Student name */
.student-name {
    text-align: center;
    font-size: 19px;
    line-height: 1.4;
    font-weight: 900;
    color: #312e81;
    overflow-wrap: anywhere;
    margin-bottom: 5px;
}

/* Student course */
.student-course {
    text-align: center;
    color: #6d28d9;
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 14px;
    overflow-wrap: anywhere;
}

/* Student details */
.info-row {
    padding: 9px;
    margin-bottom: 7px;
    border-radius: 8px;
    background: #f1f5f9;
    color: #1e293b !important;
    font-size: 12px;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

/* ID card footer */
.card-footer {
    text-align: center;
    background: #ede9fe;
    color: #4338ca !important;
    padding: 11px 8px;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 0.5px;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #f8faff;
    border: 1px dashed #a5b4fc;
    border-radius: 12px;
    padding: 10px;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# API FUNCTIONS
# =========================================================

def get_students():
    try:
        response = requests.get(
            f"{API_URL}/students",
            timeout=5
        )

        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            return data, None

        return None, "Unexpected response received from API."

    except requests.exceptions.RequestException:
        return None, (
            "Backend disconnected. Please start FastAPI first "
            "and check that the API URL is correct."
        )

    except ValueError:
        return None, "The API returned an invalid response."


def get_student(student_id):
    try:
        response = requests.get(
            f"{API_URL}/students/{student_id}",
            timeout=5
        )

        if response.status_code == 404:
            return None, "Student not found."

        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and "data" in result:
            return result["data"], None

        return result, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to FastAPI."

    except ValueError:
        return None, "The API returned an invalid response."


def create_student(data):
    try:
        # Photo is kept separately; only student fields go to the API.
        api_data = {
            key: value
            for key, value in data.items()
            if key != "photo"
        }

        response = requests.post(
            f"{API_URL}/students",
            json=api_data,
            timeout=10
        )

        if response.status_code not in (200, 201):
            return None, (
                f"API Error ({response.status_code}): "
                f"{response.text}"
            )

        result = response.json()

        if isinstance(result, dict) and "data" in result:
            student = result["data"]
        else:
            student = result

        if not isinstance(student, dict):
            return None, "Unexpected registration response from API."

        student_id = result.get("id", student.get("id"))

        if student_id is None:
            return None, (
                "Student may have been registered, but the API "
                "did not return a student ID. Check your FastAPI response."
            )

        return {
            "id": student_id,
            "data": student
        }, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to FastAPI."

    except ValueError:
        return None, "The API returned an invalid response."


def update_student(student_id, data):
    try:
        api_data = {
            key: value
            for key, value in data.items()
            if key != "photo"
        }

        response = requests.put(
            f"{API_URL}/students/{student_id}",
            json=api_data,
            timeout=10
        )

        if response.status_code != 200:
            return None, (
                f"API Error ({response.status_code}): "
                f"{response.text}"
            )

        result = response.json()

        if isinstance(result, dict) and "data" in result:
            student = result["data"]
        else:
            student = result

        return {
            "id": student_id,
            "data": student
        }, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to FastAPI."

    except ValueError:
        return None, "The API returned an invalid response."


def delete_student(student_id):
    try:
        response = requests.delete(
            f"{API_URL}/students/{student_id}",
            timeout=10
        )

        if response.status_code not in (200, 204):
            return None, (
                f"API Error ({response.status_code}): "
                f"{response.text}"
            )

        if response.status_code == 204 or not response.text.strip():
            result = {"message": "Student deleted successfully."}
        else:
            result = response.json()

        return result, None

    except requests.exceptions.RequestException:
        return None, "Unable to connect to FastAPI."

    except ValueError:
        return {"message": "Student deleted successfully."}, None


# =========================================================
# VALIDATION
# =========================================================

def validate_student(name, age, course, email, phone):
    name = name.strip()
    course = course.strip()
    email = email.strip()
    phone = phone.strip()

    if not 2 <= len(name) <= 50:
        return "Name must contain 2 to 50 characters."

    if not 1 <= age <= 99:
        return "Age must be between 1 and 99."

    if not 2 <= len(course) <= 50:
        return "Course must contain 2 to 50 characters."

    if not 5 <= len(email) <= 100:
        return "Email must contain 5 to 100 characters."

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        return "Please enter a valid email address."

    if not re.fullmatch(r"[0-9]{10}", phone):
        return "Phone number must contain exactly 10 digits."

    return None


# =========================================================
# STUDENT PHOTO HELPERS
# =========================================================

def save_student_photo(student_id, photo_bytes):
    if photo_bytes:
        st.session_state.student_photos[str(student_id)] = (
            photo_bytes
        )


def get_student_photo(student_id):
    return st.session_state.student_photos.get(
        str(student_id)
    )


# =========================================================
# STUDENT ID CARD
# =========================================================

def show_student_card(student, student_id):

    if not isinstance(student, dict):
        st.warning("Student details are unavailable.")
        return

    name = html.escape(str(student.get("name", "Student")))
    age = html.escape(str(student.get("age", "N/A")))
    course = html.escape(str(student.get("course", "N/A")))
    email = html.escape(str(student.get("email", "N/A")))
    phone = html.escape(str(student.get("phone", "N/A")))
    sid = html.escape(str(student_id))

    initial = name[0].upper() if name else "S"

    photo_bytes = get_student_photo(student_id)

    if photo_bytes:
        encoded_photo = base64.b64encode(
            photo_bytes
        ).decode("utf-8")

        photo_type = "image/jpeg"

        if photo_bytes[:8] == b"\x89PNG\r\n\x1a\n":
            photo_type = "image/png"

        photo_html = f"""
            <img
                class="student-photo"
                src="data:{photo_type};base64,{encoded_photo}"
                alt="Student Photo"
            />
        """
    else:
        photo_html = f"""
            <div class="avatar">{initial}</div>
        """

    card_html = f"""
    <div class="student-card">

        <div class="card-header">
            <h3>🎓 STUDENT ID CARD</h3>
            <p>STUDENT MANAGEMENT SYSTEM</p>
        </div>

        <div class="card-body">

            {photo_html}

            <div class="student-name">{name}</div>

            <div class="student-course">{course}</div>

            <div class="info-row">
                🆔 <b>Student ID:</b> {sid}
            </div>

            <div class="info-row">
                🎂 <b>Age:</b> {age} years
            </div>

            <div class="info-row">
                📧 <b>Email:</b> {email}
            </div>

            <div class="info-row">
                📱 <b>Phone:</b> {phone}
            </div>

        </div>

        <div class="card-footer">
            ✔ REGISTERED STUDENT
        </div>

    </div>
    """

    st.html(card_html)


# =========================================================
# STUDENT FORM
# =========================================================

def student_form(default=None, key_prefix="student"):

    if default is None:
        default = {}

    with st.form(f"{key_prefix}_form"):

        st.markdown("### 👤 Personal Information")

        st.caption(
            "Enter the student's details in the fields below."
        )

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "👤 Student Full Name *",
                value=str(default.get("name", "")),
                placeholder="Example: Anjali Sharma",
                max_chars=50,
                key=f"{key_prefix}_name"
            )

            age = st.number_input(
                "🎂 Student Age *",
                min_value=1,
                max_value=99,
                value=min(
                    max(int(default.get("age", 18)), 1),
                    99
                ),
                key=f"{key_prefix}_age"
            )

            course = st.text_input(
                "📚 Course Name *",
                value=str(default.get("course", "")),
                placeholder="Example: B.Tech CSE",
                max_chars=50,
                key=f"{key_prefix}_course"
            )

        with col2:

            email = st.text_input(
                "📧 Email Address *",
                value=str(default.get("email", "")),
                placeholder="Example: student@gmail.com",
                max_chars=100,
                key=f"{key_prefix}_email"
            )

            phone = st.text_input(
                "📱 Mobile Number *",
                value=str(default.get("phone", "")),
                placeholder="Enter 10-digit mobile number",
                max_chars=10,
                key=f"{key_prefix}_phone"
            )

        st.markdown("### 📸 Student Photograph")

        uploaded_photo = st.file_uploader(
            "Upload Student Photo",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear JPG or PNG photograph.",
            key=f"{key_prefix}_photo"
        )

        st.caption("* All fields are mandatory.")

        submitted = st.form_submit_button(
            "💾 Save Student Details",
            use_container_width=True
        )

    if submitted:

        error = validate_student(
            name,
            age,
            course,
            email,
            phone
        )

        if error:
            st.error(error)
            return None

        photo_bytes = None

        if uploaded_photo is not None:
            photo_bytes = uploaded_photo.getvalue()

        return {
            "name": name.strip(),
            "age": int(age),
            "course": course.strip(),
            "email": email.strip(),
            "phone": phone.strip(),
            "photo": photo_bytes
        }

    return None


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown("# 🎓 Student Portal")
st.sidebar.caption("Smart Student Management")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "🏠 Dashboard",
        "➕ Register Student",
        "🪪 Student ID Cards",
        "🔍 Search Student",
        "✏️ Update Student",
        "🗑️ Delete Student"
    ],
    key="selected_page"
)

st.sidebar.markdown("---")
st.sidebar.caption("Powered by FastAPI + Streamlit")

if st.sidebar.button(
    "🔄 Refresh Data",
    use_container_width=True
):
    st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🎓 Student Management System
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Register students, manage records and create
        colourful digital ID cards.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    students, error = get_students()

    if error:
        st.error(error)
        st.info(
            "Start the FastAPI backend in another terminal."
        )
        st.code("uvicorn main:app --reload")
        st.stop()

    total = len(students)

    courses = {
        data.get("course", "")
        for data in students.values()
        if isinstance(data, dict)
    }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">👨‍🎓</div>
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Students</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-icon">📚</div>
                <div class="metric-value">
                    {len(courses) if total else 0}
                </div>
                <div class="metric-label">Different Courses</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-icon">🟢</div>
                <div class="metric-value">LIVE</div>
                <div class="metric-label">API Connection</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 🌟 Registered Students")

    if not students:
        st.info(
            "No students registered yet. "
            "Open Register Student to begin."
        )

    else:
        recent = list(students.items())[::-1][:6]

        columns = st.columns(3)

        for index, (student_id, data) in enumerate(recent):

            with columns[index % 3]:
                show_student_card(data, student_id)


# =========================================================
# REGISTER STUDENT
# =========================================================

elif page == "➕ Register Student":

    st.markdown(
        """
        <div class="form-heading">
            <h2>🎓 Student Registration Form</h2>
            <p>
                Complete the required fields and upload
                a student photograph.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "📌 Enter the correct student details. "
        "All personal information fields are mandatory."
    )

    student_data = student_form(
        key_prefix="register"
    )

    if student_data is not None:

        result, error = create_student(student_data)

        if error:
            st.error(error)

        else:
            student_id = result["id"]
            student_details = result["data"]

            save_student_photo(
                student_id,
                student_data.get("photo")
            )

            st.session_state.registered_student = {
                "id": student_id,
                "data": student_details
            }

            st.success(
                f"🎉 {student_details.get('name', 'Student')} "
                "registered successfully!"
            )

            st.balloons()

            st.markdown("## 🪪 Student ID Card")

            show_student_card(
                student_details,
                student_id
            )


# =========================================================
# STUDENT ID CARDS
# =========================================================

elif page == "🪪 Student ID Cards":

    st.markdown("## 🪪 Student Identity Cards")

    students, error = get_students()

    if error:
        st.error(error)

    elif not students:
        st.info("No students registered yet.")

    else:
        search_text = st.text_input(
            "🔍 Search by student name or course",
            placeholder="Type a name or course"
        ).strip().lower()

        filtered = [
            (sid, data)
            for sid, data in students.items()
            if isinstance(data, dict)
            and (
                search_text in str(
                    data.get("name", "")
                ).lower()
                or search_text in str(
                    data.get("course", "")
                ).lower()
            )
        ]

        if not filtered:
            st.warning("No matching students found.")

        else:
            columns = st.columns(3)

            for index, (sid, data) in enumerate(filtered):

                with columns[index % 3]:
                    show_student_card(data, sid)


# =========================================================
# SEARCH STUDENT
# =========================================================

elif page == "🔍 Search Student":

    st.markdown("## 🔍 Search Student")

    st.caption(
        "Enter the ID assigned to the student during registration."
    )

    with st.form("search_form"):

        student_id = st.number_input(
            "🆔 Student ID",
            min_value=1,
            step=1
        )

        search_button = st.form_submit_button(
            "🔎 Find Student",
            use_container_width=True
        )

    if search_button:

        student, error = get_student(int(student_id))

        if error:
            st.error(error)

        else:
            st.success("Student record found!")

            show_student_card(
                student,
                int(student_id)
            )


# =========================================================
# UPDATE STUDENT
# =========================================================

elif page == "✏️ Update Student":

    st.markdown("## ✏️ Update Student Information")

    st.caption(
        "Load an existing student record before editing."
    )

    with st.form("load_student_form"):

        update_id = st.number_input(
            "🆔 Student ID to Update",
            min_value=1,
            step=1
        )

        load_button = st.form_submit_button(
            "📥 Load Student Details",
            use_container_width=True
        )

    if load_button:

        student, error = get_student(int(update_id))

        if error:
            st.error(error)

        else:
            st.session_state.editing_student_id = int(
                update_id
            )

            st.session_state.editing_student_data = student

    current_id = st.session_state.editing_student_id
    current_data = st.session_state.editing_student_data

    if current_id is not None and current_data is not None:

        st.markdown("### 📝 Edit Student Details")

        updated_data = student_form(
            default=current_data,
            key_prefix=f"edit_{current_id}"
        )

        if updated_data is not None:

            result, error = update_student(
                current_id,
                updated_data
            )

            if error:
                st.error(error)

            else:
                if updated_data.get("photo") is not None:
                    save_student_photo(
                        current_id,
                        updated_data["photo"]
                    )

                st.success(
                    "Student updated successfully! 🎉"
                )

                st.balloons()

                st.session_state.editing_student_data = (
                    result["data"]
                )

                show_student_card(
                    result["data"],
                    current_id
                )


# =========================================================
# DELETE STUDENT
# =========================================================

elif page == "🗑️ Delete Student":

    st.markdown("## 🗑️ Delete Student Record")

    st.warning(
        "⚠️ Deleting a student removes their record "
        "from the current backend storage."
    )

    with st.form("delete_student_form"):

        student_id = st.number_input(
            "🆔 Student ID to Delete",
            min_value=1,
            step=1
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        delete_button = st.form_submit_button(
            "🗑️ Delete Student",
            use_container_width=True
        )

    if delete_button:

        if not confirm:
            st.warning("Please confirm before deleting.")

        else:
            result, error = delete_student(
                int(student_id)
            )

            if error:
                st.error(error)

            else:
                st.session_state.student_photos.pop(
                    str(int(student_id)),
                    None
                )

                if (
                    st.session_state.editing_student_id
                    == int(student_id)
                ):
                    st.session_state.editing_student_id = None
                    st.session_state.editing_student_data = None

                st.success("Student deleted successfully!")

                st.toast(
                    "Student record deleted.",
                    icon="✅"
                )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <p style="
        text-align:center;
        color:#475569;
        font-weight:600;
    ">
        🎓 Student Management System |
        Built with FastAPI + Streamlit
    </p>
    """,
    unsafe_allow_html=True
)

