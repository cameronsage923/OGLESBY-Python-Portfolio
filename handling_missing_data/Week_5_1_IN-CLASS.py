import pandas as pd            # Library for data manipulation
import seaborn as sns          # Library for statistical plotting
import matplotlib.pyplot as plt  # For creating custom plots
import streamlit as st         # Framework for building interactive web apps

# ================================================================================
#Missing Data & Data Quality Checks
#
# This lecture covers:
# - Data Validation: Checking data types, missing values, and ensuring consistency.
# - Missing Data Handling: Options to drop or impute missing data.
# - Visualization: Using heatmaps and histograms to explore data distribution.
# ================================================================================
st.title("Missing Data & Data Quality Checks")
st.markdown("""
This lecture covers:
- **Data Validation:** Checking data types, missing values, and basic consistency.
- **Missing Data Handling:** Options to drop or impute missing data.
- **Visualization:** Using heatmaps and histograms to understand data distribution.
""")

# ------------------------------------------------------------------------------
# Load the Dataset
# ------------------------------------------------------------------------------
# Read the Titanic dataset from a CSV file.
df = pd.read_csv("titanic.csv")

# ------------------------------------------------------------------------------
# Display Summary Statistics
# ------------------------------------------------------------------------------
# Show key statistical measures like mean, standard deviation, etc.
st.write("**Summary Statistics**")
st.dataframe(df.describe())
# ------------------------------------------------------------------------------
# Check for Missing Values
# ------------------------------------------------------------------------------
# Display the count of missing values for each column.
st.write("**Number of Missing Values by Column**")
st.dataframe(df.isnull().sum())  #boolean that asks if the values are null, where there 
# are no values you will get TRUE, where there are values you will get FALSE
#chain on the "sum" function to go from the actual daatframe with false and true 
#values to just a series of numbers based on our features (columns) and the total number of null values in that column.

# ------------------------------------------------------------------------------
# Visualize Missing Data
# ------------------------------------------------------------------------------
# Create a heatmap to visually indicate where missing values occur.
st.subheader("Heatmap of Missing Values")
# Step (1) give python the blank canvas (need this in streamlit to get the heatmap to work in the app):
fig, ax = plt.subplots()  
# Step (2) draw the visualization:
sns.heatmap(df.isnull(), cmap = "viridis", cbar = False)
# Step (3) reveal our visualization:
st.pyplot(fig)

# SO (1) giving python the blank canvas and (2) drawing the visualization and then (3) revealing our visualization.

# ================================================================================
# Interactive Missing Data Handling
#
# Users can select a numeric column and choose a method to address missing values.
# Options include:
# - Keeping the data unchanged
# - Dropping rows with missing values
# - Dropping columns if more than 50% of the values are missing
# - Imputing missing values with mean, median, or zero
# ================================================================================
st.subheader("Handle Missing Data")

column = st.selectbox("Choose a column to fill:",
                      df.select_dtypes(include=["number"]).columns)

method = st.radio("Choose a method:",
                  ["original DF", "Drop Rows",
                   "Impute Mean", "Impute Median", "Impute Zero"])

# Work on a copy of the DataFrame so the original data remains unchanged.
#df_clean a copy of DF that will change with the custom filters.
df_clean = df.copy()

if method == "Original DF":
    pass
elif method == "Drop Rows":
    df_clean = df_clean.dropna(subset =[column])
elif method == "Impute Mean":
    df_clean[column] = df_clean[column].fillna(df_clean[column].mean())
elif method == "Impute Median":
    df_clean[column] = df_clean[column].fillna(df_clean[column].median())
elif method == "Impute Zero":
    df_clean[column] = df_clean[column].fillna(0)


# Apply the selected method to handle missing data.
# st.dataframe(df_clean.describe())
# st.dataframe(df_clean)

# ------------------------------------------------------------------------------
# Compare Data Distributions: Original vs. Cleaned
#
# Display side-by-side histograms and statistical summaries for the selected column.
# ------------------------------------------------------------------------------
st.subheader("Cleaned Data Distribution")
fig, ax = plt.subplots() #blank canvas
sns.histplot(df_clean[column], kde=True) #drawing on canvas
st.pyplot(fig) #revealing canvas
