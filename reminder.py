import streamlit as st
import datetime as dt
from plyer import notification
import os

# Log file
LOGFILE = os.path.join(os.path.expanduser("~"), "water_log.txt")

# Ensure file exists
if not os.path.exists(LOGFILE):
    with open(LOGFILE, "w") as f:
        f.write("date,time,ml\n")

# Helper: read log
def read_log():
    with open(LOGFILE, "r") as f:
        lines = f.readlines()[1:]  # skip header
    records = []
    for line in lines:
        parts = line.strip().split(",")
        if len(parts) == 3:
            records.append(parts)
    return records

# Helper: write new intake
def log_intake(ml):
    now = dt.datetime.now()
    with open(LOGFILE, "a") as f:
        f.write(f"{now.date()},{now.strftime('%H:%M:%S')},{ml}\n")

notification.notify(
    title="💧 Drink Water",
    message="Time to take a sip!",
    timeout=68  # seconds
)
      

# Config
GOAL_ML = 2500
SIP_ML = 250
today = str(dt.date.today())

# UI
st.title("💧 Drink Water Reminder")
st.write(f"Daily Goal: {GOAL_ML} ml")

# Read today’s total
records = read_log()
total_today = sum(int(r[2]) for r in records if r[0] == today)

# Progress
progress = min(1.0, total_today / GOAL_ML)
st.progress(progress)
st.write(f"Today’s intake: {total_today} ml")

# Log fixed sip
if st.button(f"Log {SIP_ML} ml"):
    log_intake(SIP_ML)
    st.rerun()


# Custom amount
ml = st.number_input("Custom amount (ml)", min_value=50, max_value=1000, step=50)
if st.button("Log custom amount"):
    log_intake(ml)
    st.rerun()


# Show history (raw)
st.subheader("History (last 10 entries)")
records = read_log()[-10:]
for r in records:
    st.write(f"{r[0]} {r[1]} → {r[2]} ml")
