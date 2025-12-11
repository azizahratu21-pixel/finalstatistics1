import streamlit as st
from PIL import Image
import os

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

st.set_page_config(page_title="Team Members", page_icon="🧑‍🤝‍🧑", layout="wide")

st.title("Team Members")
st.write("Below is the list of project contributors and their responsibilities.")

team = [
    {
        "name": "Inayah Ratu Azizah",
        "role": "Project Lead",
        "photo": "assets/member1.jpeg",
        "contribution": [
            "Structured the multi-page Streamlit application.",
            "Designed the user interface and color theme.",
            "Created the homepage layout and overall navigation.",
            "Compiled documentation and organized project deliverables.",
            "Integrated different modules into the main application."
        ]
    },
    {
        "name": "Ahmad Raihanun Nabil",
        "role": "Data Processing & Analytics",
        "photo": "assets/member2.jpeg",
        "contribution": [
            "Implemented dataset upload feature.",
            "Wrote functions for descriptive statistics generation.",
            "Developed automatic correlation computation.",
            "Tested the app using multiple datasets."
        ]
    },
    {
        "name": "Novita Aulia",
        "role": "Backend Logic & Error Handling",
        "photo": "assets/member3.jpeg",
        "contribution": [
            "Managed backend functions and library dependencies.",
            "Built error-handling systems for invalid inputs.",
            "Optimized dataset loading performance.",
            "Ensured statistical functions ran smoothly and correctly."
        ]
    },
    {
        "name": "Windi Melisa Sipayung",
        "role": "Visualization & Report Specialist",
        "photo": "assets/member4.jpeg",
        "contribution": [
            "Created visualization components (tables & charts).",
            "Designed plots for correlation and distribution.",
            "Developed PDF export functionality using FPDF.",
            "Tested visual display consistency on different screens."
        ]
    }
]

for member in team:
    cols = st.columns([1, 3])  # one column for photo, one for details
    with cols[0]:
        if os.path.exists(member["photo"]):
            st.image(member["photo"], width=130)
        else:
            st.image(Image.new("RGBA", (130, 130), (200, 200, 200, 255)), caption="No photo")
    with cols[1]:
        st.subheader(member["name"])
        st.markdown(f"**Role:** {member['role']}")
        st.write("**Contributions:**")
        for item in member["contribution"]:
            st.write(f"- {item}")
    st.markdown("---")