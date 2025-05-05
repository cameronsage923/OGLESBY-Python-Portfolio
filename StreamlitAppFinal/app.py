import streamlit as st
import pandas as pd

#Setting up the main page of the app:
st.set_page_config(page_title="Multifamily Deal Visualizer", layouts="centered")
st.title("🏢 Multifamily Value-Add Deal Visualizer")
st.markdown("""
This app lets you model the financials of a value-add multifamily real estate deal.  
Adjust assumptions like rent, renovations, and cap rate to see how value is created.
""")

#Placeholder for sidebar inputs:
st.sidebar.header("Deal Assumptions")

#Handling the user inputs in sidebar:

# Property Info:
units = st.sidebar.number_input("Number of Units", min_value=1, value=10, step=1)
current_rent = st.sidebar.number_input("Current Rent per Unit ($)", min_value=0, value=1000, step=50)
renovated_rent = st.sidebar.number_input("Renovated Rent per Unit ($)", min_value=0, value=1200, step=50)

# Occupancy:
occupancy_pre = st.sidebar.slider("Current Occupancy Rate (%)", min_value=0, max_value=100, value=90)
occupancy_post = st.sidebar.slider("Stabilized Occupancy Rate (%)", min_value=0, max_value=100, value=95)

# Expenses:
expense_ratio = st.sidebar.slider("Operating Expense Ratio (%)", min_value=0, max_value=100, value=40)

# Financials:
renovation_cost_per_unit = st.sidebar.number_input("Renovation Cost per Unit ($)", min_value=0, value=10000, step=1000)
purchase_price = st.sidebar.number_input("Acquisition Cost ($)", min_value=0, value=1000000, step=50000)
exit_cap_rate = st.sidebar.number_input("Exit Cap Rate (%)", min_value=1.0, max_value=15.0, value=5.0, step=0.1) / 100