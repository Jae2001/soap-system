import streamlit as st
import pandas as pd
from datetime import datetime

st.header("🗂 Ingredients Stock Module")

# Initialize stock data
if "stock_df" not in st.session_state:
    st.session_state.stock_df = pd.DataFrame(columns=[
        "Ingredient", "Quantity", "Unit", "Cost (RM)", "Expiry Date"
    ])

# --- Add new ingredient ---
st.subheader("➕ Add New Ingredient")
with st.form("add_ingredient_form"):
    name = st.text_input("Ingredient Name")
    qty = st.number_input("Quantity", min_value=0.0, step=1.0)
    unit = st.selectbox("Unit", ["ml", "g"])
    cost = st.number_input("Cost (RM)", min_value=0.0, step=0.01)
    expiry = st.date_input("Expiry Date", value=datetime.today())
    submitted = st.form_submit_button("Add Ingredient")

    if submitted:
        new_row = pd.DataFrame({
            "Ingredient": [name],
            "Quantity": [qty],
            "Unit": [unit],
            "Cost (RM)": [cost],
            "Expiry Date": [expiry]
        })
        st.session_state.stock_df = pd.concat([st.session_state.stock_df, new_row], ignore_index=True)
        st.success(f"{name} added to stock!")

# --- Current Stock Table ---
st.subheader("📦 Current Stock")
if st.session_state.stock_df.empty:
    st.info("No ingredients in stock yet.")
else:
    st.dataframe(st.session_state.stock_df)

# --- Delete or Edit Ingredient ---
st.subheader("✏️ Edit / Delete Ingredient")
if not st.session_state.stock_df.empty:
    selected = st.selectbox("Select Ingredient", st.session_state.stock_df["Ingredient"])
    row_index = st.session_state.stock_df[st.session_state.stock_df["Ingredient"] == selected].index[0]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete Selected"):
            st.session_state.stock_df = st.session_state.stock_df.drop(index=row_index).reset_index(drop=True)
            st.success(f"{selected} deleted from stock.")
    with col2:
        new_qty = st.number_input("Update Quantity", min_value=0.0, value=float(st.session_state.stock_df.loc[row_index, "Quantity"]))
        if st.button("Update Quantity"):
            st.session_state.stock_df.at[row_index, "Quantity"] = new_qty
            st.success(f"{selected} quantity updated to {new_qty}.")
