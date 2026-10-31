from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(scheduler: Scheduler) -> None:
    """Print today's schedule as a readable table."""
    print(f"Today's Schedule for {scheduler.owner.name}")
    print("=" * 62)
    print(f"{'Time':<7}{'Pet':<10}{'Task':<24}{'Dur':<8}{'Priority':<9}")
    print("-" * 62)
    for pet, task in scheduler.get_todays_schedule():
        status = "x" if task.completed else " "
        print(
            f"{task.time:<7}{pet.name:<10}{task.description:<24}"
            f"{task.duration_minutes:>3} min {task.priority:<9}[{status}]"
        )


def print_entries(title: str, entries) -> None:
    """Print a titled list of (pet, task) pairs, one per line."""
    print(f"\n{title}")
    for pet, task in entries:
        status = "done" if task.completed else "pending"
        print(f"  {task.due_date} {task.time}  {pet.name:<6} {task.description:<18} ({task.frequency}, {status})")


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added deliberately out of time order.
    mochi.add_task(Task("Evening feeding", "18:00", frequency="daily", duration_minutes=10, priority="high"))
    luna.add_task(Task("Vet appointment", "14:15", duration_minutes=60, priority="medium"))
    mochi.add_task(Task("Morning walk", "07:30", frequency="daily", duration_minutes=30, priority="high"))
    luna.add_task(Task("Give medication", "08:00", frequency="weekly", duration_minutes=5, priority="high"))
    # Same time as Luna's medication, to trigger a conflict warning.
    mochi.add_task(Task("Grooming", "08:00", duration_minutes=20, priority="low"))

    scheduler = Scheduler(owner)
    print_schedule(scheduler)

    print("\nConflict check")
    for warning in scheduler.detect_conflicts() or ["  No conflicts."]:
        print(f"  WARNING: {warning}")

    print_entries("Filter: Mochi's tasks", scheduler.filter_tasks(pet_name="Mochi"))

    walk = mochi.tasks[1]
    next_walk = scheduler.mark_task_complete(mochi, walk)
    print(f"\nCompleted '{walk.description}'; next occurrence created for {next_walk.due_date}.")
    print_entries("Filter: completed tasks", scheduler.filter_tasks(completed=True))
    print_entries("Filter: Mochi's pending tasks", scheduler.filter_tasks(pet_name="Mochi", completed=False))


if __name__ == "__main__":
    main()
