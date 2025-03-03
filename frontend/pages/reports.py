import streamlit as st
from components.api import generate_report


def render():
    st.title("📑 AI-Generated Reports")

    period = st.selectbox("Select report period", ["Daily", "Weekly", "Monthly"])

    if st.button("Generate Report"):
        with st.spinner("Generating report..."):
            response = generate_report(period.lower())
            if response:
                st.success("Report generated successfully!")
                st.write(response)
            else:
                st.error("Failed to generate report.")
