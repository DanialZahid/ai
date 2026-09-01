"""Self-diagnostic checks shown on the System Status page. Purely
informational — nothing here blocks the rest of the app from being used."""

import os
import cv2

from config import DATASET_DIR, MODEL_PATH, ATTENDANCE_PATH
from core.detection import face_cascade
from core.labels import load_labels

STATUS_STYLE = {
    "ok": ("check_circle", "OK"),
    "warning": ("warning", "Warning"),
    "error": ("error", "Error"),
    "info": ("info", "Info"),
}


def get_status_checks():
    checks = []

    if face_cascade.empty():
        checks.append({
            "name": "Face Detection Engine",
            "status": "error",
            "detail": "The Haar Cascade face-detection file failed to load — face detection won't work.",
            "fix": "pip uninstall opencv-python opencv-contrib-python -y && pip install opencv-contrib-python==4.10.0.84"
        })
    else:
        checks.append({
            "name": "Face Detection Engine",
            "status": "ok",
            "detail": "Haar Cascade classifier loaded successfully.",
            "fix": None
        })

    if not hasattr(cv2, "face"):
        checks.append({
            "name": "Face Recognition Module",
            "status": "error",
            "detail": "cv2.face is missing — model training and recognition won't work.",
            "fix": "pip uninstall opencv-python opencv-contrib-python -y && pip install opencv-contrib-python==4.10.0.84"
        })
    else:
        checks.append({
            "name": "Face Recognition Module",
            "status": "ok",
            "detail": "LBPH recognizer module is available.",
            "fix": None
        })

    for label, folder in [
        ("Dataset Folder", DATASET_DIR),
        ("Data Folder", "data")
    ]:
        try:
            test_file = os.path.join(folder, ".write_test")

            with open(test_file, "w") as f:
                f.write("ok")

            os.remove(test_file)

            checks.append({
                "name": f"{label} ({folder}/)",
                "status": "ok",
                "detail": "Folder is writable.",
                "fix": None
            })

        except Exception:
            checks.append({
                "name": f"{label} ({folder}/)",
                "status": "error",
                "detail": f"Cannot write to '{folder}/'. Common on locked-down campus accounts.",
                "fix": "Run the app from a folder you fully own (e.g. Desktop), not a shared/managed drive."
            })

    labels = load_labels()

    if labels.empty:
        checks.append({
            "name": "Registered Students",
            "status": "warning",
            "detail": "No students registered yet.",
            "fix": "Go to 'Register Student' to add at least one before training."
        })
    else:
        checks.append({
            "name": "Registered Students",
            "status": "ok",
            "detail": f"{labels['name'].nunique()} student(s) registered.",
            "fix": None
        })

    if os.path.exists(MODEL_PATH):
        checks.append({
            "name": "Trained Model",
            "status": "ok",
            "detail": "A trained recognition model was found.",
            "fix": None
        })
    else:
        checks.append({
            "name": "Trained Model",
            "status": "warning",
            "detail": "No trained model found yet.",
            "fix": "Go to 'Train Model' after registering students."
        })

    if os.path.exists(ATTENDANCE_PATH):
        checks.append({
            "name": "Attendance Log",
            "status": "ok",
            "detail": "Attendance log file exists.",
            "fix": None
        })
    else:
        checks.append({
            "name": "Attendance Log",
            "status": "info",
            "detail": "No attendance recorded yet.",
            "fix": None
        })

    checks.append({
        "name": "Webcam Access",
        "status": "info",
        "detail": "Webcam capture runs through your browser, not this Python process, "
                  "so it can't be verified automatically here.",
        "fix": "If no camera permission prompt appears, check browser site settings, "
               "or use Upload Photo instead."
    })

    return checks
