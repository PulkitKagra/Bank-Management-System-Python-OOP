import streamlit as st
import json
import random
import string
from pathlib import Path


class Bank:
    datapath = "data.json"

    @classmethod
    def load_data(cls):
        if Path(cls.datapath).exists():
            try:
                with open(cls.datapath, "r") as f:
                    return json.load(f)
            except:
                return []
        return []

    @classmethod
    def save_data(cls):
        with open(cls.datapath, "w") as f:
            json.dump(st.session_state.data, f, indent=4)

    @staticmethod
    def generate_account():
        return ''.join(random.choices(string.digits, k=12))

    @staticmethod
    def find_user(acc_no, pin):
        for user in st.session_state.data:
            if user["account_no"] == acc_no and user["pin"] == pin:
                return user
        return None


# Load data once
if "data" not in st.session_state:
    st.session_state.data = Bank.load_data()

st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "View Details",
        "Update Details",
        "Delete Account"
    ]
)

# ---------------- CREATE ACCOUNT ----------------
if menu == "Create Account":

    st.header("Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create Account"):

        if age < 18:
            st.error("Age must be at least 18.")

        elif len(phone) != 10:
            st.error("Phone number must contain 10 digits.")

        elif len(pin) != 4:
            st.error("PIN must be 4 digits.")

        else:
            new_user = {
                "Name": name,
                "age": age,
                "mail": email,
                "phone": phone,
                "pin": int(pin),
                "account_no": Bank.generate_account(),
                "balance": 0
            }

            st.session_state.data.append(new_user)
            Bank.save_data()

            st.balloons()

            st.success("🎉 Congratulations! Your bank account has been created successfully.")

            st.warning("⚠️ Please save your Account Number carefully. It will be required for deposits, withdrawals, updates, and account access.")

            st.code(new_user["account_no"], language=None)

            st.write(f"💰 Initial Balance: ₹{new_user['balance']}")


# ---------------- DEPOSIT ----------------
elif menu == "Deposit Money":

    st.header("Deposit Money")

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)
    amount = st.number_input("Amount", min_value=0 , step=1)

    if st.button("Deposit"):

        user = Bank.find_user(acc_no, int(pin))

        if not user:
            st.error("Invalid account number or PIN.")

        elif amount <= 0:
            st.error("Please enter an amount greater than 0.")

        elif amount > 10000:
            st.error("Maximum deposit limit is ₹10,000.")    

        else:
            user["balance"] += amount
            Bank.save_data()
            st.success("Money deposited successfully!")


# ---------------- WITHDRAW ----------------
elif menu == "Withdraw Money":

    st.header("Withdraw Money")

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)
    amount = st.number_input("Amount", min_value=0)

    if st.button("Withdraw"):

        user = Bank.find_user(acc_no, int(pin))

        if not user:
            st.error("Invalid account number or PIN.")

        elif user["balance"] < amount:
            st.error("Insufficient balance.")

        else:
            user["balance"] -= amount
            Bank.save_data()
            st.success("Money withdrawn successfully!")


# ---------------- VIEW DETAILS ----------------
elif menu == "View Details":

    st.header("Account Details")

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)

    if st.button("Show Details"):

        user = Bank.find_user(acc_no, int(pin))

        if not user:
            st.error("Invalid account.")

        else:
            st.json(user)


# ---------------- UPDATE ----------------
elif menu == "Update Details":

    st.header("Update Details")

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)

    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_phone = st.text_input("New Phone")
    new_pin = st.text_input("New PIN")

    if st.button("Update"):

        user = Bank.find_user(acc_no, int(pin))

        if not user:
            st.error("Invalid account.")

        else:

            if new_name:
                user["Name"] = new_name

            if new_email:
                user["mail"] = new_email

            if new_phone:
                user["phone"] = new_phone

            if new_pin:
                user["pin"] = int(new_pin)

            Bank.save_data()
            st.success("Details updated successfully!")


# ---------------- DELETE ----------------
elif menu == "Delete Account":

    st.header("Delete Account")

    acc_no = st.text_input("Account Number")
    pin = st.number_input("PIN", step=1)

    if st.button("Delete"):

        user = Bank.find_user(acc_no, int(pin))

        if not user:
            st.error("Invalid account.")

        else:
            st.session_state.data.remove(user)
            Bank.save_data()
            st.success("Account deleted successfully!")