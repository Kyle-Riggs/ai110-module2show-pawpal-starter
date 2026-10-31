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

## Features

- **Pets and tasks:** add pets, then schedule tasks for each with a time, duration, priority, and frequency (once, daily, weekly).
- **Sorted daily schedule:** today's tasks across all pets, ordered by time (`Scheduler.sort_by_time`).
- **Filtering:** browse tasks by pet, by status (pending or completed), or both (`Scheduler.filter_tasks`).
- **Conflict warnings:** tasks sharing the same date and start time are flagged, within one pet or across pets (`Scheduler.detect_conflicts`).
- **Daily and weekly recurrence:** completing a recurring task automatically schedules the next occurrence (`Scheduler.mark_task_complete`).
- **Persistent session:** your owner, pets, and tasks stay in memory while you use the app (`st.session_state`).

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

The suite in `tests/test_pawpal.py` has 22 tests covering:

- **Basics:** `Task.mark_complete()` changes status; `Pet.add_task()` increases the task count.
- **Sorting:** tasks come back in chronological order across pets, zero-padded times sort correctly (`09:05` before `10:00`), due date outranks time, and today's schedule excludes tasks due on other dates.
- **Recurrence:** completing a daily task creates one due the next day, a weekly task one week later, a `once` task creates nothing, and a daily task on Jan 31 rolls over to Feb 1.
- **Conflict detection:** same time on different pets or the same pet is flagged, a three-way clash gives one warning, and different times, different dates, and already-completed tasks are not flagged.
- **Filtering:** by pet name (case-insensitive), by completion status, by both, and for an unknown pet.
- **Empty cases:** an owner with no tasks and a pet with no tasks.

Sample test output:

```
============================= test session starts =============================
collecting ... collected 22 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  4%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [  9%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 13%]
tests/test_pawpal.py::test_sort_handles_zero_padded_times_around_ten PASSED [ 18%]
tests/test_pawpal.py::test_todays_schedule_is_sorted_and_excludes_other_dates PASSED [ 22%]
tests/test_pawpal.py::test_schedule_for_owner_with_no_tasks_is_empty PASSED [ 27%]
tests/test_pawpal.py::test_pet_with_no_tasks_does_not_break_other_pets PASSED [ 31%]
tests/test_pawpal.py::test_completing_daily_task_creates_task_for_next_day PASSED [ 36%]
tests/test_pawpal.py::test_completing_weekly_task_creates_task_a_week_later PASSED [ 40%]
tests/test_pawpal.py::test_completing_one_time_task_creates_no_new_task PASSED [ 45%]
tests/test_pawpal.py::test_daily_recurrence_rolls_over_month_end PASSED  [ 50%]
tests/test_pawpal.py::test_conflict_detected_for_same_time_across_pets PASSED [ 54%]
tests/test_pawpal.py::test_conflict_detected_for_same_time_on_same_pet PASSED [ 59%]
tests/test_pawpal.py::test_three_way_clash_produces_single_warning PASSED [ 63%]
tests/test_pawpal.py::test_no_conflict_for_different_times PASSED        [ 68%]
tests/test_pawpal.py::test_no_conflict_for_same_time_on_different_dates PASSED [ 72%]
tests/test_pawpal.py::test_completed_task_is_not_a_conflict PASSED       [ 77%]
tests/test_pawpal.py::test_filter_by_pet_name_is_case_insensitive PASSED [ 81%]
tests/test_pawpal.py::test_filter_by_completion_status PASSED            [ 86%]
tests/test_pawpal.py::test_filter_combines_pet_and_status PASSED         [ 90%]
tests/test_pawpal.py::test_filter_unknown_pet_returns_empty PASSED       [ 95%]
tests/test_pawpal.py::test_sort_orders_by_date_before_time PASSED        [100%]

============================= 22 passed in 0.03s ==============================
```

**Confidence Level: ★★★★☆ (4/5).** The core scheduling logic is covered on both happy paths and edge cases, and all 22 tests pass. I stopped short of five stars because conflict detection only matches exact start times (overlapping durations are not caught), times are not validated (`"8:00"` or `"25:99"` would be accepted), and the Streamlit UI is not covered by automated tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting | `Scheduler.sort_by_time()` | Orders (pet, task) pairs by `(due_date, time)` with `sorted()` and a lambda key; zero-padded `"HH:MM"` strings sort correctly as text. `get_todays_schedule()` applies it to tasks due today. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filters by pet name (case-insensitive), completion status, or both. Passing `None` skips that filter. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups pending tasks by `(due_date, time)` and returns one warning string per slot with more than one task, across the same or different pets. It never raises. |
| Recurring tasks | `Task.mark_complete()`, `Scheduler.mark_task_complete()` | Completing a `daily` or `weekly` task creates a copy due `timedelta(days=1)` or `timedelta(weeks=1)` later and adds it to the pet. `once` tasks do not recur. |

**Tradeoff:** conflicts are exact time matches only. A 30-minute walk at 08:00 and a feeding at 08:15 are not flagged, because tasks have a start time and duration but the check ignores duration.

## 📸 Demo Walkthrough

Start the app with `python -m streamlit run app.py`.

**What you can do in the UI**

- Set the owner name, add pets (name and species), and schedule tasks for any pet.
- See today's schedule as a table sorted by time, with a conflict warning above it when needed.
- Mark pending tasks complete; recurring tasks schedule their own next occurrence.
- Browse every task and filter by pet and status.

**Example workflow**

1. **Add a pet.** Enter "Mochi" with species "dog" under *Add a Pet* and submit. Mochi appears in the pets table with 0 tasks.
2. **Schedule a task.** Under *Schedule a Task* choose Mochi, enter "Morning walk" at 08:00, 30 minutes, high priority, frequency *daily*. It appears in *Today's Schedule*.
3. **Create a conflict.** Add a second task, "Grooming", for Mochi at 08:00 (or give another pet a task at 08:00). A warning appears above the schedule naming the time and both tasks, so you know to move one.
4. **Complete a recurring task.** Under *Complete a Task* pick "Morning walk" and click *Mark complete*. The app confirms the next daily occurrence is scheduled for tomorrow, and the conflict warning clears because the walk is done.
5. **Filter.** Under *Browse All Tasks* set Status to *Completed* to see the finished walk, or Pet and Status to *Pending* to see what remains for Mochi.

**Key Scheduler behaviors shown**

- **Sorting:** schedule and browse tables are ordered by date, then time, no matter what order tasks were added.
- **Conflict warnings:** one warning per clashing time slot, listing every task involved.
- **Recurrence:** completing a `daily` or `weekly` task adds the next occurrence; `once` tasks do not repeat.
- **Filtering:** by pet name, completion status, or both.

**Sample CLI output** from `python main.py`, which adds tasks out of order, includes a deliberate 08:00 clash, and completes a daily task:

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

**Screenshot or video** *(optional)*: not included.
