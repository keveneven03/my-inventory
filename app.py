import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Page Setup
st.set_page_config(page_title="Fleet Tracker", layout="wide")
st.title("🏥 Equipment & Loaner Tracker")

# Connect to Google Sheets
url = "https://docs.google.com/spreadsheets/d/1V-3BF0ON6fzOehMn56R5w4khP2WjAF-kp8QZzPlcLgU/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Read Data
df = conn.read(spreadsheet=url, worksheet="Inventory")

# Dashboard Metrics
in_stock = len(df[df['Status'] == 'In Stock'])
on_loan = len(df[df['Status'] == 'On Loan'])
st.sidebar.metric("Units In Stock", in_stock)
st.sidebar.metric("Units On Loan", on_loan)

# Search & Filter
search = st.text_input("Search Serial Number or Model")
status_filter = st.multiselect("Filter by Status", options=df['Status'].unique(), default=df['Status'].unique())

mask = (df['Status'].isin(status_filter))
if search:
    mask &= df['Serial Number'].str.contains(search, case=False) | df['Model'].str.contains(search, case=False)

st.dataframe(df[mask], use_container_width=True, hide_index=True)
