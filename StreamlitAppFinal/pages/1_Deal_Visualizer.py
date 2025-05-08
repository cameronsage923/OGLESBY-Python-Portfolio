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


# Input Acquisition Assumptions:
st.subheader("🏷️ Acquisition Assumptions")
col1a, col1b, col1c = st.columns(3)
with col1a:
    default_purchase_price = st.session_state.get("purchase_price", 1000000)
    purchase_price = st.number_input("Acquisition Cost ($)", min_value=0, value=default_purchase_price)
    st.session_state["purchase_price"] = purchase_price
with col1b:
    default_units = st.session_state.get("units", 10)
    units = st.number_input("Number of Units", min_value=1, value=default_units)
    st.session_state["units"] = units
with col1c:
    default_current_rent = st.session_state.get("current_rent", 1000)
    current_rent = st.number_input("Current Rent per Unit ($)", min_value=0, value=default_current_rent)
    st.session_state["current_rent"] = current_rent
st.markdown("---") 

# Input Renovation Assumptions:
st.subheader("🛠️ Renovation Assumptions")
col2a, col2b = st.columns(2)
with col2a:
    default_renovated_rent = st.session_state.get("renovated_rent", 1200)
    renovated_rent = st.number_input("Renovated Rent per Unit ($)", min_value=0, value=default_renovated_rent)
    st.session_state["renovated_rent"] = renovated_rent
with col2b:
    default_renovation_cost_per_unit = st.session_state.get("renovation_cost_per_unit", 10000)
    renovation_cost_per_unit = st.number_input("Renovation Cost per Unit ($)", min_value=0, value=default_renovation_cost_per_unit)
    st.session_state["renovation_cost_per_unit"] = renovation_cost_per_unit
st.markdown("---") 

# Input Operating Assumptions:
st.subheader("📊 Operating Assumptions")
col3a, col3b = st.columns(2)
with col3a:
    default_occupancy_pre = st.session_state.get("occupancy_pre", 90)
    occupancy_pre = st.slider("Current Occupancy Rate (%)", 0, 100, value=default_occupancy_pre)
    st.session_state["occupancy_pre"] = occupancy_pre
    default_expense_ratio = st.session_state.get("expense_ratio", 40)
    expense_ratio = st.slider("Operating Expense Ratio (%)", 0, 100, value=default_expense_ratio)
    st.session_state["expense_ratio"] = expense_ratio
    with st.expander("What is the Expense Ratio?"):
        st.markdown("""
        The **Expense Ratio** is the percentage of income that goes toward operating expenses.

        For example, a 40% expense ratio means 40% of the rent goes to costs like repairs, management, and utilities.  
        Lower ratios usually mean more efficient or profitable properties.
        """)

with col3b:
    default_occupancy_post = st.session_state.get("occupancy_post", 95)
    occupancy_post = st.slider("Stabilized Occupancy Rate (%)", 0, 100, value=default_occupancy_post)
    st.session_state["occupancy_post"] = occupancy_post
st.markdown("---") 

# Input Investment Assumptions:
st.subheader("📆 Investment Assumptions")
col4a, col4b, col4c = st.columns(3)
with col4a:
    default_hold = st.session_state.get("hold_period", 5)
    hold_period = st.number_input("Hold Period (Years)", min_value=1, value=default_hold)
    st.session_state["hold_period"] = hold_period
    with st.expander("What is Holding Period?"):
        st.markdown("""
        The **Holding Period** is the total number of years the investment is projected to be held before sale.

        It directly impacts projected returns, especially IRR, since time affects the value of cash flows.
        """)

with col4b:
    default_stabilized_year = st.session_state.get("stabilized_year", 2)
    stabilized_year = st.number_input( "Year Stabilized (NOI Begins)", min_value=1, max_value=hold_period, value=default_stabilized_year)
    st.session_state["stabilized_year"] = stabilized_year
    with st.expander("What is the Stabilized Year?"):
        st.markdown("""
        The **Stabilized Year** is when the property is expected to reach normal operations — 
        meaning it's fully leased, renovated, and generating steady income.

        It's important for modeling because income and expenses may be lower or inconsistent before stabilization.
        """)

with col4c:
    default_exit_cap_rate = st.session_state.get("exit_cap_rate", 5)
    exit_cap_rate = st.number_input("Exit Cap Rate (%)", min_value=1.0, max_value=15.0, value=5.0, step=0.1) / 100
    st.session_state["exit_cap_rate"] = exit_cap_rate
    with st.expander("What is an Exit Cap Rate?"):
        st.markdown("""
        The **Exit Cap Rate** is used to estimate the resale value of a property at the end of the holding period:

        \n\\[
        \\text{Exit Value} = \\frac{\\text{Final Year NOI}}{\\text{Exit Cap Rate}}
        \\]

        Investors often assume a slightly higher exit cap rate than the entry cap to be conservative.
        """)

st.markdown("---") 

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
    
    # Create downloadable CSV:
    csv = summary_data.to_csv(index=False).encode("utf-8")
    tab1, tab2, tab3 = st.tabs(["💵 Financial Summary", "📊 Visual Comparisons","📄 Download"])
    with tab1:
        col1a, col1b = st.columns(2)
        with col1a:
            st.write("### Net Operating Income (NOI)")
            st.write(f"**Current NOI:** ${noi_current:,.2f}")
            st.write(f"**Stabilized NOI:** ${noi_renovated:,.2f}")
            with st.expander("What is Net Operating Income (NOI)?"):
                st.markdown("""
                Net Operating Income is calculated as revenue minus operating expenses (excluding debt service, taxes, and capital expenditures).  
                It's a key indicator of a property's profitability before financing costs.
                """)

            st.write("### Property Valuation")
            st.write(f"**Projected Property Value After Renovation:** ${value_after_renovation:,.2f}")
            st.write("### Costs")
            st.write(f"**Total Renovation Cost:** ${total_renovation_cost:,.2f}")
            st.write(f"**Total Project Cost:** ${total_project_cost:,.2f}")
        with col1b:
            st.markdown("## Estimated Value Created")
            value_created_color = "green" if value_created > 0 else "red"
            st.markdown(f"<h2 style='color:{value_created_color};'>${value_created:,.0f}</h2>", unsafe_allow_html=True)
            st.markdown("This is the estimated increase in value after renovations, based on your exit cap rate and stabilized NOI.")

    with tab2:
        st.subheader("📊 Visual Comparisons")

        # NOI Comparison Chart
        st.write("### Current vs. Stabilized NOI")
        fig_noi, ax_noi = plt.subplots()
        ax_noi.bar(["Current", "Stabilized"], [noi_current, noi_renovated], color=["#1f77b4", "#2ca02c"])
        ax_noi.set_title("NOI Comparison")
        ax_noi.set_ylabel("Dollars ($)")
        st.pyplot(fig_noi)
        #Property Value Comparison Chart:
        st.write("### Total Project Cost vs. Post-Reno Property Value")
        fig_value, ax_value = plt.subplots()
        ax_value.bar(["Cost", "Value"], [total_project_cost, value_after_renovation], color=["#ff7f0e", "#9467bd"])
        ax_value.set_title("Project Cost vs Value")
        ax_value.set_ylabel("Dollars ($)")
        st.pyplot(fig_value)

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

# Storing inputs to be used across pages:
st.session_state["total_project_cost"] = total_project_cost
st.session_state["value_after_renovation"] = value_after_renovation
st.session_state["noi_renovated"] = noi_renovated
st.session_state["expense_ratio_decimal"] = expense_ratio_decimal

