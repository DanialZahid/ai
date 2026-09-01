"""Register Student screen."""

import os
import streamlit as st
import pandas as pd
import cv2
from PIL import Image

from config import DATASET_DIR
from core.detection import detect_face_gray
from core.labels import load_labels, save_labels
from styles import ICON_USER_PLUS, ICON_LIGHT_BULB
from ui.components import get_photo


def render_register_page():

    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        f"{ICON_USER_PLUS}Register a New Student"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1.5])

    with col1:

        name = st.text_input("Student name")

        st.markdown(
            '<div class="info-card">'
            f"{ICON_LIGHT_BULB}Capture 3-5 photos from different "
            "angles for better accuracy."
            "</div>",
            unsafe_allow_html=True,
        )

    with col2:

        photo = get_photo("Capture face", "register")

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
