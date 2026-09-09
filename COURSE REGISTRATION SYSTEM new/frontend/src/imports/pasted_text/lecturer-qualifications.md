Modify the existing Course Registration System frontend only. 
DO NOT redesign the existing application, do not change the overall layout, color palette, typography, sidebar, topbar, navigation, existing pages, or existing components.

I only want to add and complete the Teaching Qualification functionality for Lecturer accounts.

IMPORTANT:
Teaching Qualification means the COURSES that a Lecturer is qualified/allowed to teach.
It does NOT mean academic degrees such as Bachelor, Master, or PhD.

Keep the current Admin > Manage User interface and visual style exactly as it is.

==================================================
1. MANAGE USER – LECTURER TABLE
==================================================

In the existing Admin > Manage User page:

Keep the current table structure and actions.

For Lecturer rows, make sure the Qualification column displays the lecturer's qualified courses.

Example:

Qualification
CS101 - Introduction to Programming
CS201 - Data Structures
CS301 - Database Systems

If there are many courses, display them as compact tags/chips and show "+2 more" when necessary.

Do NOT display fake academic qualifications such as "PhD" or "Master".

For Student rows, keep the existing Major behavior unchanged.

==================================================
2. CREATE LECTURER
==================================================

Modify the existing "Create User" modal/drawer.

When User Type = Lecturer:

Keep all existing Lecturer fields:
- Lecturer ID
- Full Name
- Email
- Password

Add a new section:

Teaching Qualifications

Use a searchable multi-select Course selector.

Example:

Teaching Qualifications
[ Select courses ▼ ]

Selected courses appear as removable chips:

[ CS101 - Introduction to Programming × ]
[ CS201 - Data Structures × ]

The dropdown should show available courses with:
- Course Code
- Course Name

Example:

□ CS101 — Introduction to Programming
□ CS201 — Data Structures
□ CS301 — Database Systems
□ CS401 — Artificial Intelligence

Allow the Admin to select multiple courses.

The Admin must be able to remove a selected course using the × icon.

Do not use a free-text input for qualification.

The qualification must always reference an existing Course.

Add helper text:

"Select the courses this lecturer is qualified to teach."

==================================================
3. LECTURER DETAIL / VIEW
==================================================

When the Admin clicks View for a Lecturer, keep the existing Lecturer detail layout.

Add a clearly separated section:

Teaching Qualifications

Display all qualified courses as cards or compact rows.

Example:

Teaching Qualifications

CS101
Introduction to Programming
[Remove]

CS201
Data Structures
[Remove]

CS301
Database Systems
[Remove]

Add button:

[ + Add Qualification ]

The Add Qualification action should open a small modal.

==================================================
4. ADD QUALIFICATION MODAL
==================================================

Create a modal titled:

Add Teaching Qualification

Fields:

Lecturer
[ Lecturer ID / Lecturer Name ] (read-only)

Course
[ Select Course ▼ ]

The Course dropdown must contain existing courses only.

Buttons:

[ Cancel ] [ Add Qualification ]

Validation:
- Course is required.
- Do not allow the Admin to select a course that is already a qualification for this lecturer.
- Show an inline validation message for duplicate qualification.
- Show a clear success message after adding a qualification.

Example success message:

"Teaching qualification added successfully."

==================================================
5. EDIT LECTURER
==================================================

When Admin selects Edit for a Lecturer, include the Teaching Qualifications section in the existing Edit Lecturer form.

Allow Admin to:
- View current qualified courses
- Add qualified courses
- Remove qualified courses

Use the same searchable multi-select pattern as Create Lecturer.

Do not change the existing Student Edit form.

==================================================
6. REMOVE QUALIFICATION
==================================================

When Admin clicks Remove on a qualification:

Show a confirmation dialog:

"Remove this teaching qualification?"

Message:

"The lecturer will no longer be eligible to be assigned to this course."

Buttons:

[ Cancel ] [ Remove ]

If Cancel is selected:
- Keep the qualification unchanged.

If Remove is selected:
- Remove the course from the lecturer's qualification list.
- Show a success message.

==================================================
7. EMPTY STATE
==================================================

If a Lecturer has no teaching qualifications, display:

Teaching Qualifications

No teaching qualifications have been assigned.

[ + Add Qualification ]

Do not display placeholder/fake courses.

==================================================
8. RESPONSIVE DESIGN
==================================================

Preserve the existing responsive behavior.

Desktop:
- Keep the current sidebar and main content layout.
- Modal/drawer should have enough width for the course selector.

Tablet:
- Keep existing responsive behavior.

Mobile:
- Qualification chips should wrap naturally.
- Course selector should be full width.
- Modal/drawer should fit the mobile screen.
- Buttons should remain easy to tap.

Do not redesign the mobile interface.

==================================================
9. DATA / BACKEND INTENT
==================================================

Design the UI so it can later connect to the existing backend.

The qualification data concept is:

Lecturer
    ↓
Teaching Qualifications
    ↓
Existing Courses

Each qualification represents:

lecturer_id + course_code

The existing backend endpoint is conceptually:

POST /api/admin/lecturer-qualifications

with:
- qualification_id
- lecturer_id
- course_code

Do not create a new qualification text field.

Do not create a new academic-degree field.

Do not invent a separate qualification entity in the UI.

==================================================
10. IMPORTANT DESIGN RULES
==================================================

DO NOT:
- redesign the dashboard
- redesign the sidebar
- redesign the Manage User page
- change Student functionality
- change Course Management
- create fake qualification data
- use free-text qualification input
- introduce academic degree fields
- create an unrelated Qualification page
- change existing colors or typography
- change existing navigation

ONLY add the Teaching Qualification functionality described above.

The final result should look like a natural extension of the existing Course Registration System UI, not a newly redesigned application.

Keep all existing components and styling consistent with the current frontend.