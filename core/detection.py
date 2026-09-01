"""Face detection: locates and crops a face from a photo."""

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face_gray(image_pil):
    """Convert PIL image to grayscale numpy,
    detect largest face, return cropped face or None.

    Histogram equalization is applied so that both training and recognition
    always see faces normalized for lighting/contrast the same way — LBPH
    is sensitive to lighting differences, and this keeps training/predict
    inputs consistent regardless of how a given photo was lit.
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

    face = cv2.resize(
        gray[y:y + h, x:x + w],
        (200, 200),
    )

    return cv2.equalizeHist(face)
