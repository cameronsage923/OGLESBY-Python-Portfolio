import streamlit as st

st.set_page_config(page_title="Multifamily RE Deal Tool", layout="centered")

# Header Image
#st.image("pictures/Fundamentals-of-Value-Add-Real-Estate-Investing-01.png", use_column_width=True, caption="Source: CRE Knowledge Base")
#st.image("pictures/RE_image.png")

# Title Section:
st.title("🏢 Real Estate Private Equity: Multifamily Value-Add Deal Modeling Lab")
st.markdown("""
Welcome to the **Multifamily Value-Add Deal Visualizer & Waterfall Modeler** — a hands-on learning tool designed to help you understand how private equity firms analyze and structure apartment building investments.

This app is built for students, aspiring investors, and anyone curious about how real estate deals are underwritten, valued, and distributed among partners.
""")

# 🧠 What is a Multifamily Value-Add Deal?
st.subheader("🔍 What is a Multifamily Value-Add Deal?")
st.markdown("""
In real estate private equity, a **multifamily value-add deal** is a strategy where investors buy an apartment building, improve it (through renovations or better management), and then sell it at a higher value.

The goal is to:
- 🚪 **Increase rents** by improving unit interiors and amenities
- 💸 **Boost Net Operating Income (NOI)** by raising revenue or cutting expenses
- 📈 **Sell the property** later at a higher price, generating strong returns for investors

This approach creates value through both **physical upgrades** and **financial optimization**.
""")

# 💻 What This App Does
st.subheader("🛠️ What This App Helps You Do")
st.markdown("""
This Streamlit-powered app lets you simulate and visualize a full investment model:

- 🧮 **Deal Visualizer**: Adjust key inputs like unit count, rent, renovations, debt, and cap rates
- 📊 **Pro Forma**: View projected income, expenses, and cash flow across the investment period
- 💧 **Waterfall Modeling**: Structure equity splits between Limited Partners (LPs) and General Partners (GPs), including preferred returns and promotes
- 📘 **Glossary**: Learn what every financial term means in plain English

You'll see how assumptions affect investor returns — and walk away with a better grasp of how real estate private equity works.
""")

# 🧭 Navigation Instructions
st.subheader("🚀 How to Get Started")
st.markdown("""
1. Head to the **📊 Deal Visualizer** page to set up your base assumptions
2. Go to **📉 Waterfall Modeling** to customize your capital stack and return splits
3. Explore the **🧾 Pro Forma** and **📘 Glossary** pages to reinforce your understanding
""")

# (Optional Image/Diagram — uncomment when ready)
# st.image("pictures/sample_waterfall_distribution.png", caption="Sample Waterfall Structure", use_column_width=True)

# 👣 Footer
st.markdown("---")
st.caption("Created by Cameron Oglesby • Elements of Computing II Final Project • University of Notre Dame • Spring 2025")
