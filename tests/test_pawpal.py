from datetime import date, timedelta

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task


@pytest.fixture
def owner():
    """An owner with two pets and no tasks."""
    o = Owner("Jordan")
    o.add_pet(Pet("Mochi", "dog"))
    o.add_pet(Pet("Luna", "cat"))
    return o


@pytest.fixture
def mochi(owner):
    return owner.pets[0]


@pytest.fixture
def luna(owner):
    return owner.pets[1]


# --- Basics ---------------------------------------------------------------


def test_mark_complete_changes_status():
    task = Task("Morning walk", "07:30")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning walk", "07:30"))

    assert len(pet.tasks) == 1


# --- Sorting ----------------------------------------------------------------


def test_sort_by_time_returns_chronological_order(owner, mochi, luna):
    mochi.add_task(Task("Evening feeding", "18:00"))
    luna.add_task(Task("Vet appointment", "14:15"))
    mochi.add_task(Task("Morning walk", "07:30"))
    luna.add_task(Task("Medication", "08:00"))

    entries = Scheduler(owner).sort_by_time(owner.get_all_tasks())

    assert [task.time for _, task in entries] == ["07:30", "08:00", "14:15", "18:00"]


def test_sort_handles_zero_padded_times_around_ten(owner, mochi):
    mochi.add_task(Task("Late", "10:00"))
    mochi.add_task(Task("Early", "09:05"))

    entries = Scheduler(owner).sort_by_time(owner.get_all_tasks())

    assert [task.description for _, task in entries] == ["Early", "Late"]


def test_todays_schedule_is_sorted_and_excludes_other_dates(owner, mochi):
    today = date.today()
    mochi.add_task(Task("Afternoon play", "15:00", due_date=today))
    mochi.add_task(Task("Morning walk", "07:30", due_date=today))
    mochi.add_task(Task("Tomorrow's walk", "06:00", due_date=today + timedelta(days=1)))

    schedule = Scheduler(owner).get_todays_schedule()

    assert [task.description for _, task in schedule] == ["Morning walk", "Afternoon play"]


def test_schedule_for_owner_with_no_tasks_is_empty(owner):
    scheduler = Scheduler(owner)

    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_pet_with_no_tasks_does_not_break_other_pets(owner, luna):
    luna.add_task(Task("Medication", "08:00"))

    entries = owner.get_all_tasks()

    assert [(pet.name, task.description) for pet, task in entries] == [("Luna", "Medication")]


# --- Recurrence -------------------------------------------------------------


def test_completing_daily_task_creates_task_for_next_day(owner, mochi):
    start = date(2026, 3, 10)
    walk = Task("Morning walk", "07:30", due_date=start, frequency="daily")
    mochi.add_task(walk)

    next_task = Scheduler(owner).mark_task_complete(mochi, walk)

    assert walk.completed is True
    assert next_task is not None
    assert next_task.due_date == start + timedelta(days=1)
    assert next_task.completed is False
    assert (next_task.description, next_task.time) == ("Morning walk", "07:30")
    assert next_task in mochi.tasks and len(mochi.tasks) == 2


def test_completing_weekly_task_creates_task_a_week_later(owner, mochi):
    start = date(2026, 3, 10)
    bath = Task("Bath", "10:00", due_date=start, frequency="weekly")
    mochi.add_task(bath)

    next_task = Scheduler(owner).mark_task_complete(mochi, bath)

    assert next_task.due_date == start + timedelta(weeks=1)


def test_completing_one_time_task_creates_no_new_task(owner, mochi):
    vet = Task("Vet appointment", "14:15", frequency="once")
    mochi.add_task(vet)

    next_task = Scheduler(owner).mark_task_complete(mochi, vet)

    assert next_task is None
    assert len(mochi.tasks) == 1


def test_daily_recurrence_rolls_over_month_end(owner, mochi):
    walk = Task("Walk", "07:00", due_date=date(2026, 1, 31), frequency="daily")
    mochi.add_task(walk)

    next_task = Scheduler(owner).mark_task_complete(mochi, walk)

    assert next_task.due_date == date(2026, 2, 1)


# --- Conflict detection -----------------------------------------------------


def test_conflict_detected_for_same_time_across_pets(owner, mochi, luna):
    mochi.add_task(Task("Grooming", "08:00"))
    luna.add_task(Task("Medication", "08:00"))

    warnings = Scheduler(owner).detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Mochi" in warnings[0] and "Luna" in warnings[0]


def test_conflict_detected_for_same_time_on_same_pet(owner, mochi):
    mochi.add_task(Task("Walk", "08:00"))
    mochi.add_task(Task("Feeding", "08:00"))

    assert len(Scheduler(owner).detect_conflicts()) == 1


def test_three_way_clash_produces_single_warning(owner, mochi, luna):
    mochi.add_task(Task("A", "09:00"))
    mochi.add_task(Task("B", "09:00"))
    luna.add_task(Task("C", "09:00"))

    assert len(Scheduler(owner).detect_conflicts()) == 1


def test_no_conflict_for_different_times(owner, mochi, luna):
    mochi.add_task(Task("Walk", "08:00"))
    luna.add_task(Task("Medication", "08:01"))

    assert Scheduler(owner).detect_conflicts() == []


def test_no_conflict_for_same_time_on_different_dates(owner, mochi):
    today = date.today()
    mochi.add_task(Task("Walk", "08:00", due_date=today))
    mochi.add_task(Task("Walk", "08:00", due_date=today + timedelta(days=1)))

    assert Scheduler(owner).detect_conflicts() == []


def test_completed_task_is_not_a_conflict(owner, mochi, luna):
    done = Task("Grooming", "08:00")
    done.mark_complete()
    mochi.add_task(done)
    luna.add_task(Task("Medication", "08:00"))

    assert Scheduler(owner).detect_conflicts() == []


# --- Filtering --------------------------------------------------------------


def test_filter_by_pet_name_is_case_insensitive(owner, mochi, luna):
    mochi.add_task(Task("Walk", "07:00"))
    luna.add_task(Task("Medication", "08:00"))

    entries = Scheduler(owner).filter_tasks(pet_name="mochi")

    assert [task.description for _, task in entries] == ["Walk"]


def test_filter_by_completion_status(owner, mochi):
    done = Task("Walk", "07:00")
    done.mark_complete()
    mochi.add_task(done)
    mochi.add_task(Task("Feeding", "18:00"))
    scheduler = Scheduler(owner)

    assert [t.description for _, t in scheduler.filter_tasks(completed=True)] == ["Walk"]
    assert [t.description for _, t in scheduler.filter_tasks(completed=False)] == ["Feeding"]


def test_filter_combines_pet_and_status(owner, mochi, luna):
    mochi.add_task(Task("Walk", "07:00"))
    luna.add_task(Task("Medication", "08:00"))

    entries = Scheduler(owner).filter_tasks(pet_name="Luna", completed=False)

    assert [task.description for _, task in entries] == ["Medication"]


def test_filter_unknown_pet_returns_empty(owner, mochi):
    mochi.add_task(Task("Walk", "07:00"))

    assert Scheduler(owner).filter_tasks(pet_name="Rex") == []
