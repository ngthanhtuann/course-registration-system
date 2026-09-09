Update my existing Course Registration System prototype.

IMPORTANT:
- Do NOT redesign the entire application.
- Keep the current visual style, colors, typography, sidebar, navigation, spacing, buttons, cards, tables, and page structure.
- Keep all existing pages and existing functions.
- Only modify the necessary screens to support Course Capacity.
- Use the term "Lecturer", NOT "Instructor".
- The system registers students by Course, NOT Course Section.

========================================
1. ADMIN - MANAGE COURSE
========================================

Update the existing "Manage Course" page.

Course table must contain these columns:

- Course Code
- Course Name
- Credits
- Capacity
- Available Seats
- Prerequisite
- Actions

Example:

Course Code: PRG101
Course Name: Programming Fundamentals
Credits: 3
Capacity: 30
Available Seats: 12
Prerequisite: None

----------------------------------------
CREATE COURSE
----------------------------------------

Update the existing "Create Course" form.

The form must contain:

Course Code *
Course Name *
Credits *
Capacity *
Prerequisite

Capacity requirements:

- Capacity is required.
- Capacity must be a positive integer.
- Example value: 30.
- Show an error message if Capacity <= 0.

Buttons:

Cancel
Create Course

Do not remove any existing fields.

----------------------------------------
EDIT COURSE
----------------------------------------

Update the existing "Edit Course" form.

Fields:

Course Code
Course Name
Credits
Capacity
Prerequisite

Admin must be able to modify Capacity.

Show the current Capacity value when opening the Edit form.

Buttons:

Cancel
Save Changes

----------------------------------------
VIEW COURSE
----------------------------------------

Update the existing Course Details modal/page.

Display:

Course Code
Course Name
Credits
Prerequisite
Capacity
Available Seats

Example:

Capacity: 30
Available Seats: 12

========================================
2. STUDENT - VIEW COURSES
========================================

Update the existing Student "View Courses" page.

Course table/cards must display:

Course Code
Course Name
Credits
Prerequisite
Recommended Semester
Capacity
Available Seats
Status

Example:

Capacity: 30
Available Seats: 12
Status: Available

If:

Available Seats = 0

display:

Status: Full

Use a clear visual badge for:

Available
Full

========================================
3. STUDENT - COURSE REGISTRATION
========================================

Update the existing "Course Registration" page.

Each course must show:

Course Code
Course Name
Credits
Prerequisite
Capacity
Available Seats
Registration Status

Add/Register button behavior:

If Available Seats > 0:
Show an enabled "Register" button.

If Available Seats = 0:
Show "Full".
Disable the Register button.

Before registration, show a confirmation dialog:

"Are you sure you want to register for this course?"

After successful registration:

Show:
"Course registered successfully."

Update Available Seats on the interface.

Example:

Before:
Capacity: 30
Available Seats: 12

After successful registration:
Capacity: 30
Available Seats: 11

========================================
4. STUDENT - DROP COURSE
========================================

Keep the existing Drop Course page.

When the student selects a registered course:

Show a confirmation dialog:

"Are you sure you want to drop this course?"

After successful drop:

Show:
"Course dropped successfully."

Available Seats must increase by 1 after a successful drop.

Example:

Before:
Capacity: 30
Available Seats: 11

After drop:
Capacity: 30
Available Seats: 12

========================================
5. CAPACITY UI RULES
========================================

Capacity represents the maximum number of students that can register for a Course.

Available Seats represents:

Available Seats =
Capacity - Number of Active Registered Students

Do NOT create an input field that allows Admin to manually edit Available Seats.

Admin only manages Capacity.

Available Seats is calculated automatically by the system.

When Available Seats = 0:
- Display "Full"
- Student cannot register.

When Available Seats > 0:
- Display "Available"
- Student may register if all other registration conditions are satisfied.

========================================
6. DESIGN CONSISTENCY
========================================

VERY IMPORTANT:

Keep the existing Figma design style.

Do NOT:
- redesign the sidebar
- change the color theme
- change typography
- remove existing pages
- rename existing functions
- introduce Course Sections
- introduce classrooms or schedules
- replace Lecturer with Instructor
- add unrelated features

Only update the necessary UI components to support Capacity and Available Seats.

The updated prototype should visually match the current Course Registration System implementation.