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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

The scheduler's conflict detection only flags tasks with the exact same date and start time. It ignores duration, so a 30-minute walk at 08:00 and a feeding at 08:15 are not reported even though they overlap.

I chose this because it is simple to explain and test: group pending tasks by `(due_date, time)` and warn on any group larger than one. Overlap detection would need start/end times, handling for tasks that cross midnight, and a decision about whether back-to-back tasks count as conflicts. For a household with one owner, exact collisions are the most obvious scheduling mistake. A missed near-overlap is a minor annoyance that the owner can see in the sorted schedule.

I also reviewed `detect_conflicts` for readability. A nested-loop version comparing every pair of tasks is shorter to write but is O(n²) and reports each three-way clash as three separate warnings. Grouping with `defaultdict` is a little longer but runs in one pass and yields one clear warning per time slot, so I kept it.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
