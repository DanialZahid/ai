"""Student labels (id <-> name) and headshot photo lookups."""

import os
import pandas as pd

from config import DATASET_DIR, LABELS_PATH


def load_labels():
    if os.path.exists(LABELS_PATH):
        return pd.read_csv(LABELS_PATH)
    return pd.DataFrame(columns=["id", "name"])


def save_labels(df):
    df.to_csv(
        LABELS_PATH,
        index=False,
    )


def get_student_photo(student_id):
    """Return the path to a registered student's first saved photo (used as
    their headshot elsewhere in the app), or None if they have no photos."""
    try:
        student_dir = os.path.join(DATASET_DIR, str(int(student_id)))
    except (ValueError, TypeError):
        return None

    if not os.path.isdir(student_dir):
        return None

    files = sorted(os.listdir(student_dir))
    if not files:
        return None

    return os.path.join(student_dir, files[0])


def get_student_id_by_name(name):
    """Look up a student's id from their name, for attendance rows saved
    before the id column existed."""
    labels = load_labels()
    match = labels[labels["name"] == name]
    if match.empty:
        return None
    return match["id"].values[0]
