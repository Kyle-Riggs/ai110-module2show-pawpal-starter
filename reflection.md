# PawPal+ Project Reflection

## 1. System Design

**Three core user actions**

1. Add a pet to the owner's profile (name and species).
2. Schedule a care task (walk, feeding, medication, appointment) for a specific pet at a specific time, with a frequency such as once, daily, or weekly.
3. See today's schedule: every task across all pets in time order, with conflicts and completion status visible.

**a. Initial design**

The initial UML has four classes:

- `Task` (dataclass): one care activity. It holds a description, an "HH:MM" time, a frequency, a duration, a priority, and a completion flag. It knows how to mark itself complete.
- `Pet` (dataclass): a pet's name and species plus the list of tasks that belong to it. It adds and removes its own tasks.
- `Owner` (dataclass): holds the owner's name and their pets. It adds pets and gathers tasks across all of them.
- `Scheduler`: the "brain". It takes an `Owner` and reads tasks through it. It builds today's schedule, sorts by time, filters by pet or status, and detects conflicts. It stores no tasks of its own, so there is a single source of truth.

Relationships: an Owner has many Pets, a Pet has many Tasks, and the Scheduler depends on one Owner.

**b. Design changes**

I reviewed the first skeleton and made two changes before implementing anything:

1. `Owner.get_all_tasks()` now returns `(Pet, Task)` pairs instead of bare tasks. A `Task` doesn't know which pet it belongs to, so the Scheduler couldn't filter by pet name or write a useful conflict warning ("Mochi and Biscuit both at 08:00") from a flat task list. Pairs avoid a back-reference from `Task` to `Pet`, which would make the objects circular. `sort_by_time`, `filter_tasks`, and `get_todays_schedule` use the same pair type.
2. `Task` gained a `due_date` field. Recurring tasks need a date to advance ("today + 1 day" for daily), and "today's schedule" needs a date to filter on. Without it the recurrence logic in Phase 4 would have nothing to work from.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three things: **time** (tasks are ordered by due date, then start time), **date** (today's schedule only shows tasks due today, and recurring tasks move forward by a day or a week), and **pet** (filters and conflict messages are per pet). Tasks also carry a priority and duration, but the scheduler displays them rather than using them to decide anything.

I treated time as the constraint that matters most because the core job is "what do I do next?", and everything else (conflicts, recurrence) follows from when a task is due. Using priority to drop or reorder tasks would only matter if the owner had less time than the tasks need, which the current scenario doesn't model.

**b. Tradeoffs**

The scheduler's conflict detection only flags tasks with the exact same date and start time. It ignores duration, so a 30-minute walk at 08:00 and a feeding at 08:15 are not reported even though they overlap.

I chose this because it is simple to explain and test: group pending tasks by `(due_date, time)` and warn on any group larger than one. Overlap detection would need start/end times, handling for tasks that cross midnight, and a decision about whether back-to-back tasks count as conflicts. For a household with one owner, exact collisions are the most obvious scheduling mistake. A missed near-overlap is a minor annoyance that the owner can see in the sorted schedule.

I also reviewed `detect_conflicts` for readability. A nested-loop version comparing every pair of tasks is shorter to write but is O(n²) and reports each three-way clash as three separate warnings. Grouping with `defaultdict` is a little longer but runs in one pass and yields one clear warning per time slot, so I kept it.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant for the whole build, working one phase at a time: drafting the UML and class skeleton, implementing the classes and the CLI demo, wiring the Streamlit UI, adding the sorting/filtering/recurrence/conflict logic, writing the test suite, and drafting the README and diagram. After each phase I stopped to review the changes and commit them myself.

The most useful prompts were specific and tied to files that already existed, for example asking how the Scheduler should retrieve tasks from the Owner's pets, or asking for a review of the skeleton for missing relationships. That second kind of prompt, a review of existing code, found the biggest design flaw of the project early (see 1b). Running the code after each change, in `main.py`, pytest, and a headless Streamlit run, was what made the output trustworthy.

I did this in one continuous assistant session with a hard stop and a commit after every phase, rather than separate chat sessions per phase. The commit boundaries did the same organizing job: each phase had a clear scope and a clean diff to review.

**b. Judgment and verification**

The first skeleton had `Owner.get_all_tasks()` return a flat list of tasks. That looks natural, but when I reviewed it against what the Scheduler needed (filter by pet, name the pet in a conflict warning) it was missing information, so I changed the return type to `(Pet, Task)` pairs before any logic depended on it. I rejected the other obvious fix, giving `Task` a reference back to its `Pet`, because it creates a circular relationship between the two classes.

A later example happened in the UI. The first version of the "Mark complete" button changed the data after the schedule table had already been drawn, so the table showed stale information until the next click. The headless Streamlit test I ran caught nothing because the state was correct, so I only noticed it by tracing the order the script runs in. The fix was to store a message and call `st.rerun()`. While wiring the UI I also changed `sort_by_time` to sort by `(due_date, time)`, since recurring tasks put tomorrow's 07:30 into the same list as today's 08:00.

To verify suggestions I ran them: the demo script for behavior, 22 pytest tests for logic, and a scripted Streamlit session (add pet, create a conflict, complete a recurring task, filter) for the UI.

---

## 4. Testing and Verification

**a. What you tested**

The 22 tests cover sorting (chronological order, zero-padded times, date before time, today-only schedules), recurrence (daily, weekly, one-time tasks, month rollover), conflict detection (same pet, different pets, three-way clash, different times and dates, completed tasks), filtering (pet, status, both, unknown pet), and empty cases (no tasks, a pet with no tasks).

These matter because the scheduler's value is that its answers are right without the owner double-checking them. Recurrence and conflict detection are the places where an off-by-one or a wrong grouping would silently produce a bad schedule.

**b. Confidence**

I'm fairly confident (4 out of 5) in the core logic: every behavior listed above passed, and I exercised the same paths through the CLI demo and the UI.

Next I would test: malformed times like `"8:00"` or `"25:99"` (currently accepted, and `"8:00"` would sort after `"18:00"`), overlapping durations rather than exact matches, a recurring task completed twice, and removing a task from a pet that doesn't have it.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with keeping the logic layer independent of the UI. `pawpal_system.py` has no Streamlit code, so the same classes drive the CLI demo, the tests, and the app, and I could verify the algorithms before building any interface.

**b. What you would improve**

I would validate times when a task is created (a real `datetime.time` instead of a string), detect overlapping durations instead of only exact matches, and use priority to decide what happens when tasks collide instead of only displaying it. I would also make the `(Pet, Task)` pair a small named type, since it appears in every Scheduler method signature.

**c. Key takeaway**

The AI is quick at producing a plausible first version, and the lead architect's job is to decide whether that version is right. The biggest improvements in this project (returning pets with tasks, adding a due date, refreshing the UI after an action) came from reviewing the output against what the next phase would need, not from generating more code. Small phases, a commit after each, and running everything before moving on kept those reviews cheap.
