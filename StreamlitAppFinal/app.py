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