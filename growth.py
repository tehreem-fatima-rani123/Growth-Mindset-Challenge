import streamlit as st
import pandas as pd
import os
from io import BytesIO

# App Configuration
st.set_page_config(page_title="Smart Data Processor", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
        .main { background-color: #eef2f3; }
        h1 { color: #2c3e50; text-align: center; font-size: 42px; font-weight: bold; }
        .stButton>button { width: 100%; border-radius: 8px; font-size: 16px; }
        .stDownloadButton>button { width: 100%; background-color: #3498db; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title and Description
st.title("📂 Smart Data Processor")
st.markdown(
    """ 
    🔄 Easily transform and clean your CSV & Excel files! 
    - **Upload, Preview, Clean, Visualize & Download with a click** ⚡
    """
)

# File Uploader
uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel)", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[-1].lower()
        try:
            # Read the file
            df = pd.read_csv(uploaded_file) if file_ext == '.csv' else pd.read_excel(uploaded_file)
            
            # File Details
            st.subheader(f"📄 File: {uploaded_file.name}")
            st.write(f"**Size:** {uploaded_file.size / 1024:.2f} KB")

            # Preview
            with st.expander("👀 Preview Data"):
                st.dataframe(df.head())
            
            # Data Cleaning
            st.subheader("🧼 Data Cleaning")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Remove Duplicates"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button("Fill Missing Values"):
                    for col in df.select_dtypes(include=['number']).columns:
                        df[col].fillna(df[col].mean(), inplace=True)
                    st.success("✅ Missing Values Filled!")

            # Column Selection with More Options
            st.subheader("🎯 Select Columns to Keep")
            with st.expander("⚙ Advanced Column Selection"):
                st.write("Select the columns you want to keep from your dataset.")
                all_cols = st.checkbox("Select All Columns", value=True)
                predefined_columns = ["Name", "Email", "Age", "Gender", "City", "Country", "Phone Number", "Address", "Score", "Salary", "Department", "Joining Date"]
                if all_cols:
                    selected_cols = df.columns.tolist()
                else:
                    selected_cols = st.multiselect("Choose Columns", df.columns.tolist() + predefined_columns, default=df.columns[:min(5, len(df.columns))])
            df = df[selected_cols]
            
            # Data Visualization
            st.subheader("📊 Data Visualization")
            if st.checkbox("Show Charts"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    st.bar_chart(df[numeric_cols].iloc[:, :2])
                else:
                    st.warning("Not enough numeric columns for visualization.")
            
            # File Conversion
            st.subheader("🔁 Convert & Download")
            conversion_type = st.radio("Convert file to:", ['CSV', 'Excel'], key=uploaded_file.name)
            if st.button("Convert & Download"):
                buffer = BytesIO()
                new_ext = '.csv' if conversion_type == 'CSV' else '.xlsx'
                new_file_name = uploaded_file.name.replace(file_ext, new_ext)
                mime_type = 'text/csv' if conversion_type == 'CSV' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                if conversion_type == 'CSV':
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                st.download_button("⬇ Download File", buffer, file_name=new_file_name, mime=mime_type)
        
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {e}")

st.success("🎉 Thank you for using Smart Data Processor!")
