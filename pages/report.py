import streamlit as st
import os

st.set_page_config(page_title="EDA Report Viewer", layout="wide")

st.title("📊 Full EDA Report")
st.page_link("app.py", label="⬅️ Back to Home", icon="🏠")

if "latest_report" in st.session_state and os.path.exists(st.session_state["latest_report"]):
    with open(st.session_state["latest_report"], "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=1000, scrolling=True)
else:
    st.warning("No report found. Go back and generate one.")
    
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)