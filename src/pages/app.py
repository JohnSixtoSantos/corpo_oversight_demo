from pathlib import Path
from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import fitz

from src.utils import (
    extract_name,
    extract_reporting_period,
    extract_shareholders
)

load_dotenv()

# App layout
st.set_page_config(page_title="Document Analyzer", layout="wide")

st.title("📊 AI-Powered Document Analyzer")
st.markdown("Upload your financial reports to extract and analyze key data.")

uploaded_file = st.file_uploader("Upload XLSX or PDF file", type=["xlsx", "xls", "pdf"])

# Main processing
if uploaded_file is not None:
    file_type = Path(uploaded_file.name).suffix.lower()

    with st.spinner("Processing file..."):
        if file_type in [".xlsx", ".xls"]:
            df = pd.read_excel(uploaded_file)  # <-- Read Excel file into pandas

            with st.expander("🔍 Excel Data Preview"):
                st.write("**First 5 rows of the spreadsheet:**")
                st.dataframe(df.head())  # Display the top rows

            company_name = extract_name(df)
            reporting_period = extract_reporting_period(df, company_name)
            shareholders = extract_shareholders(df, company_name, reporting_period)

            st.success("Ingestion complete!")
        else:
            st.error("Unsupported file format.")

# Footer style
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Developed with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True
)
