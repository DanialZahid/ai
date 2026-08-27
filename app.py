import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Smart Face Attendance",
    page_icon="📷",
    layout="wide",
)

# ============================================================
# PURPLE + WHITE UI
# ============================================================

st.markdown(
    """
    <style>
    /* Main page */
    .stApp {
        background-color: #f8f6fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #54257f 0%,
            #6f3fa3 55%,
            #8555b5 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar heading */
    .sidebar-title {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        padding: 18px 5px 5px 5px;
    }

    .sidebar-subtitle {
        text-align: center;
        font-size: 12px;
        opacity: 0.85;
        margin-bottom: 25px;
    }

    /* Main title */
    .page-title {
        color: #54257f;
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .page-subtitle {
        color: #777777;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* White content card */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 5px 20px rgba(84, 37, 127, 0.10);
        margin-bottom: 20px;
    }

    /* Section heading */
    .section-title {
        color: #54257f;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #6f3fa3;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 25px;
    }

    .stButton > button:hover {
        background-color: #54257f;
        color: white;
    }

    /* Text input */
    div[data-baseweb="input"] {
        border-radius: 10px;
    }

    /* Camera */
    div[data-testid="stCameraInput"] {
        border-radius: 15px;
        overflow: hidden;
    }

    /* Success */
    .success-card {
        background-color: #edf8f0;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 10px;
        color: #236b38;
    }

    /* Info */
    .info-card {
        background-color: #f3edfa;
        border-left: 5px solid #6f3fa3;
        padding: 15px;
        border-radius: 10px;
        color: #54257f;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #999999;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# FILE PATHS
# ============================================================

DATASET_DIR = "dataset"
MODEL_PATH = "data/trainer.yml"
LABELS_PATH = "data/labels.csv"
ATTENDANCE_PATH = "data/attendance.csv"

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

if "show_status" not in st.session_state:
    st.session_state.show_status = False

# ============================================================
# FACE CASCADE
# ============================================================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ============================================================
# FACE DETECTION
# ============================================================


def detect_face_gray(image_pil):
    """Convert PIL image to grayscale numpy,
    detect largest face, return cropped face or None.
    """

    img = np.array(image_pil.convert("RGB"))

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
    )

    if len(faces) == 0:
        return None

    # Pick largest face
    x, y, w, h = max(
        faces,
        key=lambda f: f[2] * f[3],
    )

    return cv2.resize(
        gray[y : y + h, x : x + w],
        (200, 200),
    )


# ============================================================
# LABEL FUNCTIONS
# ============================================================


def load_labels():
    if os.path.exists(LABELS_PATH):
        return pd.read_csv(LABELS_PATH)

    return pd.DataFrame(columns=["id", "name"])


def save_labels(df):
    df.to_csv(LABELS_PATH, index=False)


# ============================================================
# SYSTEM STATUS
# ============================================================
STATUS_STYLE = {
    "ok": ("✅", "OK"),
    "warning": ("⚠️", "Warning"),
    "error": ("❌", "Error"),
    "info": ("ℹ️", "Info"),
}

def get_status_checks():
    checks = []

    if face_cascade.empty():
        checks.append({"name": "Face Detection Engine", "status": "error",
            "detail": "The Haar Cascade face-detection file failed to load — face detection won't work.",
            "fix": "pip uninstall opencv-python opencv-contrib-python -y && pip install opencv-contrib-python==4.10.0.84"})
    else:
        checks.append({"name": "Face Detection Engine", "status": "ok",
            "detail": "Haar Cascade classifier loaded successfully.", "fix": None})

    if not hasattr(cv2, "face"):
        checks.append({"name": "Face Recognition Module", "status": "error",
            "detail": "cv2.face is missing — model training and recognition won't work.",
            "fix": "pip uninstall opencv-python opencv-contrib-python -y && pip install opencv-contrib-python==4.10.0.84"})
    else:
        checks.append({"name": "Face Recognition Module", "status": "ok",
            "detail": "LBPH recognizer module is available.", "fix": None})

    for label, folder in [("Dataset Folder", DATASET_DIR), ("Data Folder", "data")]:
        try:
            test_file = os.path.join(folder, ".write_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            checks.append({"name": f"{label} ({folder}/)", "status": "ok",
                "detail": "Folder is writable.", "fix": None})
        except Exception:
            checks.append({"name": f"{label} ({folder}/)", "status": "error",
                "detail": f"Cannot write to '{folder}/'. Common on locked-down campus accounts.",
                "fix": "Run the app from a folder you fully own (e.g. Desktop), not a shared/managed drive."})

    labels = load_labels()
    if labels.empty:
        checks.append({"name": "Registered Students", "status": "warning",
            "detail": "No students registered yet.",
            "fix": "Go to 'Register Student' to add at least one before training."})
    else:
        checks.append({"name": "Registered Students", "status": "ok",
            "detail": f"{labels['name'].nunique()} student(s) registered.", "fix": None})

    if os.path.exists(MODEL_PATH):
        checks.append({"name": "Trained Model", "status": "ok",
            "detail": "A trained recognition model was found.", "fix": None})
    else:
        checks.append({"name": "Trained Model", "status": "warning",
            "detail": "No trained model found yet.",
            "fix": "Go to 'Train Model' after registering students."})

    if os.path.exists(ATTENDANCE_PATH):
        checks.append({"name": "Attendance Log", "status": "ok",
            "detail": "Attendance log file exists.", "fix": None})
    else:
        checks.append({"name": "Attendance Log", "status": "info",
            "detail": "No attendance recorded yet.", "fix": None})

    checks.append({"name": "Webcam Access", "status": "info",
        "detail": "Webcam capture runs through your browser, not this Python process, "
                  "so it can't be verified automatically here.",
        "fix": "If no camera permission prompt appears, check browser site settings, "
               "or use Upload Photo instead."})

    return checks


def render_status_page():
    st.markdown(
        '<div class="card"><div class="section-title">🩺 System Status</div>'
        '<p style="color:#777;">Live check of the app\'s setup — for troubleshooting only. '
        'Nothing here blocks you from using the app.</p></div>',
        unsafe_allow_html=True
    )
    for check in get_status_checks():
        icon, label_text = STATUS_STYLE[check["status"]]
        with st.expander(f"{icon} {check['name']} — {label_text}"):
            st.write(check["detail"])
            if check["fix"]:
                st.markdown(f"**Suggested fix:** {check['fix']}")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">'
        "📷 SMART ATTENDANCE"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        "AI-Based Student Attendance System"
        "</div>",
        unsafe_allow_html=True,
    )

    def _go_to_nav():
        st.session_state.show_status = False

    mode = st.radio(
        "Choose action",
        [
            "👤 Register Student",
            "🧠 Train Model",
            "📸 Take Attendance",
            "📊 View Attendance"
        ],
        label_visibility="collapsed",
        key="nav_mode",
        on_change=_go_to_nav
    )

    st.markdown("---")
    _issues = sum(1 for c in get_status_checks() if c["status"] in ("warning", "error"))
    _status_label = "🩺 System Status" + (f" ({_issues})" if _issues else "")

    if st.button(_status_label, use_container_width=True):
        st.session_state.show_status = True


# ============================================================
# TOP TITLE
# ============================================================

st.markdown(
    '<div class="page-title">'
    "📷 Smart Face Attendance System"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    "AI-powered student attendance management"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# REGISTER STUDENT
# ============================================================

if st.session_state.show_status:
    render_status_page()
elif mode == "👤 Register Student":
    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        "📝 Register a New Student"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        name = st.text_input("Student name")

        st.markdown(
            '<div class="info-card">'
            "💡 Capture 3-5 photos from different "
            "angles for better accuracy."
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        photo = st.camera_input("📸 Capture face")

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if photo and name:
        face = detect_face_gray(Image.open(photo))

        if face is None:
            st.error(
                "No face detected. "
                "Try again with better lighting/angle."
            )

        else:
            labels = load_labels()

            if name in labels["name"].values:
                student_id = labels[
                    labels["name"] == name
                ]["id"].values[0]

            else:
                student_id = len(labels)

                labels = pd.concat(
                    [
                        labels,
                        pd.DataFrame(
                            [
                                {
                                    "id": student_id,
                                    "name": name,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )

            save_labels(labels)

            student_dir = os.path.join(
                DATASET_DIR,
                str(student_id),
            )

            os.makedirs(
                student_dir,
                exist_ok=True,
            )

            count = len(os.listdir(student_dir))

            cv2.imwrite(
                os.path.join(
                    student_dir,
                    f"{count}.jpg",
                ),
                face,
            )

            st.success(
                f"Saved photo #{count + 1} for {name}. "
                f"Capture 3-5 photos from different angles "
                f"for best accuracy."
            )


# ============================================================
# TRAIN MODEL
# ============================================================

elif mode == "🧠 Train Model":
    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        "🧠 Train Recognition Model"
        "</div>"
        '<p style="color:#777;">'
        "Run this after registering all students "
        "(or whenever you add someone new)."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("🧠 Train Now"):
        labels = load_labels()

        if labels.empty:
            st.error("No students registered yet.")

        else:
            faces = []
            ids = []

            for _, row in labels.iterrows():
                student_dir = os.path.join(
                    DATASET_DIR,
                    str(row["id"]),
                )

                if not os.path.isdir(student_dir):
                    continue

                for fname in os.listdir(student_dir):
                    img = cv2.imread(
                        os.path.join(
                            student_dir,
                            fname,
                        ),
                        cv2.IMREAD_GRAYSCALE,
                    )

                    if img is None:
                        continue

                    faces.append(img)
                    ids.append(int(row["id"]))

            if len(faces) == 0:
                st.error("No training images found.")

            else:
                recognizer = (
                    cv2.face.LBPHFaceRecognizer_create()
                )

                recognizer.train(
                    faces,
                    np.array(ids),
                )

                recognizer.save(MODEL_PATH)

                st.success(
                    f"Model trained on {len(faces)} "
                    f"images from "
                    f"{labels['name'].nunique()} students."
                )


# ============================================================
# TAKE ATTENDANCE
# ============================================================

elif mode == "📸 Take Attendance":
    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        "📸 Mark Attendance"
        "</div>"
        '<p style="color:#777;">'
        "Look directly at the camera to recognize the student."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if not os.path.exists(MODEL_PATH):
        st.error(
            "No trained model found. "
            "Register students and train the model first."
        )

    else:
        photo = st.camera_input("📸 Look at the camera")

        if photo:
            face = detect_face_gray(Image.open(photo))

            if face is None:
                st.error("No face detected. Try again.")

            else:
                recognizer = (
                    cv2.face.LBPHFaceRecognizer_create()
                )

                recognizer.read(MODEL_PATH)

                label_id, confidence = recognizer.predict(face)

                labels = load_labels()

                match = labels[
                    labels["id"] == label_id
                ]

                # LBPH: lower confidence = better match
                if confidence < 70 and not match.empty:
                    name = match["name"].values[0]

                    st.success(
                        f"Recognized: {name} "
                        f"(confidence score: "
                        f"{confidence:.1f})"
                    )

                    today = str(date.today())

                    if os.path.exists(ATTENDANCE_PATH):
                        att = pd.read_csv(ATTENDANCE_PATH)

                    else:
                        att = pd.DataFrame(
                            columns=[
                                "name",
                                "date",
                                "time",
                            ]
                        )

                    already_marked = (
                        (att["name"] == name)
                        & (att["date"] == today)
                    ).any()

                    if already_marked:
                        st.info(
                            f"{name} is already "
                            "marked present today."
                        )

                    else:
                        new_row = {
                            "name": name,
                            "date": today,
                            "time": datetime.now().strftime(
                                "%H:%M:%S"
                            ),
                        }

                        att = pd.concat(
                            [
                                att,
                                pd.DataFrame([new_row]),
                            ],
                            ignore_index=True,
                        )

                        att.to_csv(
                            ATTENDANCE_PATH,
                            index=False,
                        )

                        st.success(
                            f"Attendance marked for {name}."
                        )

                else:
                    st.error(
                        f"Face not recognized "
                        f"(confidence score: "
                        f"{confidence:.1f}). "
                        f"Try again or register this student."
                    )


# ============================================================
# VIEW ATTENDANCE
# ============================================================

elif mode == "📊 View Attendance":
    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        "📊 Attendance Log"
        "</div>"
        '<p style="color:#777;">'
        "View all recorded student attendance."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if os.path.exists(ATTENDANCE_PATH):
        df = pd.read_csv(ATTENDANCE_PATH)

        st.dataframe(
            df.sort_values(
                ["date", "time"],
                ascending=False,
            ),
            use_container_width=True,
        )

    else:
        st.info("No attendance recorded yet.")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    "📷 Smart Face Attendance System "
    "• AI & Computer Vision"
    "</div>",
    unsafe_allow_html=True,
)
