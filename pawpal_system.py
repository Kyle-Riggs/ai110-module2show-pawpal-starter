from collections import defaultdict
from dataclasses import dataclass, field, replace
from datetime import date, timedelta


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM"
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"  # "once", "daily", or "weekly"
    duration_minutes: int = 15
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False

    def mark_complete(self) -> "Task | None":
        """Mark this task completed and return the next occurrence if it recurs, else None."""
        self.completed = True
        if self.frequency == "daily":
            return replace(self, due_date=self.due_date + timedelta(days=1), completed=False)
        if self.frequency == "weekly":
            return replace(self, due_date=self.due_date + timedelta(weeks=1), completed=False)
        return None


@dataclass
class Pet:
    """A pet and the care tasks assigned to it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task across all pets as (pet, task) pairs."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler that reads tasks from the given owner."""
        self.owner = owner

    def get_todays_schedule(self) -> list[tuple[Pet, Task]]:
        """Return today's tasks across all pets in time order."""
        today = date.today()
        todays = [(pet, task) for pet, task in self.owner.get_all_tasks() if task.due_date == today]
        return self.sort_by_time(todays)

    def sort_by_time(self, entries: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return the (pet, task) pairs ordered by task time ("HH:MM")."""
        return sorted(entries, key=lambda entry: entry[1].time)

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet, Task]]:
        """Return tasks matching a pet name (case-insensitive) and/or completion status."""
        return [
            (pet, task)
            for pet, task in self.owner.get_all_tasks()
            if (pet_name is None or pet.name.lower() == pet_name.lower())
            and (completed is None or task.completed == completed)
        ]

    def mark_task_complete(self, pet: Pet, task: Task) -> Task | None:
        """Complete a task and, if it recurs, add its next occurrence to the pet."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> list[str]:
        """Return a warning for each date and time with more than one pending task."""
        slots: dict[tuple[date, str], list[tuple[Pet, Task]]] = defaultdict(list)
        for pet, task in self.owner.get_all_tasks():
            if not task.completed:
                slots[(task.due_date, task.time)].append((pet, task))

        return [
            f"Conflict on {day} at {time}: "
            + "; ".join(f"{pet.name} - {task.description}" for pet, task in entries)
            for (day, time), entries in sorted(slots.items())
            if len(entries) > 1
        ]
