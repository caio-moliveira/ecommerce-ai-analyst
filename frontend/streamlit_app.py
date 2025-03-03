import streamlit as st
from pages import home, sales_query, reports

# Configure Streamlit
st.set_page_config(page_title="E-commerce AI Analytics", layout="wide")

# Sidebar navigation
st.sidebar.title("📊 AI-Powered Sales Dashboard")
page = st.sidebar.radio("Navigation", ["Home", "Sales Query", "Reports"])

# Render the selected page
if page == "Home":
    home.render()
elif page == "Sales Query":
    sales_query.render()
elif page == "Reports":
    reports.render()
