import streamlit as st

st.set_page_config(page_title="Multifamily RE Deal Tool", layout="centered")

# Header Image
st.image("https://sdmntprwestus.oaiusercontent.com/files/00000000-b604-6230-bc01-3d0c87f77144/raw?se=2025-05-06T02%3A50%3A31Z&sp=r&sv=2024-08-04&sr=b&scid=957bd86b-2b03-535f-899f-f38c4d2b07a2&skoid=51916beb-8d6a-49b8-8b29-ca48ed86557e&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-05-05T17%3A38%3A05Z&ske=2025-05-06T17%3A38%3A05Z&sks=b&skv=2024-08-04&sig=z7Mor8dfg6lJ19ovsWr%2Bpfq8yqb0c55QSLVM2fIQJm8%3D", use_column_width=True, caption="Source: OpenAI")

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
st.image("sample_waterfall_distribution.png", caption="Sample Waterfall Structure", use_column_width=True)

# --- Footer or Credits ---
st.markdown("---")
st.caption("Created by Cameron Oglesby • Elements of Computing II Final Project • University of Notre Dame • Spring 2025")
