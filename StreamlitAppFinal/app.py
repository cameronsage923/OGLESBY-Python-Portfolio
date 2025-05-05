import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Setting up the main page of the app:
st.set_page_config(page_title="Multifamily Deal Visualizer", layout="centered")
st.title("🏢 Multifamily Value-Add Deal Visualizer")
st.markdown("""
This app lets you model the financials of a value-add multifamily real estate deal.  
Adjust assumptions like rent, renovations, and cap rate to see how value is created.
""")

# Placeholder for sidebar inputs:
st.header("🔧 Deal Assumptions")

# --- Acquisition Assumptions ---
st.subheader("🏷️ Acquisition Assumptions")
col1a, col1b = st.columns(2)
with col1a:
    purchase_price = st.number_input("Acquisition Cost ($)", min_value=0, value=1000000)
    exit_cap_rate = st.number_input("Exit Cap Rate (%)", min_value=1.0, max_value=15.0, value=5.0, step=0.1) / 100
with col1b:
    units = st.number_input("Number of Units", min_value=1, value=10)
    current_rent = st.number_input("Current Rent per Unit ($)", min_value=0, value=1000)

# --- Renovation Assumptions ---
st.subheader("🛠️ Renovation Assumptions")
col2a, col2b = st.columns(2)
with col2a:
    renovated_rent = st.number_input("Renovated Rent per Unit ($)", min_value=0, value=1200)
with col2b:
    renovation_cost_per_unit = st.number_input("Renovation Cost per Unit ($)", min_value=0, value=10000)

# --- Operating Assumptions ---
st.subheader("📊 Operating Assumptions")
col3a, col3b = st.columns(2)
with col3a:
    occupancy_pre = st.slider("Current Occupancy Rate (%)", 0, 100, 90)
    expense_ratio = st.slider("Operating Expense Ratio (%)", 0, 100, 40)
with col3b:
    occupancy_post = st.slider("Stabilized Occupancy Rate (%)", 0, 100, 95)

# Handling errors: show warnings if key inputs are questionable:
if current_rent <= 0 or renovated_rent <= 0:
    st.warning("⚠️ Rents must be greater than $0.")

if exit_cap_rate <= 0:
    st.warning("⚠️ Exit Cap Rate must be greater than 0% to calculate property value.")

if purchase_price <= 0:
    st.warning("⚠️ Acquisition Cost should be greater than $0.")

if occupancy_pre == 0 or occupancy_post == 0:
    st.warning("⚠️ A 0% occupancy rate will produce $0 income.")

if units <= 0:
    st.warning("⚠️ Number of units must be at least 1.")

# Financial Calculations:

if current_rent > 0 and renovated_rent > 0 and exit_cap_rate > 0 and units > 0:
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
    
    # Adding visualizations for user exploration:
    # Preparing a summary DataFrame:
    summary_data = pd.DataFrame({
        "Metric": [
            "Current NOI",
            "Stabilized NOI",
            "Projected Property Value",
            "Total Renovation Cost",
            "Total Project Cost",
            "Value Created"
        ],
        "Amount ($)": [
            round(noi_current, 2),
            round(noi_renovated, 2),
            round(value_after_renovation, 2),
            round(total_renovation_cost, 2),
            round(total_project_cost, 2),
            round(value_created, 2)
        ]
    })

    # Create downloadable CSV
    csv = summary_data.to_csv(index=False).encode("utf-8")
    tab1, tab2, tab3 = st.tabs(["📈 Financial Summary", "📊 Visual Comparisons","📄 Download"])
    with tab1:
        col1a, col1b = st.columns(2)
        with col1a:
            st.write("### Net Operating Income (NOI)")
            st.write(f"**Current NOI:** ${noi_current:,.2f}")
            st.write(f"**Stabilized NOI:** ${noi_renovated:,.2f}")
            st.write("### Property Valuation")
            st.write(f"**Projected Property Value After Renovation:** ${value_after_renovation:,.2f}")
        with col1b:
            st.write("### Costs and Value Creation")
            st.write(f"**Total Renovation Cost:** ${total_renovation_cost:,.2f}")
            st.write(f"**Total Project Cost (Acquisition + Reno):** ${total_project_cost:,.2f}")
            st.write(f"**Estimated Value Created:** ${value_created:,.2f}")
    with tab2:
        st.subheader("📊 Visual Comparisons")
        # Create 2 or 3 columns
        col1, col2 = st.columns(2)
        # NOI Comparison Chart
        with col1:
            st.write("### Current vs. Stabilized NOI")
            fig_noi, ax_noi = plt.subplots()
            ax_noi.bar(["Current", "Stabilized"], [noi_current, noi_renovated], color=["#1f77b4", "#2ca02c"])
            ax_noi.set_title("NOI Comparison")
            ax_noi.set_ylabel("Dollars ($)")
            st.pyplot(fig_noi)
        #Property Value Comparison Chart:
        with col2:
            st.write("### Total Project Cost vs. Post-Reno Property Value")
            fig_value, ax_value = plt.subplots()
            ax_value.bar(["Cost", "Value"], [total_project_cost, value_after_renovation], color=["#ff7f0e", "#9467bd"])
            ax_value.set_title("Project Cost vs Value")
            ax_value.set_ylabel("Dollars ($)")
            st.pyplot(fig_value)

        # NOI Comparison Chart:
        #st.write("### Current vs. Stabilized NOI")

        #fig_noi, ax_noi = plt.subplots()
        #ax_noi.bar(["Current NOI", "Stabilized NOI"], [noi_current, noi_renovated], color=["#1f77b4", "#2ca02c"])
        #ax_noi.set_ylabel("Dollars ($)")
        #ax_noi.set_title("NOI Comparison")
        #st.pyplot(fig_noi)

        # Property Value Comparison Chart:
        #st.write("### Total Project Cost vs. Post-Reno Property Value")

        #fig_value, ax_value = plt.subplots()
        #ax_value.bar(["Total Cost", "Value After Reno"], [total_project_cost, value_after_renovation], color=["#ff7f0e", "#9467bd"])
        #ax_value.set_ylabel("Dollars ($)")
        #ax_value.set_title("Value Creation Comparison")
        #st.pyplot(fig_value)

        #Stacked bar: income vs expenses:
        st.write("### Income vs. Expenses (Pre vs. Post Renovation)")

        fig, ax = plt.subplots()
        ax.bar(["Current"], [gross_income_current], label="Gross Income", color="#1f77b4")
        ax.bar(["Current"], [operating_expenses_current], label="Operating Expenses", color="#ff7f0e", bottom=0)

        ax.bar(["Renovated"], [gross_income_renovated], color="#1f77b4")
        ax.bar(["Renovated"], [operating_expenses_renovated], color="#ff7f0e", bottom=0)

        ax.set_ylabel("Dollars ($)")
        ax.set_title("Income vs Expenses")
        ax.legend()
        st.pyplot(fig)

    with tab3: 
        st.subheader("Downloadable Deal Summary")
        st.dataframe(summary_data)
        st.download_button("⬇️ Download Summary as CSV", data=csv, file_name="deal_summary.csv", mime="text/csv")
    if value_created > 0:
        st.success("🎉 This deal creates value! You should consider pursuing it.")
    else:
        st.error("⚠️ This deal loses value. Consider changing your assumptions.")
else:
    st.error("❌ Cannot calculate financials with invalid inputs above.")


