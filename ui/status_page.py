"""System Status screen — self-diagnostic, purely informational."""

import streamlit as st

from core.status import get_status_checks, STATUS_STYLE
from styles import ICON_STATUS


def render_status_page():
    st.markdown(
        f'<div class="card"><div class="section-title">{ICON_STATUS}System Status</div>'
        '<p style="color:#777;">Live check of the app\'s setup — for troubleshooting only. '
        'Nothing here blocks you from using the app.</p></div>',
        unsafe_allow_html=True
    )

    for check in get_status_checks():
        icon, label_text = STATUS_STYLE[check["status"]]

        with st.expander(f"{check['name']} — {label_text}", icon=f":material/{icon}:"):
            st.write(check["detail"])

            if check["fix"]:
                st.markdown(f"**Suggested fix:** {check['fix']}")
