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


def main() -> None:
    owner = Owner(name="Jordan")

    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("Morning walk", "07:30", frequency="daily", duration_minutes=30, priority="high"))
    mochi.add_task(Task("Evening feeding", "18:00", frequency="daily", duration_minutes=10, priority="high"))
    luna.add_task(Task("Give medication", "08:00", frequency="daily", duration_minutes=5, priority="high"))
    luna.add_task(Task("Vet appointment", "14:15", duration_minutes=60, priority="medium"))

    print_schedule(Scheduler(owner))


if __name__ == "__main__":
    main()
