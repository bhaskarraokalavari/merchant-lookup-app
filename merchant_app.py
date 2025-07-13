import streamlit as st
import pandas as pd

st.set_page_config(page_title="Merchant Lookup", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("merchant_data.xlsx", engine="openpyxl")
    df.columns = df.columns.str.strip()  # Remove extra spaces
    return df

df = load_data()

# --- UI ---
st.title("🔍 Merchant ID Lookup")
st.markdown("Enter Merchant ID to search. You can also filter by date if needed.")

# --- Optional: Show column names for debugging ---
# st.write("Available Columns:", df.columns.tolist())

# --- Date Filter (optional) ---
if "Date" in df.columns:
    selected_date = st.selectbox("📅 Filter by Date (optional)", ["All"] + sorted(df["Date"].astype(str).unique().tolist()))
    if selected_date != "All":
        df = df[df["Date"].astype(str) == selected_date]

# --- Merchant ID Search ---
merchant_id = st.text_input("🔎 Enter Merchant ID")

if merchant_id:
    result_df = df[df["Merchant_id"].astype(str).str.contains(merchant_id, case=False, na=False)]

    if not result_df.empty:
        st.success(f"Found {len(result_df)} result(s):")
        st.dataframe(result_df, use_container_width=True)
    else:
        st.warning("No results found for the entered Merchant ID.")
else:
    st.info("Please enter a Merchant ID to search.")

# --- Optional: Footer ---
st.markdown("---")
st.caption("📄 Data source: merchant_data.xlsx | Built with ❤️ using Streamlit")
