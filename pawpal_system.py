from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    description: str
    time: str  # "HH:MM"
    due_date: date = field(default_factory=date.today)
    frequency: str = "once"  # "once", "daily", or "weekly"
    duration_minutes: int = 15
    priority: str = "medium"  # "low", "medium", or "high"
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_todays_schedule(self) -> list[tuple[Pet, Task]]:
        pass

    def sort_by_time(self, entries: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        pass

    def filter_tasks(
        self, pet_name: str | None = None, completed: bool | None = None
    ) -> list[tuple[Pet, Task]]:
        pass

    def detect_conflicts(self) -> list[str]:
        pass
