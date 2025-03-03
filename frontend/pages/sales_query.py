import streamlit as st
from components.api import analyze_data


def render():
    st.title("🤖 AI-Powered Sales Query")

    question = st.text_input(
        "Ask a question about sales data:", "What were the total sales last month?"
    )

    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            response = analyze_data(question)
            if response:
                st.success("Analysis Complete!")
                st.write(response["insights"])
            else:
                st.error("Failed to fetch AI insights.")
