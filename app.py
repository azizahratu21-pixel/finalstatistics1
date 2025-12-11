import streamlit as st
import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
from PIL import Image

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(
    page_title="Statistics Project",
    layout="wide"
)

# ----------------------
# PAGE STYLING (sage green)
# ----------------------
page_bg = """
<style>
body {
    background-color: #E7F0EC; /* light sage green */
}

.main > div {
    background-color: #E7F0EC !important;
}

.sidebar .sidebar-content {
    background-color: #C9DCD3 !important; /* darker sage layer */
}

.stButton>button {
    background-color: #A9C7B8 !important;
    color: white !important;
    border-radius: 8px !important;
}

.stTabs [data-baseweb="tab"] {
    background-color: #C9DCD3 !important;
}

.stTabs [aria-selected="true"] {
    background-color: #A9C7B8 !important;
    color: white !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------
# HEADER
# ----------------------
st.title("📊 Statistics 1 – Data Analysis App")
st.write("Upload your dataset and run descriptive statistics and correlation analysis.")

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
