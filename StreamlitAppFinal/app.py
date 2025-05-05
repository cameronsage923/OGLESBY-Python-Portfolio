import streamlit as st
import pandas as pd

# Setting up the main page of the app:
st.set_page_config(page_title="Multifamily Deal Visualizer", layout="centered")
st.title("🏢 Multifamily Value-Add Deal Visualizer")
st.markdown("""
This app lets you model the financials of a value-add multifamily real estate deal.  
Adjust assumptions like rent, renovations, and cap rate to see how value is created.
""")

# Placeholder for sidebar inputs:
st.sidebar.header("Deal Assumptions")

# Handling the user inputs in sidebar:

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

# Financial Calculations:

# Convert occupancy rates and expense ratio from % to decimals:
occupancy_rate_pre = occupancy_pre / 100
occupancy_rate_post = occupancy_post / 100
expense_ratio_decimal = expense_ratio / 100

# Computing Annual Gross Income:
gross_income_current = units * current_rent * 12 * occupancy_rate_pre
gross_income_renovated = units * renovated_rent * 12 * occupancy_rate_post

# Computing Operating Expenses:
operating_expenses_current = gross_income_current * expense_ratio_decimal
operating_expenses_renovated = gross_income_renovated * expense_ratio_decimal

# NOI Calculations:
noi_current = gross_income_current - operating_expenses_current
noi_renovated = gross_income_renovated - operating_expenses_renovated

# Property Value after Renovation (using cap rate):
value_after_renovation = noi_renovated / exit_cap_rate

# Computing Total Renovation Cost:
total_renovation_cost = renovation_cost_per_unit * units

# Computing Total Project Cost:
total_project_cost = purchase_price + total_renovation_cost

# Computing Total Value Creation:
value_created = value_after_renovation - total_project_cost

# Outputting the Results to the user:
st.subheader("📈 Deal Summary")

st.write("### Net Operating Income (NOI)")
st.write(f"**Current NOI:** ${noi_current:,.2f}")
st.write(f"**Stabilized NOI:** ${noi_renovated:,.2f}")

st.write("### Property Valuation")
st.write(f"**Projected Property Value After Renovation:** ${value_after_renovation:,.2f}")

st.write("### Costs and Value Creation")
st.write(f"**Total Renovation Cost:** ${total_renovation_cost:,.2f}")
st.write(f"**Total Project Cost (Acquisition + Reno):** ${total_project_cost:,.2f}")
st.write(f"**Estimated Value Created:** ${value_created:,.2f}")