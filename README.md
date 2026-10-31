# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output of `python main.py` (`[ ]` = not yet completed):

```
Today's Schedule for Jordan
==============================================================
Time   Pet       Task                    Dur     Priority 
--------------------------------------------------------------
07:30  Mochi     Morning walk             30 min high     [ ]
08:00  Mochi     Grooming                 20 min low      [ ]
08:00  Luna      Give medication           5 min high     [ ]
14:15  Luna      Vet appointment          60 min medium   [ ]
18:00  Mochi     Evening feeding          10 min high     [ ]

Conflict check
  WARNING: Conflict on 2026-10-31 at 08:00: Mochi - Grooming; Luna - Give medication

Filter: Mochi's tasks
  2026-10-31 18:00  Mochi  Evening feeding    (daily, pending)
  2026-10-31 07:30  Mochi  Morning walk       (daily, pending)
  2026-10-31 08:00  Mochi  Grooming           (once, pending)

Completed 'Morning walk'; next occurrence created for 2026-11-01.

Filter: completed tasks
  2026-10-31 07:30  Mochi  Morning walk       (daily, done)

Filter: Mochi's pending tasks
  2026-10-31 18:00  Mochi  Evening feeding    (daily, pending)
  2026-10-31 08:00  Mochi  Grooming           (once, pending)
  2026-11-01 07:30  Mochi  Morning walk       (daily, pending)
```

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The suite in `tests/test_pawpal.py` has 21 tests covering:

- **Basics:** `Task.mark_complete()` changes status; `Pet.add_task()` increases the task count.
- **Sorting:** tasks come back in chronological order across pets, zero-padded times sort correctly (`09:05` before `10:00`), and today's schedule excludes tasks due on other dates.
- **Recurrence:** completing a daily task creates one due the next day, a weekly task one week later, a `once` task creates nothing, and a daily task on Jan 31 rolls over to Feb 1.
- **Conflict detection:** same time on different pets or the same pet is flagged, a three-way clash gives one warning, and different times, different dates, and already-completed tasks are not flagged.
- **Filtering:** by pet name (case-insensitive), by completion status, by both, and for an unknown pet.
- **Empty cases:** an owner with no tasks and a pet with no tasks.

Sample test output:

```
============================= test session starts =============================
collecting ... collected 21 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  4%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [  9%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 14%]
tests/test_pawpal.py::test_sort_handles_zero_padded_times_around_ten PASSED [ 19%]
tests/test_pawpal.py::test_todays_schedule_is_sorted_and_excludes_other_dates PASSED [ 23%]
tests/test_pawpal.py::test_schedule_for_owner_with_no_tasks_is_empty PASSED [ 28%]
tests/test_pawpal.py::test_pet_with_no_tasks_does_not_break_other_pets PASSED [ 33%]
tests/test_pawpal.py::test_completing_daily_task_creates_task_for_next_day PASSED [ 38%]
tests/test_pawpal.py::test_completing_weekly_task_creates_task_a_week_later PASSED [ 42%]
tests/test_pawpal.py::test_completing_one_time_task_creates_no_new_task PASSED [ 47%]
tests/test_pawpal.py::test_daily_recurrence_rolls_over_month_end PASSED  [ 52%]
tests/test_pawpal.py::test_conflict_detected_for_same_time_across_pets PASSED [ 57%]
tests/test_pawpal.py::test_conflict_detected_for_same_time_on_same_pet PASSED [ 61%]
tests/test_pawpal.py::test_three_way_clash_produces_single_warning PASSED [ 66%]
tests/test_pawpal.py::test_no_conflict_for_different_times PASSED        [ 71%]
tests/test_pawpal.py::test_no_conflict_for_same_time_on_different_dates PASSED [ 76%]
tests/test_pawpal.py::test_completed_task_is_not_a_conflict PASSED       [ 80%]
tests/test_pawpal.py::test_filter_by_pet_name_is_case_insensitive PASSED [ 85%]
tests/test_pawpal.py::test_filter_by_completion_status PASSED            [ 90%]
tests/test_pawpal.py::test_filter_combines_pet_and_status PASSED         [ 95%]
tests/test_pawpal.py::test_filter_unknown_pet_returns_empty PASSED       [100%]

============================= 21 passed in 0.03s ==============================
```

**Confidence Level: ★★★★☆ (4/5).** The core scheduling logic is covered on both happy paths and edge cases, and all 21 tests pass. I stopped short of five stars because conflict detection only matches exact start times (overlapping durations are not caught), times are not validated (`"8:00"` or `"25:99"` would be accepted), and the Streamlit UI is not covered by automated tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()` | Orders (pet, task) pairs by the zero-padded `"HH:MM"` string with `sorted()` and a lambda key. `get_todays_schedule()` applies it to tasks due today. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filters by pet name (case-insensitive), completion status, or both. Passing `None` skips that filter. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups pending tasks by `(due_date, time)` and returns one warning string per slot with more than one task, across the same or different pets. It never raises. |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.mark_task_complete()` | Completing a `daily` or `weekly` task creates a copy due `timedelta(days=1)` or `timedelta(weeks=1)` later and adds it to the pet. `once` tasks do not recur. |

**Tradeoff:** conflicts are exact time matches only. A 30-minute walk at 08:00 and a feeding at 08:15 are not flagged, because tasks have a start time and duration but the check ignores duration.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
