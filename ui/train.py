"""Train Model screen."""

import os
import streamlit as st
import numpy as np
import cv2

from config import DATASET_DIR, MODEL_PATH
from core.labels import load_labels
from styles import ICON_CPU_CHIP


def render_train_page():

    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        f"{ICON_CPU_CHIP}Train Recognition Model"
        "</div>"
        '<p style="color:#777;">'
        "Run this after registering all students "
        "(or whenever you add someone new)."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if st.button("Train Now", icon=":material/model_training:"):

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
