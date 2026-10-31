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
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
