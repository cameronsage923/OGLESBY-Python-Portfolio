import streamlit as st
import pandas as pd

#Display a title:
st.title("Welcome to The Penguin App!")

#Short description of what the app does:
st.write("This app allows you to filter data collected from 344 different penguins by island, species, and body mass.")

#Sample DataFrame:
df = pd.read_csv("data/penguins.csv")

#Interactive filtering options:
island = st.selectbox("To filter by island, please select an island:", df["island"].unique())
st.write(f"Penguins in {island}:")
st.dataframe(df[df["island"] == island])

species = st.selectbox("To filter by species, please select a species:", df["species"].unique())
st.write(f"Penguins of the {species} species:")
st.dataframe(df[df["species"] == species])

body_mass_g = st.slider("Choose a maximum body mass:",
          min_value = df["body_mass_g"].min(),
          max_value = df["body_mass_g"].max())

st.write(f"Penguins with a body mass under {body_mass_g}:")
st.dataframe(df[df["body_mass_g"] <= body_mass_g])
