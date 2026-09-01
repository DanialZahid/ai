"""Smart Face Attendance System — entry point.

This file only wires things together: page config, global CSS, the sidebar,
and routing to whichever screen is currently selected. Each screen's actual
logic lives in ui/, and shared non-UI logic lives in core/.
"""

import os
import streamlit as st

from styles import CSS, ICON_CAMERA
from ui.sidebar import render_sidebar
from ui.register import render_register_page
from ui.train import render_train_page
from ui.attendance import render_attendance_page
from ui.view_log import render_view_log_page
from ui.status_page import render_status_page

from config import DATASET_DIR

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

st.set_page_config(
    page_title="Smart Face Attendance",
    page_icon="📷",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="page-title">'
    f"{ICON_CAMERA}Smart Face Attendance System"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">'
    "AI-powered student attendance management"
    "</div>",
    unsafe_allow_html=True,
)

mode = render_sidebar()

if st.session_state.show_status:
    render_status_page()
elif mode == "Register Student":
    render_register_page()
elif mode == "Train Model":
    render_train_page()
elif mode == "Take Attendance":
    render_attendance_page()
elif mode == "View Attendance":
    render_view_log_page()

st.markdown(
    '<div class="footer">'
    f"{ICON_CAMERA}Smart Face Attendance System "
    "• AI & Computer Vision"
    "</div>",
    unsafe_allow_html=True,
)
