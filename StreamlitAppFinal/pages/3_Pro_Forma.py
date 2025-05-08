import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pro Forma Statement", layout="centered")
st.title("📄 Pro Forma Statement")

st.markdown("""
#### 📋 What is a Pro Forma?

A **pro forma** is a forward-looking financial projection. In real estate, it estimates a property’s income, expenses, and cash flow over the life of the investment — often 5 to 10 years. It helps investors evaluate whether a deal is likely to meet their return targets.
""")

# First, pull key values from session_state:

required_keys = ["units", "renovated_rent", "occupancy_post", "expense_ratio_decimal", "hold_period", "debt", "interest_rate", "value_after_renovation"]
if not all(k in st.session_state for k in required_keys):
    st.error("Missing required inputs from other pages. Please complete the Deal Visualizer and Waterfall Modeling pages first.")
    st.stop()

units = st.session_state["units"]
rent = st.session_state["renovated_rent"]
occupancy = st.session_state["occupancy_post"]
expense_ratio = st.session_state["expense_ratio_decimal"]
hold_period = st.session_state["hold_period"]
value_after_renovation = st.session_state["value_after_renovation"]

debt = st.session_state["debt"]
interest_rate = st.session_state["interest_rate"]

# Next, build Pro Forma Table:
annual_debt_service = debt * (interest_rate / 100)

rows = []
occupancy = occupancy/100
gross_income = units * rent * 12 * occupancy

for year in range(1, hold_period + 1):
    # Assuming no rent or expense growth to keep things simple:
    income = gross_income
    expenses = income * expense_ratio
    noi = income - expenses
    sale_proceeds = value_after_renovation if year == hold_period else 0

    if year < hold_period:
        debt_service = annual_debt_service
        cash_flow = noi - debt_service
    else:
        debt_service = annual_debt_service + debt # Add debt repayment
        cash_flow = noi - debt_service + value_after_renovation # Add sale proceeds

    rows.append({
        "Year": year,
        "Gross Income": income,
        "Operating Expenses": expenses,
        "NOI": noi,
        "Debt Service": debt_service,
        "Proceeds from Sale": sale_proceeds,
        "Cash Flow to Equity": cash_flow
    })

# Transpose the pro forma to match RE industry format:
proforma_df = pd.DataFrame(rows)

# Color coding & bolding pro forma line items for clarity and visual storytelling:
proforma_df_transposed = proforma_df.set_index("Year").T
def style_rows(row):
    if row.name == "Cash Flow to Equity":
        return ["font-weight: bold;" for _ in row]
    elif row.name == "Debt Service" or row.name == "Operating Expenses":
        return ["color: red;" for _ in row]
    else:
        return ["color: green" for _ in row]
proforma_df_transposed.index.name = "Year:" 

# Finally, display Pro Forma Table:
st.markdown(f"### {hold_period}-Year Simple Pro Forma")
#st.dataframe(
    #proforma_df_transposed.style.format("${:,.0f}")
#)
st.dataframe(
    proforma_df_transposed.style
        .format("${:,.0f}")
        .apply(style_rows, axis=1)
)

st.markdown("""
The table above shows key financial projections for each year of the investment:

- **Gross Income**: Rental income, adjusted for annual rent growth  
- **Operating Expenses**: Property costs, adjusted for expense growth  
- **NOI**: Income after expenses, before loan payments  
- **Debt Service**: Annual loan payments (if debt is used)  
- **Cash Flow**: The money available to investors each year 
""")


# Adding a Visualization:

st.markdown("### 📊 Annual Cash Flow Components (Bar Chart)")

# Set up the components
x = np.arange(len(proforma_df["Year"]))  # the label locations
width = 0.15  # width of the bars

fig3, ax3 = plt.subplots(figsize=(12, 6))

# Plot each component side-by-side
ax3.bar(x - 2*width, proforma_df["Gross Income"], width, label="Gross Income", color="#1f77b4")
ax3.bar(x - width, -proforma_df["Operating Expenses"], width, label="Operating Expenses", color="#ff7f0e")
ax3.bar(x, -proforma_df["Debt Service"], width, label="Debt Service", color="#d62728")
ax3.bar(x + width, proforma_df["Proceeds from Sale"], width, label="Proceeds from Sale", color="#9467bd")
ax3.bar(x + 2*width, proforma_df["Cash Flow to Equity"], width, label="Cash Flow to Equity", color="#2ca02c")

# Format chart
ax3.set_xticks(x)
ax3.set_xticklabels(proforma_df["Year"])
ax3.set_ylabel("Dollars ($)")
ax3.set_title("Annual Cash Flow Components")
ax3.axhline(0, color="gray", linewidth=0.8)
ax3.legend()
st.pyplot(fig3)
