import streamlit as st
import cv2
import numpy as np
import pandas as pd
import os
from datetime import date, datetime
from PIL import Image

DATASET_DIR = "dataset"
MODEL_PATH = "data/trainer.yml"
LABELS_PATH = "data/labels.csv"
ATTENDANCE_PATH = "data/attendance.csv"

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def detect_face_gray(image_pil):
    """Convert PIL image to grayscale numpy, detect largest face, return cropped face or None."""
    img = np.array(image_pil.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    if len(faces) == 0:
        return None
    # pick largest face
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    return cv2.resize(gray[y:y + h, x:x + w], (200, 200))


def load_labels():
    if os.path.exists(LABELS_PATH):
        return pd.read_csv(LABELS_PATH)
    return pd.DataFrame(columns=["id", "name"])


def save_labels(df):
    df.to_csv(LABELS_PATH, index=False)


st.title("Smart Face Attendance System")
mode = st.sidebar.radio("Choose action", ["Register Student", "Train Model", "Take Attendance", "View Attendance"])

# Register Student
if mode == "Register Student":
    st.header("Register a New Student")
    name = st.text_input("Student name")
    photo = st.camera_input("Capture face")

    if photo and name:
        face = detect_face_gray(Image.open(photo))
        if face is None:
            st.error("No face detected. Try again with better lighting/angle.")
        else:
            labels = load_labels()
            if name in labels["name"].values:
                student_id = labels[labels["name"] == name]["id"].values[0]
            else:
                student_id = len(labels)
                labels = pd.concat([labels, pd.DataFrame([{"id": student_id, "name": name}])], ignore_index=True)
                save_labels(labels)

            student_dir = os.path.join(DATASET_DIR, str(student_id))
            os.makedirs(student_dir, exist_ok=True)
            count = len(os.listdir(student_dir))
            cv2.imwrite(os.path.join(student_dir, f"{count}.jpg"), face)
            st.success(f"Saved photo #{count + 1} for {name}. Capture 3-5 photos from different angles for best accuracy.")

# Train Model
elif mode == "Train Model":
    st.header("Train Recognition Model")
    st.write("Run this after registering all students (or whenever you add someone new).")

    if st.button("Train Now"):
        labels = load_labels()
        if labels.empty:
            st.error("No students registered yet.")
        else:
            faces, ids = [], []
            for _, row in labels.iterrows():
                student_dir = os.path.join(DATASET_DIR, str(row["id"]))
                if not os.path.isdir(student_dir):
                    continue
                for fname in os.listdir(student_dir):
                    img = cv2.imread(os.path.join(student_dir, fname), cv2.IMREAD_GRAYSCALE)
                    faces.append(img)
                    ids.append(int(row["id"]))

            if len(faces) == 0:
                st.error("No training images found.")
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.train(faces, np.array(ids))
                recognizer.save(MODEL_PATH)
                st.success(f"Model trained on {len(faces)} images from {labels['name'].nunique()} students.")

# Take Attendance
elif mode == "Take Attendance":
    st.header("Mark Attendance")

    if not os.path.exists(MODEL_PATH):
        st.error("No trained model found. Register students and train the model first.")
    else:
        photo = st.camera_input("Look at the camera")
        if photo:
            face = detect_face_gray(Image.open(photo))
            if face is None:
                st.error("No face detected. Try again.")
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(MODEL_PATH)
                label_id, confidence = recognizer.predict(face)
                # LBPH: lower confidence = better match. ~<70 is usually a reliable match.
                labels = load_labels()
                match = labels[labels["id"] == label_id]

                if confidence < 70 and not match.empty:
                    name = match["name"].values[0]
                    st.success(f"Recognized: {name} (confidence score: {confidence:.1f})")

                    today = str(date.today())
                    if os.path.exists(ATTENDANCE_PATH):
                        att = pd.read_csv(ATTENDANCE_PATH)
                    else:
                        att = pd.DataFrame(columns=["name", "date", "time"])

                    already_marked = ((att["name"] == name) & (att["date"] == today)).any()
                    if already_marked:
                        st.info(f"{name} is already marked present today.")
                    else:
                        new_row = {"name": name, "date": today, "time": datetime.now().strftime("%H:%M:%S")}
                        att = pd.concat([att, pd.DataFrame([new_row])], ignore_index=True)
                        att.to_csv(ATTENDANCE_PATH, index=False)
                        st.success(f"Attendance marked for {name}.")
                else:
                    st.error(f"Face not recognized (confidence score: {confidence:.1f}). Try again or register this student.")

# View Attendance
elif mode == "View Attendance":
    st.header("Attendance Log")
    if os.path.exists(ATTENDANCE_PATH):
        df = pd.read_csv(ATTENDANCE_PATH)
        st.dataframe(df.sort_values(["date", "time"], ascending=False), use_container_width=True)
    else:
        st.info("No attendance recorded yet.")
