import streamlit as st
import json, os
from datetime import date, datetime

# -----------------------------
# Config
# -----------------------------
DATA_FILE = "tasks.json"

# -----------------------------
# Storage helpers
# -----------------------------
def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2, default=str)  # store date as string

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📝 To-Do List with Deadlines")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# Manual add
new_task = st.text_input("Add a new task:")
priority = st.selectbox("Priority", ["Low", "Medium", "High"])
due_date = st.date_input("Due Date", value=date.today())

if st.button("➕ Add Task") and new_task.strip():
    st.session_state.tasks.append({
        "task": new_task.strip(),
        "done": False,
        "priority": priority,
        "due_date": str(due_date)
    })
    save_tasks(st.session_state.tasks)
    st.success("Task added!")
    st.rerun()

# Sorting logic (priority + due date)
priority_order = {"High": 0, "Medium": 1, "Low": 2}
def sort_key(task):
    return (
        priority_order[task["priority"]],
        datetime.strptime(task["due_date"], "%Y-%m-%d")
    )

st.session_state.tasks.sort(key=sort_key)

# Show tasks
st.subheader("Your Tasks")
for i, task in enumerate(st.session_state.tasks):
    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    checked = st.checkbox(
        f"{task['task']}  [{task['priority']}]  ⏳ {due}", 
        value=task["done"], key=i
    )
    st.session_state.tasks[i]["done"] = checked

if st.button("💾 Save Progress"):
    save_tasks(st.session_state.tasks)
    st.success("Tasks saved!")

# Manual organize button
if st.button("✨ Organize Manually"):
    pending = [t for t in st.session_state.tasks if not t["done"]]
    done = [t for t in st.session_state.tasks if t["done"]]

    st.markdown("### 📌 Suggestions")
    st.markdown("**Pending (sorted by priority & deadline):**")
    for t in pending:
        due = datetime.strptime(t["due_date"], "%Y-%m-%d").date()
        st.write(f"- {t['task']} ({t['priority']}, ⏳ {due})")

    st.markdown("**✅ Completed:**")
    for t in done:
        st.write(f"- {t['task']}")

# Clear all
if st.button("🗑️ Clear All"):
    st.session_state.tasks = []
    save_tasks(st.session_state.tasks)
    st.warning("All tasks cleared!")
    st.rerun()
