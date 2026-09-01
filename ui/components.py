"""Shared UI widgets used by more than one screen."""

import streamlit as st


def get_photo(label, key):
    """Let the user either take a live webcam photo or upload one. Returns
    a file-like object compatible with Image.open(), or None if nothing given yet."""
    method = st.radio(
        "Photo source", ["Use Webcam", "Upload Photo"],
        horizontal=True, key=f"{key}_method",
    )
    if method == "Use Webcam":
        return st.camera_input(label, key=f"{key}_cam")
    else:
        return st.file_uploader(
            label + " (jpg/png)", type=["jpg", "jpeg", "png"], key=f"{key}_upload"
        )
