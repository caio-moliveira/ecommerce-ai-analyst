import streamlit as st
import pandas as pd
from components.api import fetch_sales_data


def render():
    st.title("📊 E-commerce Sales Dashboard")

    # Fetch sales data from backend
    sales_data = fetch_sales_data()

    if sales_data:
        df = pd.DataFrame(sales_data)
        st.dataframe(df)

        # Show summary metrics
        total_sales = df["total_revenue"].sum()
        total_orders = df.shape[0]

        col1, col2 = st.columns(2)
        col1.metric("Total Revenue", f"${total_sales:,.2f}")
        col2.metric("Total Orders", total_orders)
    else:
        st.error("Failed to fetch sales data.")
