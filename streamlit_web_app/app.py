import streamlit as st  
import pandas as pd 
import os
from io import BytesIO

# Setup our app
st.set_page_config(page_title="🪐Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp{
    background-color:black;
    color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("🪐Data Sweeper Sterling Integrator  By Shagufta Kanwal")
st.write("Transform your file between CSV and Excel format with built-in data cleaning and visualization!")

# Uploaded file
uploaded_files = st.file_uploader("Upload Your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")    
        continue

    # Show preview of the data
    st.write("Preview the Head of the DataFrame")
    st.dataframe(df.head())

    # Option for data cleaning
    st.subheader("Data Cleaning Options")
    if st.checkbox(f"Clean Data for {file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from: {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")

        with col2:
            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing values have been filled!")

        # Choose specific columns to keep or convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Create some visualization
        st.subheader("💿 Data Visualization")             
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the file ==> CSV to Excel
        st.subheader("🌡 Conversions Options") 
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)  # type: ignore
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)  # type: ignore

            # Download Button
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,  # type: ignore
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed!")
