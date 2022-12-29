import streamlit as st
from pycaret.regression import setup, compare_models, pull, save_model
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
from helper import *

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.image("https://i.ibb.co/SKjmS7K/Streamlit-app-logo-2-45.jpg")
    st.title("AutoSteelML")
    choice = st.radio("Navigation", [
                      "Extract Data", "Clean Data", "Upload Clean Data", "Data Profiling", "Modelling"])
    st.info("This automated ML pipe-line application helps you extract and explore your EAF data")
if st.sidebar.button("Clear Session State"):
    for key in st.session_state.keys():
        del st.session_state[key]

if choice == "Extract Data":
    st.title('Data Extraction')
    # Select the directory containing the Excel files
    st.info('Upload your EAF report excel files', icon="ℹ️")
    with st.form("file_upload-form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Choose your excel files", accept_multiple_files=True)
        submitted = st.form_submit_button("UPLOAD")
    if submitted and uploaded_files is not None:
        st.success("UPLOADED!")
    if st.button('Extract Data'):
        st.session_state.raw_data = extract(uploaded_files)
        # Display the raw_data array
        st.dataframe(st.session_state.raw_data)
        st.success('Data extracted successfully')
    # Save the raw_data array to a CSV file
    st.info('Save the extracted raw data as a CSV file for cleaning', icon="ℹ️")
    if st.button('Save to CSV file'):
        st.session_state.raw_data.to_csv('raw_data.csv', index=False)
        st.dataframe(st.session_state.raw_data)
        st.success('Raw data saved to CSV file')
        with open('raw_data.csv') as f:
            st.download_button('Download CSV', f, file_name='raw_data.csv')

if choice == "Clean Data":
    st.title('Data Cleaning Module')
    st.info('Upload your raw data or use saved data for cleaning', icon="ℹ️")
    file = st.file_uploader("Upload Your Raw Dataset")
    if file:
        st.session_state.raw_data = pd.read_csv(file, index_col=None)
    if 'raw_data' not in st.session_state:
        st.error('Extract or upload raw data', icon="🚨")
        st.stop()
    if not st.session_state.raw_data.empty:
        if st.button('Clean Data'):
            if not os.path.isfile('raw_data.csv'):
                st.session_state.raw_data.to_csv('raw_data.csv', index=False)
            st.session_state.raw_data = pd.read_csv(
                'raw_data.csv', index_col=None)
            st.session_state.clean_data = clean(st.session_state.raw_data)
            # Display the clean_data list
            st.dataframe(st.session_state.clean_data)
            st.success('Data cleaned successfully')
    # Save the clean_data list to a CSV file
    st.info('Save the clean data as a CSV file for profiling', icon="ℹ️")
    if st.button('Save to CSV file'):
        st.session_state.clean_data.to_csv('clean_data.csv', index=False)
        st.dataframe(st.session_state.clean_data)
        st.success('Clean data saved to CSV file')
        with open('clean_data.csv') as f:
            st.download_button('Download CSV', f, file_name='clean_data.csv')

if choice == "Upload Clean Data":
    st.title("Upload Your Clean Dataset")
    st.info('Upload your clean data or use saved data for profiling', icon="ℹ️")
    file = st.file_uploader("Upload Your Dataset")
    if file:
        st.session_state.clean_data = pd.read_csv(file, index_col=None)
        st.dataframe(st.session_state.clean_data)

if choice == "Data Profiling":
    st.title("Exploratory Data Analysis")
    st.info('Generate and download pandas data profile report using uploaded or saved clean data', icon="ℹ️")
    if 'clean_data' not in st.session_state:
        st.error('Extract or upload clean data', icon="🚨")
        st.stop()
    profile_df = st.session_state.clean_data.profile_report()
    if st.button('Generate Data Profile'):
        with st.spinner('Wait for it...'):
            profile_df.to_file('profile_report.html')
        st.success('Done!')
        with open('profile_report.html', 'rb') as f:
            st.download_button('Download Report', f,
                               file_name='profile_report.html')
    if st.button('Show Data Profile'):
        st_profile_report(profile_df)

if choice == "Modelling":
    st.title("Explore ML Models")
    st.info(
        'Generate machine learning models using uploaded or saved clean data', icon="ℹ️")
    if 'clean_data' not in st.session_state:
        st.error('Extract or upload clean data', icon="🚨")
        st.stop()
    chosen_target = st.selectbox(
        'Choose the Target Column', st.session_state.clean_data.columns)
    if st.button('Run Modelling'):
        setup(st.session_state.clean_data, target=chosen_target, silent=True)
        st.info('Model settings:')
        setup_df = pull()
        st.dataframe(setup_df)
        best_model = compare_models()
        st.info('Compare and save the best model:')
        compare_df = pull()
        st.dataframe(compare_df)
        save_model(best_model, 'best_model')
        with open('best_model.pkl', 'rb') as f:
            st.download_button('Download Best Model', f,
                               file_name="best_model.pkl")
