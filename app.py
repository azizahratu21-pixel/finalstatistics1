import streamlit as st
import pandas as pd
import numpy as np
import pingouin as pg
import matplotlib.pyplot as plt
from PIL import Image
from languages import LANG

# ----------------------
# PAGE CONFIG
# ----------------------
st.set_page_config(page_title="Multi Language App")

# ----------------------
# LANGUAGE STATE
# ----------------------
if "lang" not in st.session_state:
    st.session_state.lang = "id"

lang_choice = st.sidebar.radio(
    "Language / Bahasa",
    ["id", "en"],
    index=0 if st.session_state.lang == "id" else 1
)
st.session_state.lang = lang_choice

T = LANG[st.session_state.lang]

# ----------------------
# CSS
# ----------------------
page_bg = """
<style>
html, body, [class*="css"]  {
    background-color: #DDE5D5 !important;   
}
.stApp {
    background-color: #DDE5D5 !important;
}
header[data-testid="stHeader"] {
    background-color: #DDE5D5 !important;
}
main[data-testid="stMain"] {
    background-color: #DDE5D5 !important;
    padding-top: 0 !important;
}
.block-container {
    background-color: #DDE5D5 !important;
    padding-top: 1rem !important;
}
[data-testid="stSidebar"] {
    background-color: #DDE5D5 !important;
}
.feature-box {
    background-color: #C3D1C0;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-top: 25px;
}
section[data-testid="stSidebar"] > div:first-child {
    background-color: #DDE5D5 !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------
# HEADER
# ----------------------
st.title(T["app_title"])
st.write(T["app_desc"])

# ----------------------
# FILE UPLOAD
# ----------------------
uploaded = st.file_uploader(T["upload"], type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    st.subheader(T["preview"])
    st.dataframe(df)

    # ----------------------
    # SELECT VARIABLES
    # ----------------------
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    st.subheader(T["select_vars"])

    col1, col2 = st.columns(2)
    with col1:
        X_var = st.selectbox(T["select_x"], numeric_cols)
    with col2:
        Y_var = st.selectbox(T["select_y"], numeric_cols)

    # ----------------------
    # DESCRIPTIVE STATISTICS
    # ----------------------
    st.subheader(T["desc_stats"])
    desc = df.describe().T
    st.dataframe(desc)

    # ----------------------
    # FREQUENCY TABLES
    # ----------------------
    st.subheader(T["freq_table"])
    for col in numeric_cols:
        st.write(f"### {col}")
        freq = df[col].value_counts().rename(T["frequency"])
        perc = df[col].value_counts(normalize=True).rename(T["percentage"])
        st.dataframe(pd.concat([freq, perc], axis=1))

    # ----------------------
    # HISTOGRAMS
    # ----------------------
    st.subheader(T["histogram"])
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.hist(df[col], bins=7)
        ax.set_title(f"{T['hist_of']} {col}")
        st.pyplot(fig)

    # ----------------------
    # BOXPLOTS
    # ----------------------
    st.subheader(T["boxplot"])
    for col in numeric_cols:
        fig, ax = plt.subplots()
        ax.boxplot(df[col])
        ax.set_title(f"{T['box_of']} {col}")
        st.pyplot(fig)

    # ----------------------
    # CORRELATION
    # ----------------------
    st.subheader(T["correlation"])

    method = st.selectbox(
        T["select_method"],
        ["Pearson", "Spearman"]
    )

    if method == "Pearson":
        result = pg.corr(df[X_var], df[Y_var], method="pearson")
    else:
        result = pg.corr(df[X_var], df[Y_var], method="spearman")

    st.write(T["corr_output"])
    st.dataframe(result)

    # ----------------------
    # INTERPRETATION
    # ----------------------
    r = float(result["r"])
    p = float(result["p-val"])

    st.write(T["interpretation"])

    if abs(r) < 0.2:
        strength = T["very_weak"]
    elif abs(r) < 0.4:
        strength = T["weak"]
    elif abs(r) < 0.6:
        strength = T["moderate"]
    elif abs(r) < 0.8:
        strength = T["strong"]
    else:
        strength = T["very_strong"]

    direction = T["positive"] if r > 0 else T["negative"]

    st.write(f"- **{T['direction']}**: {direction}")
    st.write(f"- **{T['strength']}**: {strength}")
    st.write(f"- **{T['p_value']}**: {p:.4f}")











