"""Take Attendance screen."""

import os
import streamlit as st
import pandas as pd
import cv2
from datetime import date, datetime
from PIL import Image

from config import MODEL_PATH, ATTENDANCE_PATH, RECOGNITION_THRESHOLD
from core.detection import detect_face_gray
from core.labels import load_labels, get_student_photo, get_student_id_by_name
from styles import ICON_VIEWFINDER
from ui.components import get_photo


def render_attendance_page():

    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        f"{ICON_VIEWFINDER}Mark Attendance"
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

        photo = get_photo("Look at the camera", "attendance")

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

                # LBPH: lower confidence = better match. This threshold is a
                # tuned default, not a guarantee — recognition reliability
                # depends heavily on registering 3-5 varied photos per
                # student (see Register Student). The exact confidence
                # value is logged to the console below for debugging,
                # rather than shown in the UI.
                print(
                    f"[Take Attendance] predicted label_id={label_id}, "
                    f"confidence={confidence:.1f}, "
                    f"threshold={RECOGNITION_THRESHOLD}, "
                    f"matched_name={match['name'].values[0] if not match.empty else None}"
                )

                if confidence < RECOGNITION_THRESHOLD and not match.empty:

                    name = match["name"].values[0]
                    student_id = match["id"].values[0]

                    photo_col, msg_col = st.columns([1, 4])

                    with photo_col:
                        headshot = get_student_photo(student_id)
                        if headshot:
                            st.image(headshot, width=70)

                    with msg_col:
                        st.success(f"Recognized: {name}")

                    today = str(date.today())

                    if os.path.exists(ATTENDANCE_PATH):

                        att = pd.read_csv(ATTENDANCE_PATH)

                    else:

                        att = pd.DataFrame(
                            columns=[
                                "id",
                                "name",
                                "date",
                                "time",
                            ]
                        )

                    if "id" not in att.columns:
                        att["id"] = att["name"].apply(get_student_id_by_name)

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
                            "id": student_id,
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

                    print(
                        f"[Take Attendance] REJECTED — confidence "
                        f"{confidence:.1f} did not clear threshold "
                        f"{RECOGNITION_THRESHOLD}, or no matching label."
                    )

                    st.error(
                        "Face not recognized. If this student is "
                        "registered, try again with better lighting — "
                        "otherwise, register them first."
                    )
