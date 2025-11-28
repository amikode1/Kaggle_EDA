import streamlit as st
import kaggle
import pandas as pd
from ydata_profiling import ProfileReport
import os
import time

def download(url):
    if url=="":
        st.warning("Please Provide the URL")
    
    else:
        data_path_url = "/".join(url.split("/")[-2:])
        
        info = [file['name'] for file in kaggle.api.dataset_list_files(data_path_url).to_dict()['datasetFiles']]
        st.session_state['files'] = info
        data_path_local = f'data/{data_path_url}'
        st.session_state["datapath"] =  data_path_local
        #download
        kaggle.api.dataset_download_files(data_path_url, path=data_path_local, unzip=True)

        if os.path.exists(f'{data_path_local}'):
            st.session_state['downloaded'] = True
        else:
            st.session_state['downloaded'] = False

def EDA(df_name):
    df = pd.read_csv(f"{st.session_state['datapath']}/{df_name}")
    profile = ProfileReport(df, title="My Data Profile")
    report = f"./static/{df_name.replace(" ","_")}_{int(time.time())}.html"
    profile.to_file(report)
    st.session_state["latest_report"] = report


st.set_page_config(page_title="EDA Report Generator", layout="centered")
st.title("Automate Kaggle EDA")
st.write("This will automate most of Kaggle Exploratory Data Analysis.")

url = st.text_input("URL",placeholder="https://kaggle.com/#####/#####")


st.button("Download Data", on_click=download, args=[url])

if "downloaded" not in st.session_state:
    st.session_state['downloaded'] = False

if st.session_state['downloaded']:
    st.success("Data downloaded successfully!")

    file = st.selectbox("Select a column", st.session_state['files'])    
    st.session_state['file_name'] = file
    if st.button("Generate EDA Report"):
        EDA(st.session_state['file_name'])
        st.success(f"EDA report generated:")

if "latest_report" in st.session_state:
    report_name = os.path.basename(st.session_state["latest_report"])
    st.page_link(
        "pages/report.py",
        label="Open EDA Report",

    )
# Hide sidebar and navigation entirely
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

