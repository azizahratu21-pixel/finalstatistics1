import streamlit as st
import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
from PIL import Image

page_bg = """
<style>

html, body, [class*="css"]  {
    background-color: #DDE5D5 !important;   
}

.stApp {
    background-color: #DDE5D5 !important;
}

/* Removes the white top navbar/header */
header[data-testid="stHeader"] {
    background-color: #DDE5D5 !important;
}

/* Removes the white padding above main content */
main[data-testid="stMain"] {
    background-color: #DDE5D5 !important;
    padding-top: 0 !important;
}

/* Main container background */
.block-container {
    background-color: #DDE5D5 !important;
    padding-top: 1rem !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #DDE5D5 !important;
}

/* The darker sage green layer box */
.feature-box {
    background-color: #C3D1C0;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-top: 25px;
}

/* Optional: remove white gap around sidebar */
section[data-testid="stSidebar"] > div:first-child {
    background-color: #DDE5D5 !important;
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------
# HEADER
# ----------------------
st.title("📊 Statistics 1 – Data Analysis App")
st.write("This is a data analysis app that allows users to upload a CSV dataset and perform descriptive statistical and correlation analysis. The app provides dataset previews, summary statistics, frequency and percentage tables, visualizations (histograms and boxplots), and evaluates the strength and direction of relationships between numeric variables using Pearson or Spearman correlation, complete with statistical interpretation.")
st.write("Upload the CSV file here!")

# ----------------------
# FILE UPLOAD
# ----------------------
uploaded = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("Preview of Dataset")
    st.dataframe(df)

    # ----------------------
    # SELECT X and Y VARIABLES
    # ----------------------
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    st.subheader("Select Variables for Analysis")

    col1, col2 = st.columns(2)
    with col1:
        X_var = st.selectbox("Select X variable", numeric_cols)
    with col2:
        Y_var = st.selectbox("Select Y variable", numeric_cols)

    # ----------------------
    # DESCRIPTIVE STATISTICS
    # ----------------------
    st.subheader("📌 Descriptive Statistics (Each Item + Composite Scores)")

    desc = df.describe().T
    st.dataframe(desc)

    # frequency tables
    st.subheader("Frequency & Percentage Tables")
    for col in numeric_cols:
        st.write(f"### {col}")
        freq = df[col].value_counts().rename("Frequency")
        perc = df[col].value_counts(normalize=True).rename("Percentage")
        st.dataframe(pd.concat([freq, perc], axis=1))

    # histograms
    st.subheader("📊 Histograms")
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.hist(df[col], bins=7)
        ax.set_title(f"Histogram of {col}")
        st.pyplot(fig)

    # boxplots
    st.subheader("📦 Boxplots")
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.boxplot(df[col])
        ax.set_title(f"Boxplot of {col}")
        st.pyplot(fig)

    # ----------------------
    # CORRELATION ANALYSIS
    # ----------------------
    st.subheader("🔗 Association Analysis (Correlation)")

    method = st.selectbox(
        "Select correlation method",
        ["Pearson", "Spearman"]
    )

    if method == "Pearson":
        result = pg.corr(df[X_var], df[Y_var], method="pearson")
    else:
        result = pg.corr(df[X_var], df[Y_var], method="spearman")

    st.write("### Correlation Output")
    st.dataframe(result)

    # Interpretation
    r = float(result["r"])
    p = float(result["p-val"])

    st.write("### Interpretation")

    # strength
    if abs(r) < 0.2:
        strength = "Very Weak"
    elif abs(r) < 0.4:
        strength = "Weak"
    elif abs(r) < 0.6:
        strength = "Moderate"
    elif abs(r) < 0.8:
        strength = "Strong"
    else:
        strength = "Very Strong"

    direction = "Positive" if r > 0 else "Negative"

    st.write(f"- **Direction:** {direction}")
    st.write(f"- **Strength:** {strength}")
    st.write(f"- **p-value:** {p:.4f}")

# END





