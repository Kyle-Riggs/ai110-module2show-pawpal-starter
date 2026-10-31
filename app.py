import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planner: add your pets, schedule their care, and see today's plan.")

# Streamlit reruns this script on every interaction, so the Owner lives in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
owner: Owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        elif any(p.name.lower() == pet_name.strip().lower() for p in owner.pets):
            st.error(f"You already have a pet named {pet_name.strip()}.")
        else:
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            st.success(f"Added {pet_name.strip()} the {species}.")

if owner.pets:
    st.write("Your pets:")
    st.table([{"Name": p.name, "Species": p.species, "Tasks": len(p.tasks)} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add a pet before scheduling tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        target = st.selectbox("Pet", [p.name for p in owner.pets])
        description = st.text_input("Task description", placeholder="Morning walk")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_time = st.time_input("Time")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        with col4:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if not description.strip():
                st.error("Please enter a task description.")
            else:
                pet = next(p for p in owner.pets if p.name == target)
                pet.add_task(
                    Task(
                        description=description.strip(),
                        time=task_time.strftime("%H:%M"),
                        frequency=frequency,
                        duration_minutes=int(duration),
                        priority=priority,
                    )
                )
                st.success(f"Added '{description.strip()}' for {target}.")

st.divider()

scheduler = Scheduler(owner)


def task_rows(entries):
    """Convert (pet, task) pairs into table rows for st.table."""
    return [
        {
            "Date": str(task.due_date),
            "Time": task.time,
            "Pet": pet.name,
            "Task": task.description,
            "Duration": f"{task.duration_minutes} min",
            "Priority": task.priority,
            "Repeats": task.frequency,
            "Done": "✅" if task.completed else "",
        }
        for pet, task in entries
    ]


st.subheader("Today's Schedule")
todays = scheduler.get_todays_schedule()
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.warning(
        f"{len(conflicts)} scheduling conflict(s) found. Two tasks share the same start time, "
        "so you can't do both at once. Move one of them to a different time:"
    )
    for message in conflicts:
        st.warning(message, icon="⚠️")
elif todays:
    st.success("No conflicts. Your schedule is clear.")

if todays:
    st.table(task_rows(todays))
else:
    st.info("Nothing scheduled for today yet.")

st.divider()

st.subheader("Complete a Task")
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))
pending = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))
if pending:
    choice = st.selectbox(
        "Pending task",
        range(len(pending)),
        format_func=lambda i: (
            f"{pending[i][1].due_date} {pending[i][1].time} - "
            f"{pending[i][0].name}: {pending[i][1].description}"
        ),
    )
    if st.button("Mark complete"):
        pet, task = pending[choice]
        next_task = scheduler.mark_task_complete(pet, task)
        if next_task:
            st.session_state.flash = (
                f"Completed '{task.description}'. Next {task.frequency} occurrence "
                f"scheduled for {next_task.due_date} at {next_task.time}."
            )
        else:
            st.session_state.flash = f"Completed '{task.description}'."
        st.rerun()  # redraw the schedule above with the updated task
else:
    st.info("No pending tasks.")

st.divider()

st.subheader("Browse All Tasks")
if owner.pets:
    col_pet, col_status = st.columns(2)
    with col_pet:
        pet_filter = st.selectbox("Pet", ["All pets"] + [p.name for p in owner.pets])
    with col_status:
        status_filter = st.selectbox("Status", ["All", "Pending", "Completed"])
    completed_value = {"All": None, "Pending": False, "Completed": True}[status_filter]
    results = scheduler.sort_by_time(
        scheduler.filter_tasks(
            pet_name=None if pet_filter == "All pets" else pet_filter,
            completed=completed_value,
        )
    )
    if results:
        st.table(task_rows(results))
    else:
        st.info("No tasks match these filters.")
else:
    st.info("Add a pet to see tasks here.")
