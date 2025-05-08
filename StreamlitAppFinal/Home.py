import streamlit as st

st.set_page_config(page_title="Multifamily RE Deal Tool", layout="centered")

# Header Image
st.image("pictures/RE_image.png", caption="Source: CRE Knowledge Base", use_column_width=True)

# Title Section:
st.title("🏢 Real Estate Private Equity: Multifamily Value-Add Deal Modeling Lab")
st.markdown("""
Welcome to the **Multifamily Value-Add Deal Visualizer & Waterfall Modeler**! This app is a Streamlit-powered financial analysis tool for real estate private equity deals.

Whether you're underwriting your first deal or testing promote structures, this app allows you to:
- 🧮 Model rent growth, renovation costs, and value creation
- 💧 Simulate equity waterfalls and IRR splits
- 📈 Visualize your deal's financials clearly
""")

# --- Navigation Instructions ---
st.header("To Get Started:")
st.markdown("""
1. Click the **📊 Deal Visualizer** page on the sidebar to model acquisition, rent, and renovation assumptions.
2. Then, head to **📉 Waterfall Modeling** to customize your capital stack, simulate LP/GP IRRs, and view equity distributions.
""")

# --- Optional Image or Diagram ---
st.image("pictures/sample_waterfall_distribution.png", caption="Sample Waterfall Structure", use_column_width=True)

# --- Footer or Credits ---
st.markdown("---")
st.caption("Created by Cameron Oglesby • Elements of Computing II Final Project • University of Notre Dame • Spring 2025")
