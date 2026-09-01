"""App-wide constants: file paths, tuning values, navigation."""

DATASET_DIR = "dataset"
MODEL_PATH = "data/trainer.yml"
LABELS_PATH = "data/labels.csv"
ATTENDANCE_PATH = "data/attendance.csv"

# LBPH: lower confidence = better match. This threshold is a tuned default,
# not a guarantee — recognition reliability depends heavily on registering
# 3-5 varied photos per student (see the Register Student screen).
RECOGNITION_THRESHOLD = 65

NAV_ITEMS = [
    ("Register Student", ":material/person_add:"),
    ("Train Model", ":material/model_training:"),
    ("Take Attendance", ":material/photo_camera:"),
    ("View Attendance", ":material/fact_check:"),
]
