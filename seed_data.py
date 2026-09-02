import os
import random
import shutil
from datetime import datetime, timedelta

import cv2
import numpy as np
import pandas as pd
from PIL import Image

from config import DATASET_DIR, LABELS_PATH, ATTENDANCE_PATH, MODEL_PATH
from core.detection import detect_face_gray

random.seed(42)
np.random.seed(42)

NUM_STUDENTS = 100
SEED_PHOTOS_DIR = "seed_photos"
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png")


# ------------------------------------------------------------------
# 1. Process the user-supplied source photos into face crops
# ------------------------------------------------------------------
def build_face_pool():
    if not os.path.isdir(SEED_PHOTOS_DIR):
        raise RuntimeError(
            f"'{SEED_PHOTOS_DIR}/' folder not found. Create it and add "
            f"10-20 real headshot photos (.jpg/.png) before running this script."
        )

    source_files = [
        f for f in sorted(os.listdir(SEED_PHOTOS_DIR))
        if f.lower().endswith(VALID_EXTENSIONS)
    ]

    if not source_files:
        raise RuntimeError(
            f"No .jpg/.jpeg/.png files found in '{SEED_PHOTOS_DIR}/'. "
            f"Add some real headshot photos and try again."
        )

    pool = []
    skipped = []

    for fname in source_files:
        path = os.path.join(SEED_PHOTOS_DIR, fname)
        try:
            face = detect_face_gray(Image.open(path))
        except Exception as e:
            face = None
            print(f"  Could not read {fname}: {e}")

        if face is None:
            skipped.append(fname)
        else:
            pool.append(face)

    print(f"Processed {SEED_PHOTOS_DIR}/: {len(pool)} usable, {len(skipped)} skipped (no face detected).")
    if skipped:
        print(f"  Skipped: {', '.join(skipped)}")

    if not pool:
        raise RuntimeError(
            f"None of the photos in '{SEED_PHOTOS_DIR}/' had a detectable face. "
            f"Try clearer, front-facing photos."
        )

    if len(pool) < 5:
        print(f"  Note: only {len(pool)} usable photo(s) — headshots will repeat a lot. "
              f"10-20 photos gives more visual variety across the 100 students.")

    return pool


# ------------------------------------------------------------------
# 2. Generate 100 unique plausible student names
# ------------------------------------------------------------------
FIRST_NAMES = [ "Aiden", "Sophia", "Liam", "Olivia", "Emma", "Ethan", "Ava", "Mason", "Isabella", "Lucas", "Mia", "Logan", "Amelia", "Jack", "Harper", "Owen", "Evelyn", "Leo", "Abigail", "Wyatt", "Ella", "Julian", "Scarlett", "Levi", "Grace", "Hudson", "Chloe", "Grayson", "Victoria", "Riley", "Anthony", "Aria", "Dylan", "Lily", "Gary", "Aubrey", "Adrian", "Zoey", "Nathan", "Penelope", "Cameron", "Layla", "Ryan", "Nora", "Jaxon", "Hazel", "Benjamin", "Emily", "James", "Charlotte", "Henry", "Elizabeth", "Alexander", "Samantha", "Michael", "Madison", "Daniel", "Eleanor", "Matthew", "Samuel", "David", "Ellie", "Joseph", "Andrew", "Lucy", "Christopher", "Anna", "John", "Claire", "William", "Hannah", "Thomas", "Sarah", "Charles", "Caroline", "Robert", "Alice", "George", "Julia", "Edward", "Audrey", "Natalie", "Lillian", "Oliver", "Sophie", "Harry", "Amelia", "Charlie", "Isla", "Oscar", "Florence", "Arthur", "Poppy", "Jack", "Evie", "Freddie", "Rosie", "Archie", "Millie", ]

LAST_NAMES = [ "Smith", "Johnson", "Williams", "Jones", "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Thompson", "White", "Harris", "Clark", "Lewis", "Robinson", "Walker", "Allen", "King", "Wright", "Scott", "Hill", "Green", "Adams", "Baker", "Nelson", "Carter", "Mitchell", "Roberts", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Peterson", "Gray", "Watson", "Brooks", "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Foster", "Butler", "Simmons", "Fisher", "Russell", "Griffin", "Hayes", "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan", "Owens", "Reynolds", "Fleming", "Webster", "Hunter", "Marshall", "Spencer", "Harrison", "Lawson", "Bradley", "Pearson", "Dawson", ]


def generate_unique_names(n):
    names = set()
    while len(names) < n:
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        names.add(name)
    return list(names)


# ------------------------------------------------------------------
# 3. Reset and write labels + one headshot per student
# ------------------------------------------------------------------
def seed_students(pool):
    if os.path.isdir(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
    os.makedirs(DATASET_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    names = generate_unique_names(NUM_STUDENTS)
    labels_rows = []

    for student_id, name in enumerate(names):
        labels_rows.append({"id": student_id, "name": name})

        student_dir = os.path.join(DATASET_DIR, str(student_id))
        os.makedirs(student_dir, exist_ok=True)

        face = random.choice(pool)
        cv2.imwrite(os.path.join(student_dir, "0.jpg"), face)

    labels_df = pd.DataFrame(labels_rows)
    labels_df.to_csv(LABELS_PATH, index=False)
    print(f"Registered {len(labels_df)} students (1 photo each, randomly assigned from the pool).")
    return labels_df


# ------------------------------------------------------------------
# 4. Simulate a multi-week attendance history
# ------------------------------------------------------------------
def seed_attendance(labels_df, num_sessions=10):
    today = datetime.now().date()

    # Class held every Mon/Wed/Fri, working backwards from today
    session_dates = []
    d = today
    while len(session_dates) < num_sessions:
        if d.weekday() in (0, 2, 4):  # Mon, Wed, Fri
            session_dates.append(d)
        d -= timedelta(days=1)
    session_dates.reverse()

    rows = []
    for session_date in session_dates:
        for _, student in labels_df.iterrows():
            # Most students attend most sessions, some are less consistent
            attendance_rate = random.choice([0.95, 0.9, 0.85, 0.8, 0.7])
            if random.random() > attendance_rate:
                continue

            hour = random.choice([9, 9, 9, 14, 14])  # mostly a 9am class, some 2pm
            minute = random.randint(0, 20)
            second = random.randint(0, 59)

            rows.append({
                "id": student["id"],
                "name": student["name"],
                "date": str(session_date),
                "time": f"{hour:02d}:{minute:02d}:{second:02d}",
            })

    attendance_df = pd.DataFrame(rows)
    attendance_df.to_csv(ATTENDANCE_PATH, index=False)
    print(f"Generated {len(attendance_df)} attendance records across {num_sessions} sessions "
          f"({session_dates[0]} to {session_dates[-1]}).")


# ------------------------------------------------------------------
# 5. Pre-train the recognition model on the seeded photos
# ------------------------------------------------------------------
def train_model():
    labels_df = pd.read_csv(LABELS_PATH)
    faces, ids = [], []

    for _, row in labels_df.iterrows():
        student_dir = os.path.join(DATASET_DIR, str(row["id"]))
        for fname in os.listdir(student_dir):
            img = cv2.imread(os.path.join(student_dir, fname), cv2.IMREAD_GRAYSCALE)
            if img is not None:
                faces.append(img)
                ids.append(int(row["id"]))

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.save(MODEL_PATH)
    print(f"Trained recognition model on {len(faces)} photos.")
    print("  Note: since headshots repeat across these seeded students, the model")
    print("  won't meaningfully distinguish between them — that's expected and fine,")
    print("  this data is for populating the log/UI, not for a live recognition demo.")


if __name__ == "__main__":
    pool = build_face_pool()
    labels_df = seed_students(pool)
    seed_attendance(labels_df)
    train_model()
    print("\nDone. Run the app as usual — View Attendance is already populated with demo data.")
