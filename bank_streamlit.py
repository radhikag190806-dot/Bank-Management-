import streamlit as st
import json
import random
import string
from pathlib import Path

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Bank",
    page_icon="🏦",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main-title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#00c6ff;
}

.card {
    padding:20px;
    border-radius:20px;
    background:linear-gradient(135deg,#141E30,#243B55);
    color:white;
    box-shadow:0px 0px 25px rgba(0,0,0,0.4);
    margin-bottom:15px;
}

.stButton>button {
    border-radius:12px;
    background:linear-gradient(45deg,#00c6ff,#0072ff);
    color:white;
    font-weight:bold;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- BANK CLASS ----------------

class Bank:

    database = "data.json"
    data = []

    if Path(database).exists():
        with open(database, "r") as f:
            data = json.load(f)
    else:
        with open(database, "w") as f:
            json.dump([], f)

    @classmethod
    def update(cls):
        with open(cls.database, "w") as f:
            json.dump(cls.data, f, indent=4)

    @staticmethod
    def generate_account():
        while True:
            acc = "".join(
                random.choices(string.ascii_uppercase, k=4)
                + random.choices(string.digits, k=4)
            )
            if not any(i["Account No."] == acc for i in Bank.data):
                return acc

    @staticmethod
    def find(acc, pin):
        for user in Bank.data:
            if user["Account No."] == acc and str(user["pin"]) == pin:
                return user
        return None


# ---------------- HEADER ----------------

st.markdown('<p class="main-title">🏦 Smart Bank System</p>', unsafe_allow_html=True)
st.caption("✨ Secure • Fast • Modern Banking Experience")

menu = st.sidebar.selectbox(
    "📌 Select Option",
    [
        "🏠 Home",
        "🧾 Create Account",
        "💰 Deposit",
        "💸 Withdraw",
        "📄 View Details",
        "✏️ Update",
        "❌ Delete"
    ]
)

# ---------------- HOME ----------------

if menu == "🏠 Home":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### 👋 Welcome to Smart Bank")
    st.write("Experience secure and modern digital banking.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.snow()

# ---------------- CREATE ACCOUNT ----------------

elif menu == "🧾 Create Account":

    st.subheader("🧾 Create New Account")

    name = st.text_input("👤 Name")
    email = st.text_input("📧 Email")
    phone = st.text_input("📱 Phone")
    pin = st.text_input("🔒 4 Digit PIN", type="password")

    if st.button("🚀 Create Account"):

        if len(pin) != 4 or not pin.isdigit():
            st.error("PIN must be 4 digits")

        elif len(phone) != 10 or not phone.isdigit():
            st.error("Phone must be 10 digits")

        else:
            acc = Bank.generate_account()

            user = {
                "name": name,
                "email": email,
                "phone No.": phone,
                "pin": int(pin),
                "Account No.": acc,
                "balance": 0
            }

            Bank.data.append(user)
            Bank.update()

            st.success("🎉 Account Created Successfully!")
            st.info(f"🏦 Your Account Number: {acc}")
            st.balloons()

# ---------------- DEPOSIT ----------------

elif menu == "💰 Deposit":

    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=0)

    if st.button("💵 Deposit"):

        user = Bank.find(acc, pin)

        if user:
            user["balance"] += amount
            Bank.update()
            st.success("✅ Deposit Successful")
            st.balloons()
        else:
            st.error("❌ Invalid Account or PIN")

# ---------------- WITHDRAW ----------------

elif menu == "💸 Withdraw":

    st.subheader("💸 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=0)

    if st.button("🏧 Withdraw"):

        user = Bank.find(acc, pin)

        if user:
            if user["balance"] >= amount:
                user["balance"] -= amount
                Bank.update()
                st.success("✅ Withdrawal Successful")
            else:
                st.error("❌ Insufficient Balance")
        else:
            st.error("Invalid Details")

# ---------------- VIEW DETAILS ----------------

elif menu == "📄 View Details":

    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("👁️ View Details"):

        user = Bank.find(acc, pin)

        if user:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"👤 Name: {user['name']}")
            st.write(f"📧 Email: {user['email']}")
            st.write(f"📱 Phone: {user['phone No.']}")
            st.write(f"🏦 Account: {user['Account No.']}")
            st.write(f"💰 Balance: ₹ {user['balance']}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.snow()
        else:
            st.error("❌ Invalid Account or PIN")

# ---------------- UPDATE ----------------

elif menu == "✏️ Update":

    st.subheader("✏️ Update Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    user = Bank.find(acc, pin)

    if user:
        name = st.text_input("New Name", user["name"])
        email = st.text_input("New Email", user["email"])
        phone = st.text_input("New Phone", user["phone No."])

        if st.button("🔄 Update"):

            user["name"] = name
            user["email"] = email
            user["phone No."] = phone

            Bank.update()
            st.success("✅ Updated Successfully")
            st.balloons()

# ---------------- DELETE ----------------

elif menu == "❌ Delete":

    st.subheader("❌ Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("🗑️ Delete Account"):

        user = Bank.find(acc, pin)

        if user:
            Bank.data.remove(user)
            Bank.update()
            st.success("⚠️ Account Deleted Successfully")
            st.snow()
        else:
            st.error("Invalid Details")