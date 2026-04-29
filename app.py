import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import psutil
import plotly.express as px
import json
import hashlib

from scheduler import *
from ml_model import predict_best

# -------- AUTH FUNCTIONS --------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------- SESSION --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------- LOGIN SYSTEM --------
if not st.session_state.logged_in:

    st.title("🔐 AI CPU Scheduler Login System")

    option = st.radio("Choose Option", ["Login", "Signup"])

    users = load_users()

    if option == "Signup":
        st.subheader("📝 Create Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_user in users:
                st.error("⚠️ User already exists")
            else:
                users[new_user] = hash_password(new_pass)
                save_users(users)
                st.success("✅ Account created! Go to Login")

    else:
        st.subheader("🔑 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == hash_password(password):
                st.session_state.logged_in = True
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Credentials")

    st.stop()

# -------- SIDEBAR --------
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

dark_mode = st.sidebar.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }

        .stTabs [role="tab"] {
            color: white;
        }

        .stDataFrame, .stTable {
            background-color: #1e2228 !important;
            color: white !important;
        }

        div[data-testid="stMetric"] {
            background-color: #1e2228;
            padding: 10px;
            border-radius: 10px;
            color: white;
        }

        .stButton>button {
            background-color: #262730;
            color: white;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            color: #111111;
        }

        .stTabs [role="tab"] {
            color: #111111;
            font-weight: 600;
        }

        .stDataFrame, .stTable {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        div[data-testid="stMetric"] {
            background-color: #f5f7fa;
            padding: 10px;
            border-radius: 10px;
            color: #111111;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

# -------- MAIN --------
st.title("🧠 AI-Based CPU Scheduling System")
st.markdown("### Intelligent Scheduling using Machine Learning 🚀")

# -------- TABS --------
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Home",
    "⚙️ Simulator",
    "📊 Analytics",
    "💻 System Monitor"
])

# -------- HOME --------
with tab1:
    st.markdown("## Welcome 👋")
    st.info("👉 Go to Simulator tab to start")

# -------- SIMULATOR --------
with tab2:

    st.subheader("⚙️ Scheduling Simulator")

    algo_choice = st.selectbox(
        "Select Algorithm",
        ["FCFS", "SJF", "Priority", "Round Robin", "All (Compare)"]
    )

    n = st.number_input("Number of Processes", 1, 10, 3)

    processes = []
    for i in range(n):
        a = st.number_input(f"Arrival {i}", key=f"a{i}")
        b = st.number_input(f"Burst {i}", key=f"b{i}")

        if algo_choice in ["Priority", "All (Compare)"]:
            p = st.number_input(f"Priority {i}", key=f"p{i}")
        else:
            p = 0

        processes.append({'id': i, 'arrival': a, 'burst': b, 'priority': p})

    run = st.button("🚀 Run Scheduler")

    if run:
        st.session_state.ran = True

        # -------- SINGLE --------
        if algo_choice == "FCFS":
            res = fcfs(processes)
            name = "FCFS"

        elif algo_choice == "SJF":
            res = sjf(processes)
            name = "SJF"

        elif algo_choice == "Priority":
            res = priority_scheduling(processes)
            name = "Priority"

        elif algo_choice == "Round Robin":
            res = round_robin(processes)
            name = "Round Robin"

        # -------- DISPLAY CLEAN --------
        if algo_choice != "All (Compare)":

            df_res = pd.DataFrame(res)

            st.subheader(f"📊 {name} Result")
            st.dataframe(df_res)

            avg_wt = df_res["waiting"].mean()
            avg_tat = df_res["turnaround"].mean()

            col1, col2 = st.columns(2)
            col1.metric("Avg Waiting Time", round(avg_wt, 2))
            col2.metric("Avg Turnaround Time", round(avg_tat, 2))

            # ✅ FIX ADDED HERE (for Analytics tab)
            st.session_state.performance = {name: avg_wt}
            st.session_state.df = pd.DataFrame({
                "Algorithm": [name],
                "Waiting Time": [avg_wt],
                "Turnaround Time": [avg_tat]
            })
            st.session_state.best = name
            st.session_state.fcfs_res = res

            # -------- GANTT --------
            st.subheader("📅 Gantt Chart")

            fig, ax = plt.subplots()
            for p in res:
                ax.barh(1, p['burst'], left=p['start'])
                ax.text(p['start'], 1, f"P{p['id']}")

            ax.set_title(f"{name} Gantt Chart")
            ax.set_yticks([])
            ax.set_xlabel("Time")

            st.pyplot(fig)

        # -------- ALL --------
        else:
            fcfs_res = fcfs(processes)
            sjf_res = sjf(processes)
            pri_res = priority_scheduling(processes)
            rr_res = round_robin(processes)

            fcfs_avg = avg_time(fcfs_res)
            sjf_avg = avg_time(sjf_res)
            pri_avg = avg_time(pri_res)
            rr_avg = avg_time(rr_res)

            performance = {
                "FCFS": fcfs_avg[0],
                "SJF": sjf_avg[0],
                "Priority": pri_avg[0],
                "RR": rr_avg[0]
            }

            min_wt = min(performance.values())
            best_algos = [algo for algo, wt in performance.items() if wt == min_wt]

            st.session_state.performance = performance
            st.session_state.df = pd.DataFrame({
                "Algorithm": ["FCFS", "SJF", "Priority", "RR"],
                "Waiting Time": [fcfs_avg[0], sjf_avg[0], pri_avg[0], rr_avg[0]],
                "Turnaround Time": [fcfs_avg[1], sjf_avg[1], pri_avg[1], rr_avg[1]]
            })
            st.session_state.best = ", ".join(best_algos)
            st.session_state.fcfs_res = fcfs_res

            st.success("Go to Analytics tab")

# -------- ANALYTICS --------
with tab3:

    if "ran" not in st.session_state:
        st.warning("Run simulation first")

    elif "performance" in st.session_state:

        df = st.session_state.df
        perf = st.session_state.performance

        st.metric("Best Algorithm(s)", st.session_state.best)
        st.dataframe(df)

        fig = px.bar(
            x=list(perf.keys()),
            y=list(perf.values()),
            labels={'x': 'Algorithm', 'y': 'Waiting Time'}
        )

        st.plotly_chart(fig)

        st.subheader("Gantt Chart")
        fig2, ax = plt.subplots()
        for p in st.session_state.fcfs_res:
            ax.barh(1, p['burst'], left=p['start'])
        st.pyplot(fig2)

# -------- SYSTEM --------
with tab4:
    st.metric("CPU", psutil.cpu_percent())
    st.metric("Memory", psutil.virtual_memory().percent)

# -------- FOOTER --------
st.markdown("---")