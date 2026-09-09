I want you to modify the existing frontend source code of this
Course Registration System.

IMPORTANT:
This is NOT a UI redesign task.

==================================================
1. PRESERVE THE EXISTING UI
==================================================

Keep the existing Figma design EXACTLY as it is.

Do NOT redesign the interface.

Do NOT change:
- page layout
- sidebar
- navbar
- buttons
- colors
- typography
- spacing
- cards
- tables
- forms
- modals
- icons
- navigation
- responsive layout
- existing components
- existing visual hierarchy

Keep the current UI and user experience.

Only modify the APPLICATION LOGIC and DATA FLOW behind the existing UI.

The final application should look the same as the current Figma design.

==================================================
2. MAIN OBJECTIVE
==================================================

Convert the current frontend prototype/mock-data application into a
real frontend connected to my existing Flask backend and PostgreSQL database.

Current architecture:

Frontend:
React + TypeScript + Vite

Backend:
Python Flask

Database:
PostgreSQL

Backend URL:

http://127.0.0.1:5000

Do NOT create a new backend.

Do NOT replace Flask.

Do NOT change the PostgreSQL database schema.

Use the existing backend API.

==================================================
3. REMOVE MOCK DATA
==================================================

The current frontend contains prototype/static/mock data in files such as:

src/data.ts

and other pages/components.

Remove the dependency on mock data for real application functions.

Do NOT use fake users, fake courses, fake students, fake lecturers,
fake semesters, fake registrations, etc.

The application must display real data returned by the Flask API.

Empty database tables should produce empty UI states.

Do NOT automatically insert demonstration data.

==================================================
4. AUTHENTICATION
==================================================

Connect the login page to:

POST /api/login

Request:

{
  "username": "...",
  "password": "..."
}

The backend returns:

{
  "token": "...",
  "user": {
    "user_id": "...",
    "username": "...",
    "fullname": "...",
    "email": "...",
    "role": "admin|lecturer|student"
  }
}

After successful login:

- store the JWT token
- store the logged-in user information
- use the token for protected API requests
- redirect the user according to their role

For protected requests use:

Authorization: Bearer <token>

Do NOT create another authentication system.

Use the existing Flask JWT authentication.

==================================================
5. API REQUEST STYLE
==================================================

Keep the code simple.

Use:

- fetch()
- useState()
- useEffect()

Do NOT introduce:

- Redux
- Axios
- React Query
- Zustand
- complex state management
- unnecessary libraries
- complicated architecture

The code should be easy for a university student to understand.

Create a simple API helper only if it makes the code cleaner.

For example:

const API_URL = "http://127.0.0.1:5000";

Use fetch() for API requests.

==================================================
6. ADMIN - USER MANAGEMENT
==================================================

Connect the existing Admin Manage User interface to:

GET /api/admin/users

POST /api/admin/users

PUT /api/admin/users/:user_id

The existing UI must remain unchanged.

Admin can create:

- Student
- Lecturer

Admin must NOT create another Admin account from the normal user
management form.

--------------------------------------------------
Create Lecturer
--------------------------------------------------

Use the existing Create Lecturer form.

Send:

POST /api/admin/users

Request:

{
  "user_id": "...",
  "fullname": "...",
  "email": "...",
  "password": "...",
  "role": "lecturer"
}

The backend automatically creates the lecturer record.

--------------------------------------------------
Create Student
--------------------------------------------------

Use the existing Create Student form.

Send:

POST /api/admin/users

Request:

{
  "user_id": "...",
  "fullname": "...",
  "email": "...",
  "password": "...",
  "role": "student",
  "major_code": "...",
  "dob": "YYYY-MM-DD"
}

The backend automatically creates the student record.

After successful creation:

- close the modal/form
- reload the user list
- display the newly created user immediately

Do NOT add the user only to React state.

The database is the source of truth.

==================================================
7. ADMIN - MAJOR MANAGEMENT
==================================================

Connect the existing Major Management interface to:

GET /api/admin/majors

POST /api/admin/majors

PUT /api/admin/majors/:major_code

DELETE /api/admin/majors/:major_code

Keep the existing UI.

After create/update/delete:

reload the data from the backend.

Do NOT only modify local React state.

==================================================
8. ADMIN - COURSE MANAGEMENT
==================================================

Connect the existing Manage Course interface to:

GET /api/admin/courses

POST /api/admin/courses

PUT /api/admin/courses/:course_code

DELETE /api/admin/courses/:course_code

Keep the existing Create Course, Edit Course and Delete Course UI.

Request for Create Course:

{
  "course_code": "...",
  "course_name": "...",
  "credit": 3,
  "prerequisite_course_code": null,
  "max_capacity": 40
}

Backend field mapping:

course_code -> code
course_name -> name
credit -> credits
prerequisite_course_code -> prerequisite
max_capacity -> capacity

When the page opens:

GET /api/admin/courses

and display the real courses.

When Create Course succeeds:

1. close the form/modal
2. GET /api/admin/courses again
3. update the table
4. display the newly created course

When Edit Course succeeds:

1. update backend
2. reload courses
3. update table

When Delete Course succeeds:

1. delete from backend
2. reload courses
3. update table

Do NOT use local mock course data.

==================================================
9. ADMIN - CURRICULUM
==================================================

Connect the existing Curriculum interface to:

GET /api/admin/curriculum/:major_code

POST /api/admin/curriculum

PUT /api/admin/curriculum/:curriculum_id

DELETE /api/admin/curriculum/:curriculum_id

Use real courses and real majors from the backend.

Keep the existing UI.

==================================================
10. ADMIN - SEMESTER
==================================================

Connect the existing Semester Management interface to:

GET /api/admin/semesters

POST /api/admin/semesters

PUT /api/admin/semesters/:semester_id

DELETE /api/admin/semesters/:semester_id

Keep the existing UI.

After every successful CRUD operation,
reload the semester list from the backend.

==================================================
11. ADMIN - REGISTRATION PERIOD
==================================================

Connect the existing Registration Period interface to:

GET /api/admin/registration-periods

POST /api/admin/registration-periods

PUT /api/admin/registration-periods/:period_id

DELETE /api/admin/registration-periods/:period_id

Use real semester data.

Keep the existing UI.

==================================================
12. ADMIN - REGISTRATION DEMAND
==================================================

Connect the existing Registration Demand interface to:

GET /api/admin/registration-demand

Parameters:

period_id
major_code

For students registered in a course:

GET /api/admin/registration-demand/:course_code/students

Parameter:

period_id

Display real registration demand data.

Do NOT use fake registration numbers.

==================================================
13. ADMIN - TEACHING ASSIGNMENT
==================================================

Connect the existing Teaching Assignment interface to:

GET /api/admin/teaching-assignments

POST /api/admin/teaching-assignments

DELETE /api/admin/teaching-assignments/:assignment_id

For qualified lecturers:

GET /api/admin/qualified-lecturers/:course_code

Use real lecturers and real courses.

Keep the current UI.

==================================================
14. LECTURER
==================================================

Connect Lecturer pages to the existing Flask backend.

Lecturer information must come from the authenticated user/database.

Do NOT use fake lecturer data.

Keep the existing Lecturer dashboard and UI.

Use the JWT token for protected requests.

If an endpoint is required by the existing Lecturer UI but does not exist
in the current backend, do NOT invent fake data.

Instead, structure the frontend so the page can use the backend endpoint
when available.

==================================================
15. STUDENT
==================================================

Connect Student pages to the real backend/database.

Student information must come from the authenticated user/database.

Course information must come from the backend.

Registration information must come from the backend.

Do NOT use:

- fake courses
- fake registrations
- fake grades
- fake student information

Keep the existing Student UI.

Use JWT authentication for protected requests.

==================================================
16. DATABASE IS THE SOURCE OF TRUTH
==================================================

Very important:

React state is NOT the database.

After any:

CREATE
UPDATE
DELETE
REGISTER
DROP

operation:

1. send request to Flask
2. wait for successful response
3. fetch the latest data from Flask
4. update the UI

Do NOT make the UI appear successful if the database request failed.

==================================================
17. ERROR HANDLING
==================================================

Use simple error handling.

If Flask returns:

400
401
403
404
409
500

display a suitable error message in the existing UI.

Do not create a completely new error design.

Use the existing notification/toast/modal system if one already exists.

Examples:

"Invalid username or password"

"Email already exists"

"Course code already exists"

"Major is still referenced by existing data"

"Lecturer is not qualified for this course"

==================================================
18. EMPTY STATES
==================================================

Because mock data is being removed, many database tables may initially
be empty.

Do NOT insert sample data automatically.

Use the existing empty-state UI when there is no data.

For example:

No courses found.

No students found.

No lecturers found.

No registration data found.

Keep the existing design.

==================================================
19. DATA FIELD MAPPING
==================================================

The backend uses database-style field names.

The frontend currently uses some different names.

Handle the mapping in the frontend.

For example:

Backend:

user_id
username
fullname
email
role

Course:

course_code
course_name
credit
prerequisite_course_code
max_capacity

Student:

student_id
user_id
dob
major_code

Lecturer:

lecturer_id
user_id

Major:

major_code
major_name

Semester:

semester_id
semester_name
start_date
end_date
status

Registration Period:

period_id
semester_id
period_name
start_date
end_date

Do NOT change the database schema just to match the frontend.

==================================================
20. DO NOT CHANGE BACKEND
==================================================

The Flask backend already exists.

Do NOT rewrite the backend.

Do NOT create a second backend.

Do NOT create fake API endpoints.

Use the existing endpoints.

If a frontend feature has no corresponding backend endpoint,
do not simulate it with mock data.

Clearly keep that functionality ready for the backend endpoint.

==================================================
21. DO NOT CHANGE THE FILE STRUCTURE UNNECESSARILY
==================================================

Keep the current project structure.

Modify existing files where possible.

Do not create hundreds of new files.

Do not replace the whole application with a new architecture.

Keep the current components and pages.

==================================================
22. IMPORTANT FIGMA MAKE REQUIREMENT
==================================================

Preserve the existing Figma Make configuration.

Do not remove:

.figma/make/

Do not remove:

.figma/make/site.json

Do not break:

vite.config.ts

The project must continue to run with:

npm install

npm run dev

==================================================
23. FINAL QUALITY REQUIREMENTS
==================================================

Before finishing:

Check every Admin page.

Check Login.

Check Student pages.

Check Lecturer pages.

Check all API calls.

Check that JWT is included in protected requests.

Check loading states.

Check empty states.

Check error states.

Check create/update/delete operations.

Check that data is reloaded from the backend after successful operations.

Most importantly:

The UI must look the SAME as the current Figma design.

Only the data source and application logic should change.

==================================================
24. FINAL GOAL
==================================================

The final application should behave like a real Course Registration System:

Figma UI
   ↓
React
   ↓
fetch()
   ↓
Flask API
   ↓
PostgreSQL
   ↓
Flask API
   ↓
React UI

NOT:

Figma UI
   ↓
mock data
   ↓
React state only

Keep the interface exactly as designed,
but replace prototype/mock behavior with real backend functionality.