import streamlit as st
import pandas as pd

#Display a title:
st.title()

#Short description of what the app does:


#Sample DataFrame:
st.write("Here's a simple table about penguins:")
df = pd.read_csv("data\penguins.csv")
st.dataframe(df)

#Interactive filtering options: