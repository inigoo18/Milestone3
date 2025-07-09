import streamlit as st
from admin_manager import render_admin_view
from user_manager import render_user_view

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(page_title="DUPIFLOW", layout="wide")

if "mode" not in st.session_state:
    st.session_state.mode = "User"

def toggle_mode():
    st.session_state.mode = "Admin" if st.session_state.mode == "User" else "User"

image_path = "assets/sanofi-logo.png"  # adjust path as needed

img_base64 = get_base64_of_bin_file(image_path)

BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"

def set_background(mode):
    if mode == "Admin":
        pastel_color = "rgba(232, 209, 255, 0.6)"  # pastel purple with lower opacity
    else:
        pastel_color = "rgba(255, 235, 204, 0.6)"  # pastel orange with lower opacity

    st.markdown(f"""
    <style>
    /* Body container */
    .stApp {{
        position: relative;
        min-height: 100vh;
        background-color: {pastel_color};
        z-index: 0;
        overflow: hidden;
    }}

        /* Background image bottom right */
        .stApp::before {{
        content: "";
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 200px;
        height: 200px;
        background-image: url("data:image/png;base64,{img_base64}");
        background-repeat: no-repeat;
        background-position: center;
        background-size: contain;
        opacity: 0.15;
        z-index: 0;
        pointer-events: none;
    }}

    /* Content container above background */
    .appview-container > main {{
        position: relative;
        z-index: 10;
        background: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# HEADER
top_col = st.columns([9, 1])
with top_col[0]:
    st.markdown(
        """
        <div style="margin-top: 40px;">
            <h1>DUPIFLOW</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_col[1]:
    st.markdown('<div style="margin-top: 40px;">', unsafe_allow_html=True)
    icon = "🛠️" if st.session_state.mode == "User" else "👤"
    st.button(icon, help="Switch mode", key="mode_toggle", on_click=toggle_mode)
    st.markdown("</div>", unsafe_allow_html=True)



set_background(st.session_state.mode)

if st.session_state.mode == "Admin":
    render_admin_view()
else:
    render_user_view()

st.markdown("""
<style>
footer {visibility: hidden;}
.block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)
