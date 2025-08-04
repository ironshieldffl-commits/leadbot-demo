import streamlit as st
import pandas as pd
import os
from datetime import datetime

CSV_PATH = os.path.expanduser("~/Desktop/leadbot_demo_leads.csv")
FIELDS = [
    "Timestamp", "Name", "Phone", "Email", "DOB",
    "State", "Lead Type", "Budget", "Beneficiary", "Contact Method"
]

if not os.path.isfile(CSV_PATH):
    pd.DataFrame(columns=FIELDS).to_csv(CSV_PATH, index=False)

@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

st.set_page_config(page_title="LeadBot Demo", layout="wide")
st.title("IronShield LeadBot Demo")

tab1, tab2 = st.tabs(["📊 Dashboard", "🆕 New Lead"])

with tab1:
    st.subheader("Leads Received")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="leadbot_leads.csv")

with tab2:
    st.subheader("Submit a New Lead")
    with st.form("lead_form"):
        name    = st.text_input("Name")
        phone   = st.text_input("Phone")
        email   = st.text_input("Email")
        dob     = st.date_input("DOB")
        state   = st.selectbox("State", options=[
            "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA",
            "HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
            "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
            "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
            "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"
        ])
        lead_ty = st.selectbox("Lead Type", ["Veteran","Trucker","IUL"])
        budget  = st.number_input("Monthly Budget ($)", min_value=0)
        bene    = st.selectbox("Beneficiary", ["Spouse","Child","Parents","Other"])
        contact = st.selectbox("Contact Method", ["Call","Text","Email"])
        submit  = st.form_submit_button("Submit Lead")

    if submit:
        new_row = {
            "Timestamp": datetime.now().strftime("%m/%d/%Y %H:%M"),
            "Name": name,
            "Phone": phone,
            "Email": email,
            "DOB": dob.strftime("%m/%d/%Y"),
            "State": state,
            "Lead Type": lead_ty,
            "Budget": budget,
            "Beneficiary": bene,
            "Contact Method": contact,
        }
        df2 = df.append(new_row, ignore_index=True)
        df2.to_csv(CSV_PATH, index=False)
        st.success("Lead submitted!")
        st.experimental_rerun()
