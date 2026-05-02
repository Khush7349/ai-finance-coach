import streamlit as st
import requests
import pandas as pd
API = "http://localhost:8000/api/v1"
st.set_page_config(
    page_title="AI Finance Coach",
    layout="wide",
    page_icon="💰"
)
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background: #161b22;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
    margin-bottom: 15px;
}
.metric {
    font-size: 28px;
    font-weight: bold;
}
.chat-user {
    background: #1f6feb;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.chat-ai {
    background: #30363d;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)
st.sidebar.title("💰 Finance Coach")
page = st.sidebar.radio(
    "Navigate",
    ["Dashboard", "Transactions", "Insights", "AI Chat", "Goals"]
)
if page == "Dashboard":
    st.title("📊 Financial Overview")
    try:
        res = requests.get(f"{API}/transactions").json()
        df = pd.DataFrame(res["data"])
        total_spent = res["summary"]["total_spent"]
        total_records = res["meta"]["total_records"]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="card"><div class="metric">₹{total_spent}</div>Total Spending</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="card"><div class="metric">{total_records}</div>Total Transactions</div>', unsafe_allow_html=True)
        st.subheader("📊 Category Spending")
        cat = df.groupby("category")["amount"].sum()
        st.bar_chart(cat)
        st.subheader("📈 Monthly Trend")
        df["date"] = pd.to_datetime(df["date"])
        monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum()
        st.line_chart(monthly)
    except:
        st.error("⚠️ Backend not reachable")
elif page == "Transactions":
    st.title("📋 Transactions")
    try:
        res = requests.get(f"{API}/transactions").json()
        df = pd.DataFrame(res["data"])
        st.dataframe(df, use_container_width=True)
    except:
        st.error("Error loading data")
elif page == "Insights":
    st.title("🧠 AI Insights")
    if st.button("Generate Insights"):
        with st.spinner("Analyzing your finances..."):
            try:
                res = requests.get(f"{API}/insights").json()
                st.markdown("### 📊 Summary")
                st.markdown(f'<div class="card">{res["summary"]}</div>', unsafe_allow_html=True)
                st.markdown("### ⚠️ Anomalies")
                st.json(res["anomalies"])
                st.markdown("### 💡 Analysis")
                st.markdown(f'<div class="card">{res["analysis"]}</div>', unsafe_allow_html=True)
            except:
                st.error("Failed to generate insights")
elif page == "AI Chat":
    st.title("🤖 Finance Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    user_input = st.text_input("Ask your question")
    if st.button("Ask") and user_input:
        try:
            res = requests.post(
                f"{API}/chat",
                json={"question": user_input}
            ).json()
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("ai", res["response"]))
        except:
            st.error("AI not reachable")
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f'<div class="chat-user">👤 {msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai">🤖 {msg}</div>', unsafe_allow_html=True)
elif page == "Goals":
    st.title("🎯 Savings Planner")
    target = st.number_input("Target Amount (₹)", min_value=1000, step=1000)
    months = st.slider("Duration (months)", 1, 24)
    if st.button("Generate Plan"):
        with st.spinner("Calculating your plan..."):
            try:
                res = requests.post(
                    f"{API}/goals",
                    json={"target": target, "months": months}
                ).json()

                st.markdown("### 📊 Plan")
                st.markdown(f'<div class="card">{res["plan"]}</div>', unsafe_allow_html=True)

                st.markdown("### 💡 Advice")
                st.markdown(f'<div class="card">{res["advice"]}</div>', unsafe_allow_html=True)

            except:
                st.error("Error generating plan")