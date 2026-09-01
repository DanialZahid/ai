"""View Attendance screen."""

import os
import streamlit as st
import pandas as pd
from datetime import datetime

from config import ATTENDANCE_PATH
from core.labels import get_student_photo, get_student_id_by_name
from styles import ICON_TABLE_CELLS


def render_view_log_page():

    st.markdown(
        '<div class="card">'
        '<div class="section-title">'
        f"{ICON_TABLE_CELLS}Attendance Log"
        "</div>"
        '<p style="color:#777;">'
        "View all recorded student attendance."
        "</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    if os.path.exists(ATTENDANCE_PATH):

        df = pd.read_csv(ATTENDANCE_PATH)

        if "id" not in df.columns:
            df["id"] = df["name"].apply(get_student_id_by_name)

        df = df.sort_values(["date", "time"], ascending=False).reset_index(drop=True)

        def format_datetime(row):
            dt = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M:%S")
            return f"{dt.strftime('%b %d, %Y')}, {dt.strftime('%I:%M %p').lstrip('0')}"

        header_photo, header_name, header_when = st.columns([1, 3, 3])
        with header_name:
            st.markdown("**Name**")
        with header_when:
            st.markdown("**Date & Time**")

        for _, row in df.iterrows():
            photo_col, name_col, when_col = st.columns([1, 3, 3])

            with photo_col:
                headshot = get_student_photo(row.get("id"))
                if headshot:
                    st.image(headshot, width=45)

            with name_col:
                st.write(row["name"])

            with when_col:
                st.write(format_datetime(row))

    else:

        st.info("No attendance recorded yet.")
