import pandas as pd  # For data manipulation
import numpy as np  # For numerical operations
import streamlit as st  # For creating the interactive app
import seaborn as sns  # For easy dataset loading and visualizations
import matplotlib.pyplot as plt  # For plotting
from scipy.stats import iqr # For getting the iqr

# ------------------------------------------------------------------------------
# Lecture: Data Validation, Outliers, Inconsistencies & Errors in Data
# ------------------------------------------------------------------------------
st.title("Data Validation & Data Quality Checks")
st.markdown("""
This lecture covers:
- **Data Validation:** Checking data types, missing values, and basic consistency.
- **Outlier Detection:** Using boxplots and the IQR method.
- **Identifying Inconsistencies & Errors:** Spotting duplicates and unexpected values.
""")

# ------------------------------------------------------------------------------
# Load a different dataset: the 'tips' dataset from seaborn
# ------------------------------------------------------------------------------
df = sns.load_dataset("tips")
# Appending a negative tip
df.loc[-1] = [-25, -5, "Male", "Yes", "Jan", "Midnight", 30]

st.header("1. Data Validation")
st.subheader("Data Overview")
st.write("First few rows of the dataset:")
st.code("df.head()")
st.dataframe(df.head())

st.subheader("Data Types & Missing Values")
st.write("Data Types:")
st.code("df.dtypes")
st.write(df.dtypes)
st.write("Missing Values per Column:")
st.code("df.isnull().sum()")
st.write(df.isnull().sum())

# ------------------------------------------------------------------------------
# Detecting Outliers in a Numerical Column ('total_bill')
# ------------------------------------------------------------------------------
st.header("2. Detecting Outliers")
st.subheader("Boxplot for Selected Column")

# Create a boxplot for 'total_bill'
fig1, ax1 = plt.subplots()
column = st.selectbox("Select a Column:", df.columns.unique())
sns.boxplot(x=df[column])
ax1.set_title(f"Boxplot of {column}")
st.pyplot(fig1)

# Calculate IQR for 'total_bill' to identify outliers
# Compute Q1 and Q3 using numpy
Q1, Q3 = np.percentile(df[column].dropna(), [25, 75])
IQR = iqr(df[column].dropna())

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

st.write(f"Lower Bound: {lower_bound:.2f}")
st.write(f"Upper Bound: {upper_bound:.2f}")

# Identify outliers in 'total_bill'
outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
st.write(f"Rows with outliers in '{column}':")
st.dataframe(outliers)

# ------------------------------------------------------------------------------
# Identifying Inconsistencies and Errors
# ------------------------------------------------------------------------------
st.header("3. Identifying Inconsistencies and Errors")
st.subheader("Duplicate Records")

# Check for duplicate rows in the dataset
duplicate_count = df.duplicated().sum()
st.write(f"Number of duplicate rows: {duplicate_count}")
st.dataframe(df[df.duplicated() == 1])

# For demonstration, let's simulate an inconsistency:
# Assume that a negative tip value is an error.
st.subheader("Checking for Unexpected Values in 'tip'")

# Check for negative tip values
negative_tips = df[df["tip"] < 0]
if negative_tips.empty:
    st.write("No negative tip values found.")
else:
    st.write("Negative tip values detected:")
    st.dataframe(negative_tips)

# ------------------------------------------------------------------------------
# Final Notes
# ------------------------------------------------------------------------------
st.header("Conclusion")
st.markdown("""
Validating your data is a crucial first step in any analysis.  
By checking for data type mismatches, missing values, outliers, duplicates,  
and other inconsistencies, you can ensure that your insights are based on reliable data.
""")
