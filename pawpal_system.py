from dataclasses import dataclass, field
from datetime import date


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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


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
        """Return tasks matching a pet name and/or completion status (Phase 4)."""
        raise NotImplementedError

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for tasks scheduled at the same time (Phase 4)."""
        raise NotImplementedError
