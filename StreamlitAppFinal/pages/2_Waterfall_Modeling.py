import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt

st.set_page_config(page_title="Waterfall Modeling", layout="wide")
st.title("📉 Equity Waterfall Modeling")

# Checking for required data:
required_keys = ["total_project_cost", "value_after_renovation", "noi_renovated"]
if not all(k in st.session_state for k in required_keys):
    st.error("Please run the Deal Visualizer first to generate project outputs.")
    st.stop()

# Retrieving project metrics:
total_project_cost = st.session_state["total_project_cost"]
value_after_renovation = st.session_state["value_after_renovation"]
noi_renovated = st.session_state["noi_renovated"]

# Displaying the deal summary:
st.markdown("### 🔍 Deal Snapshot (from Visualizer)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Project Cost", f"${total_project_cost:,.0f}")
col2.metric("Stabilized NOI", f"${noi_renovated:,.0f}")
col3.metric("Projected Exit Value", f"${value_after_renovation:,.0f}")

st.markdown("### 🧮 Waterfall & Capital Stack Assumptions")

col1a, col1b, col1c = st.columns(3)
with col1a:
    hold_period = st.number_input("Hold Period (Years)", min_value=1, value=5)
    st.number_input(
    "📆 Year Stabilized (NOI Begins)",
    min_value=1,
    max_value=hold_period,
    value=2,
    key="stabilized_year"
    )
    debt_ratio = st.slider("Debt %", 0, 100, 60) / 100
with col1b:
    interest_rate = st.number_input("Interest Rate (%)", 0.0, 15.0, 5.0) / 100
    interest_only = st.checkbox("Interest-Only?", value=True)
with col1c:
    gp_equity_pct = st.slider("GP Equity %", 0, 100, 10) / 100
    lp_equity_pct = 1 - gp_equity_pct

st.divider()

col2a, col2b = st.columns(2)
with col2a:
    pref_rate = st.number_input("Preferred Return to LP (%)", 0.0, 20.0, 8.0) / 100
    promote_pct = st.slider("Promote % (GP Share of Upside)", 0, 100, 20) / 100
with col2b:
    show_catchup = st.checkbox("Enable GP Catch-Up Tier?", value=False)

# Capital structure calculations:
equity = total_project_cost * (1 - debt_ratio)
debt = total_project_cost * debt_ratio
gp_equity = equity * gp_equity_pct
lp_equity = equity * lp_equity_pct

# Build annual project-level cash flows:
annual_debt_service = debt * interest_rate if interest_only else 0

stabilized_year = st.session_state["stabilized_year"]

annual_cash_flows = []
for year in range(1, hold_period + 1):
    noi = noi_renovated if year >= stabilized_year else 0
    if year < hold_period:
        debt_payment = annual_debt_service
        equity_cf = noi - debt_payment
    else:
        # Add sale proceeds to final year:
        debt_payment = annual_debt_service + (0 if interest_only else debt)
        equity_cf = noi + value_after_renovation - debt_payment

    annual_cash_flows.append({
        "Year": year,
        "NOI": noi,
        "Debt Service": debt_payment,
        "Cash to Equity": equity_cf
    })

cf_df = pd.DataFrame(annual_cash_flows)

# Create year-by-year LP and GP cash flows:
lp_cf = [-lp_equity]  # Initial investment
gp_cf = [-gp_equity]  # Initial investment

for year_data in annual_cash_flows:
    annual_equity_cf = year_data["Cash to Equity"]

    # Apply promote to final year only (like your original logic)
    if year_data["Year"] == hold_period:
        lp_share = annual_equity_cf * (1 - promote_pct)
        gp_share = annual_equity_cf * promote_pct
    else:
        # Before sale year, assume 100% to LP until preferred return tiers are built
        lp_share = annual_equity_cf
        gp_share = 0

    lp_cf.append(lp_share)
    gp_cf.append(gp_share)


# Display to user:
st.markdown("### 🗓️ Annual Project Cash Flows")
st.dataframe(cf_df.style.format({"NOI": "${:,.0f}", "Debt Service": "${:,.0f}", "Cash to Equity": "${:,.0f}"}))

# Calculate final cash available at exit:
sale_proceeds = value_after_renovation
total_exit_cash = (noi_renovated + sale_proceeds)  # Exit-year NOI + sale
debt_repayment = debt if not interest_only else 0  # Assume balloon payment at end
cash_to_equity = total_exit_cash - debt_repayment

# Defining the Waterfall function:
def waterfall_distribution(lp_equity, pref_rate, hold_period, cash_to_equity, promote_pct, gp_equity, catchup=False):
    results = {}

    # Tier 1: Return of Capital to LP
    tier1 = min(lp_equity, cash_to_equity)
    cash_remaining = cash_to_equity - tier1

    # Tier 2: Preferred Return to LP 
    lp_pref_total = lp_equity * pref_rate * hold_period
    tier2 = min(lp_pref_total, cash_remaining)
    cash_remaining -= tier2

    results["LP Return of Capital"] = tier1
    results["LP Preferred Return"] = tier2

    # Tier 3: GP Catch-Up (if enabled)
    tier3_gp = 0
    tier3_lp = 0

    if catchup:
        # GP catch-up amount needed to "true up" to promote % of total profits:
        profits_so_far = tier1 + tier2  # LP only so far
        target_gp_share = promote_pct / (1 - promote_pct) * profits_so_far
        tier3_gp = min(cash_remaining, target_gp_share)
        cash_remaining -= tier3_gp

    results["GP Catch-Up"] = tier3_gp

    # Tier 4: Residual Split
    tier4_lp = cash_remaining * (1 - promote_pct)
    tier4_gp = cash_remaining * promote_pct

    # Final distributions:
    total_lp = tier1 + tier2 + tier4_lp
    total_gp = gp_equity + tier3_gp + tier4_gp

    results["LP Residual Split"] = tier4_lp
    results["GP Residual Split"] = tier4_gp
    results["Total LP Distribution"] = total_lp
    results["Total GP Distribution"] = total_gp

    return results

# Compute the Waterfall:
results = waterfall_distribution(
    lp_equity=lp_equity,
    pref_rate=pref_rate,
    hold_period=hold_period,
    cash_to_equity=cash_to_equity,
    promote_pct=promote_pct,
    gp_equity=gp_equity,
    catchup=show_catchup  # this is your checkbox value
)

# Compute the IRR cash flows:
#lp_cf = [-lp_equity] + [0] * (hold_period - 1) + [results["Total LP Distribution"]]
#gp_cf = [-gp_equity] + [0] * (hold_period - 1) + [results["Total GP Distribution"]]
#project_cf = [-equity] + [0] * (hold_period - 1) + [cash_to_equity]

lp_irr = npf.irr(lp_cf)
gp_irr = npf.irr(gp_cf)
project_cf = [-equity] + [row["Cash to Equity"] for row in annual_cash_flows]
total_equity_irr = npf.irr(project_cf)

# Display the results:
st.markdown("### 📈 Waterfall Summary")

col1, col2, col3 = st.columns(3)
col1.metric("LP IRR", f"{lp_irr*100:.2f}%")
col2.metric("GP IRR", f"{gp_irr*100:.2f}%")
col3.metric("Total Equity IRR", f"{total_equity_irr*100:.2f}%")

st.write("### 💸 Distribution Breakdown")
st.write(pd.DataFrame.from_dict(results, orient="index", columns=["Amount ($)"]))

# Visualize the waterfall with chart:

# First, build tiers dynamically:
tiers = [
    ("Cash to Equity", cash_to_equity),
    ("Return of Capital (LP)", -results["LP Return of Capital"]),
    ("Preferred Return (LP)", -results["LP Preferred Return"]),
]

if show_catchup:
    tiers.append(("GP Catch-Up", -results["GP Catch-Up"]))

tiers += [
    ("Residual to LP", -results["LP Residual Split"]),
    ("Residual to GP", -results["GP Residual Split"]), #  Negative signs mean "outflow" from total--> used to simulate how cash steps down through the tiers.
]

# Then, plot the waterfall:
st.markdown("### 💧 Cash Flow Waterfall")

labels, values = zip(*tiers)
cumulative = [0]
for v in values[:-1]:
    cumulative.append(cumulative[-1] + v)

fig, ax = plt.subplots(figsize=(10, 5))

# Plot bars:
for i in range(len(values)):
    bar_color = "#1f77b4" if values[i] < 0 else "#2ca02c"
    ax.bar(labels[i], values[i], bottom=cumulative[i], color=bar_color)

    # Calculate the vertical center of the bar:
    y_pos = cumulative[i] + values[i] / 2
    # Annotate the value inside or above the bar:
    ax.text(
        i, y_pos, f"${abs(values[i]):,.0f}",
        ha='center', va='center', fontsize=10, color='white' if values[i] < 0 else 'black',
        fontweight='bold'
    )

# Labels and aesthetics:
ax.set_title("Equity Distribution at Sale: Final-Year Waterfall")
ax.set_ylabel("Dollars ($)")
ax.axhline(0, color="black", linewidth=0.8)
plt.xticks(range(len(labels)), labels, rotation=30)
st.pyplot(fig)
st.caption("This chart shows how equity is distributed at the end of the hold period, after debt is repaid and sale proceeds are realized.")


# Disclosure of my modeling assumptions:
with st.expander("📘 Modeling Assumptions"):
    st.markdown("""
    - All equity and debt are deployed at the beginning of the hold period.
    - Cash flows are modeled as a single distribution at exit (NOI + Sale Proceeds).
    - Debt is assumed to be interest-only unless otherwise selected.
    - No taxes, fees, or reversion costs are included.
    - Waterfall includes the following tiers:
        1. LP return of capital  
        2. LP preferred return (simple interest, not compounded)  
        3. GP catch-up (if enabled) to reach target promote share  
        4. Residual split per the promote structure
    - IRRs are calculated on a single-entry, single-exit cash flow basis.
    """)