import json
import streamlit as st
from pathlib import Path
from gemini_helper import get_recommendations_from_gemini

DATA_FILE = Path(__file__).parent / "data" / "yojnas.json"

# ------------------- Load schemes -------------------
def load_schemes():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

schemes = load_schemes()

# ------------------- UI Setup -------------------
st.set_page_config(page_title="Yojna Mitra", page_icon="🪙", layout="centered")

st.title("Yojna Mitra")
st.caption("Personalized government scheme recommendations—AI powered.")

with st.sidebar:
    st.header("About Yojna Mitra")
    st.write("""
**Yojna Mitra** helps you discover which Indian Government Schemes
you might be eligible for.  

Just enter your basic details, and the app uses AI to suggest 
the most suitable schemes for you — simply and instantly.
""")
    st.divider()



# ------------------- Form -------------------
with st.form("user_form"):
    name = st.text_input("Name (optional)")
    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.number_input("Age", min_value=0, max_value=120, value=25)

    with c2:
        gender = st.selectbox("Gender", ["female", "male", "other"])

    with c3:
        income = st.number_input("Income (annual)", min_value=0, value=300000)

    c4, c5 = st.columns(2)
    with c4:
        state = st.text_input("State (KA, MH, DL, etc.)", value="KA")

    with c5:
        occupation = st.text_input("Occupation (e.g., student, farmer)")

    submit = st.form_submit_button("Get Recommendations")


# ------------------- Output -------------------
if submit:
    user_profile = {
        "name": name,
        "age": age,
        "gender": gender,
        "income": income,
        "state": state.upper(),
        "occupation": occupation
    }

    st.subheader("AI Recommendations")
    st.caption("🔮 Source: Gemini AI")

    response = get_recommendations_from_gemini(user_profile, schemes)
    st.info(response)

    with st.expander("🔍 User Profile Sent to AI"):
        st.json(user_profile)

    with st.expander("📚 Scheme Data Used"):
        st.json(schemes)