import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# -----------------------------
# Custom Sage Green Theme (CSS)
# -----------------------------
# -----------------------------
# Custom Sage Green Theme (CSS)
# -----------------------------
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


# -----------------------------
# App Title
# -----------------------------
st.title("CSV Data Analyzer ◜ᴗ◝")
st.write("Generate descriptive statistics and associations automatically.")

# -----------------------------
# Upload Dataset Section
# -----------------------------
st.header("Upload here!")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Uploaded successfully!")
    st.write("### Preview of Dataset")
    st.dataframe(df)

    # ----------------------------------------------------------
    # Feature Selection Container (Darker Sage Green Background)
    # ----------------------------------------------------------
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)

    st.subheader("Descriptive Statistics")

    st.write("#### Summary Statistics")
    st.write(df.describe())

    st.write("#### Frequency Tables (for categorical columns)")
    for col in df.select_dtypes(include=["object", "category"]).columns:
        st.write(f"**{col}**")
        st.write(df[col].value_counts())
        st.write(df[col].value_counts(normalize=True) * 100)

    # -----------------------------
    # Optional Histograms
    # -----------------------------
    st.write("### Histograms")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    selected_col = st.selectbox("Choose a numeric column to plot", numeric_cols)

    if selected_col:
        fig, ax = plt.subplots()
        ax.hist(df[selected_col])
        ax.set_title(f"Histogram of {selected_col}")
        st.pyplot(fig)

    # Boxplot
    st.write("### Boxplot (Numeric Columns)")
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.boxplot(df[col].dropna())
        ax.set_title(f"Boxplot of {col}")
        st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

     # --------------------------------------------------------
    # COMPOSITE SCORES (X_total & Y_total)
    # --------------------------------------------------------
    st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
    st.subheader("🧮 Composite Scores")

    st.write("Select items for X_total and Y_total:")

    x_items = st.multiselect("Select X items:", df.columns)
    y_items = st.multiselect("Select Y items:", df.columns)

    if len(x_items) > 0:
        df["X_total"] = df[x_items].sum(axis=1)
        st.write("X_total added to dataset ✔")

    if len(y_items) > 0:
        df["Y_total"] = df[y_items].sum(axis=1)
        st.write("Y_total added to dataset ✔")

    st.dataframe(df)
    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # ASSOCIATION ANALYSIS
    # --------------------------------------------------------
    st.markdown("<div class='feature-box'>", unsafe_allow_html=True)
    st.subheader("🔗 Association Analysis")

    method = st.selectbox(
        "Choose correlation method:",
        ["Pearson Correlation", "Spearman Rank Correlation", "Chi-square Test"]
    )

    if method in ["Pearson Correlation", "Spearman Rank Correlation"]:
        if "X_total" in df.columns and "Y_total" in df.columns:
            x = df["X_total"]
            y = df["Y_total"]

            if method == "Pearson Correlation":
                r, p = stats.pearsonr(x, y)
                test_name = "Pearson Correlation"
            else:
                r, p = stats.spearmanr(x, y)
                test_name = "Spearman Rank Correlation"

            st.write(f"### {test_name} Results")
            st.write(f"**Correlation coefficient (r):** {r:.3f}")
            st.write(f"**p-value:** {p:.4f}")

            # Interpretation
            if abs(r) < 0.2:
                strength = "very weak"
            elif abs(r) < 0.4:
                strength = "weak"
            elif abs(r) < 0.6:
                strength = "moderate"
            elif abs(r) < 0.8:
                strength = "strong"
            else:
                strength = "very strong"

            direction = "positive" if r > 0 else "negative"

            st.write(f"**Interpretation:** {strength}, {direction} correlation.")

    else:  # Chi-square
        st.write("### Chi-square Test for Categorical Variables")
        cat1 = st.selectbox("Select first categorical variable:", df.columns)
        cat2 = st.selectbox("Select second categorical variable:", df.columns)

        contingency = pd.crosstab(df[cat1], df[cat2])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)

        st.write("Chi-square statistic:", chi2)
        st.write("p-value:", p)
        st.write("Degrees of freedom:", dof)
        st.write("Expected frequencies:")
        st.write(expected)

    st.markdown("</div>", unsafe_allow_html=True)