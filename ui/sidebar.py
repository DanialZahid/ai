"""Sidebar: title, nav buttons, and the System Status entry point."""

import streamlit as st

from config import NAV_ITEMS
from core.status import get_status_checks
from styles import ICON_CAMERA


def render_sidebar():
    """Render the sidebar and return the currently selected nav mode."""

    if "show_status" not in st.session_state:
        st.session_state.show_status = False

    if "nav_mode" not in st.session_state:
        st.session_state.nav_mode = NAV_ITEMS[0][0]

    with st.sidebar:

        st.markdown(
            '<div class="sidebar-title">'
            f"{ICON_CAMERA}SMART ATTENDANCE"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="sidebar-subtitle">'
            "AI-Based Student Attendance System"
            "</div>",
            unsafe_allow_html=True,
        )

        for nav_label, nav_icon in NAV_ITEMS:
            is_active = st.session_state.nav_mode == nav_label

            if st.button(
                nav_label,
                icon=nav_icon,
                key=f"nav_btn_{nav_label}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.nav_mode = nav_label
                st.session_state.show_status = False

        mode = st.session_state.nav_mode

        st.markdown('<div class="sidebar-bottom-anchor"></div>', unsafe_allow_html=True)

        st.markdown("---")

        _issues = sum(
            1
            for c in get_status_checks()
            if c["status"] in ("warning", "error")
        )

        _status_label = "System Status" + (
            f" ({_issues})" if _issues else ""
        )

        if st.button(
            _status_label,
            icon=":material/health_and_safety:",
            use_container_width=True,
            type="primary" if st.session_state.show_status else "secondary",
        ):
            st.session_state.show_status = True

    return mode
