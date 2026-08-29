# COURSE REGISTRATION SYSTEM SPECIFICATION

## I. Functional Requirements

## FR01 — Login (User Authentication)
* The system shall allow Admin, Lecturer, and Student to log in using a valid username and password.
* The system shall verify the username, password, and account status.
* If the credentials are valid, the system shall grant access according to the user's role; otherwise, it shall display an appropriate error message.
* After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.

## FR02 — Manage Account
* The system shall allow Admin, Lecturer, and Student to view their account information, change their password, and log out.
* The system shall validate the current password before saving a new password.

## FR03 — Manage User (Admin)
* The system shall allow the Admin to view, search, create, edit, and deactivate Student and Lecturer accounts.
* Student ID and Lecturer ID shall be unique, and email addresses shall be valid.
* The Admin shall be able to set Lecturer teaching qualifications.
* The system shall ensure that only one Admin account exists.

## FR04 — Manage Major (Admin)
* The system shall allow the Admin to view, create, edit, and delete Majors.
* Major Code shall be unique.
* The system shall prevent deletion of a Major that is still referenced by existing data.

## FR05 — Manage Curriculum (Admin)
* The system shall allow the Admin to select a Major and view the Courses in its Curriculum.
* The Admin shall be able to add or remove Courses and set the Recommended Semester.
* The system shall prevent the same Course from being added to the same Curriculum more than once.

## FR06 — Manage Course (Admin)
* The system shall allow the Admin to view, search, create, edit, and delete Courses.
* Course information shall include Course Code, Course Name, Credit, Prerequisite, and Capacity.
* The system shall validate that Course Code is unique, Credit is valid, Capacity is a positive number, and a Course cannot be its own Prerequisite.

## FR07 — Manage Semester (Admin)
* The system shall allow the Admin to create, view, edit, and delete Semesters.
* Semester information shall include Semester Name, Start Date, End Date, and Status.
* The system shall validate that Start Date is earlier than End Date and that Semesters do not overlap.

## FR08 — Manage Registration Period (Admin)
* The system shall allow the Admin to select a Semester and configure a Registration Period with a name, Start Date, and End Date.
* The system shall validate the dates and automatically update the Registration Status as Upcoming, Open, or Closed.
* The system shall allow the Admin to configure a Drop Period, with a Start Date and End Date, for dropping registered Courses.

## FR09 — Manage Registration Demand (Admin)
* The system shall allow the Admin to select a Registration Period and Major to view registration demand by Course.
* The system shall display Course Code, Course Name, Number of Registered Students, and the registered Student list.
* The system shall allow the Admin to generate a Registration Demand Report.

## FR10 — Assign Lecturer (Admin)
* The system shall allow the Admin to select a Major and Course and view Lecturers qualified to teach that Course.
* The Admin shall be able to assign a qualified Lecturer to the Course.
* The system shall reject assignments when the Lecturer is not qualified.

## FR11 — Manage Teaching Course (Lecturer)
* The system shall allow the Lecturer to select a Semester and view Courses assigned by the Admin.
* The Lecturer shall not be allowed to self-select, request, or modify Course assignments.
* The Lecturer's teaching Course list shall be updated when the Admin changes an assignment.

## FR12 — Manage Student Grades (Lecturer)
* The system shall allow the Lecturer to view Students registered in Courses assigned to them.
* The system shall allow the Lecturer to view a Student's Prerequisite status for the Course, without allowing the Lecturer to modify it.
* The Lecturer shall be able to enter or update a Student's Grade.
* The system shall validate the Grade and ensure that the Student is registered in the selected Course and the Course is assigned to that Lecturer.

## FR13 — View Courses (Student)
* The system shall allow the Student to view and search Courses belonging to their Major.
* The system shall exclude Courses the Student has already completed or is currently registered in from the displayed list.
* The system shall display Course Code, Course Name, Credit, Prerequisite, Recommended Semester, Capacity, and Available Seats.

## FR14 — Course Registration (Student)
* The system shall allow the Student to select a Course to register.
* The system shall validate that the Registration Period is Open, the Course belongs to the Student's Major/Curriculum, the Prerequisite is satisfied, the Student has not already completed the Course, and the * * Student is not already registered for the Course.
* The system shall check Course Capacity before registration. Registration shall be rejected when no seat is available.
* If all validations pass, the system shall save the registration, decrease Available Seats by one, and display a success message.

## FR15 — View Registration Status (Student)
* The system shall allow the Student to select a Semester and view registered Courses and Registration Period information.
* The system shall display Course Code, Course Name, Credit, Registration Status, Registration Start Date, Registration End Date, and Current Registration Status.
* Course registration status shall be shown as Registered or Dropped.

## FR16 — Drop Course (Student)
* The system shall allow the Student to select and drop a previously registered Course while the Drop Period is open.
* The system shall require confirmation and validate that the Course was registered by the Student.
* After a successful drop, the system shall update the Registration Status to Dropped, increase Available Seats by one, and display a success message.

## FR17 — View Grades (Student)
* The system shall allow the Student to select a Semester and view only their own Grades.
* The system shall display Course Code, Course Name, Credit, Grade, Semester, and Result Status.
* The system shall determine the Result Status as Passed or Not Passed and display an appropriate message when a Grade has not yet been entered.

## II. Non-Functional Requirements

### Product Requirements
#### Usability Requirements

###### Usability
- The system shall provide a clear, consistent, and user-friendly interface for Students, Lecturers, and Administrators.
- Course, prerequisite, recommended-semester, registration-status, and lecturer information shall be presented clearly.
- Course registration status shall be displayed clearly, including Registered, Dropped, and Failed where applicable.
- Lecturer-assignment status shall clearly indicate whether a course is Assigned or Unassigned.
- Error messages and notifications shall clearly explain the reason for failed operations.

#### Efficiency Requirements
###### Performance
- The system shall respond to common user requests such as login, course viewing, course registration, course dropping, teaching-course viewing, grade entry, grade updating, and grade viewing within 3 seconds under normal operating conditions.
- The system shall remain responsive during peak course-registration periods.

###### Scalability
- The system shall support an increasing number of students, lecturers, majors, courses, semesters, registration records, teaching assignments, and grade records.
- The system architecture shall support future functional expansion without requiring a complete redesign of the core system.

#### Dependability Requirements
###### Availability
- The system shall be available during normal academic operations and throughout active registration periods, except during scheduled maintenance.
- Scheduled maintenance should be performed outside active registration periods whenever possible.

###### Reliability
- The system shall ensure correct and reliable processing of course registration, course dropping, lecturer assignment, grade entry, and grade updates.
- If a transaction fails, incomplete changes shall be rolled back so that no partial or invalid data remains.
- The system shall prevent duplicate registration of the same course by the same student.

###### Data Integrity
- The system shall maintain valid relationships among Major, Student, Course, Lecturer, Teaching Qualification, Registration, Teaching Assignment, and Grade data.
- A student shall only register for courses belonging to the student's assigned major.
- A registered course shall reference an existing course.
- A lecturer assignment shall reference an existing lecturer and a valid course.
- A teaching assignment shall reference a valid Course and Lecturer.
- A Grade shall reference an existing Student and Course.
- A Lecturer shall only enter or update Grades for Students registered in Courses assigned to that Lecturer.
- A Student shall only view their own Grades.
- Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
- Deleting or updating records shall not create orphaned or inconsistent data.

###### Concurrency
- The system shall correctly handle simultaneous registration requests from multiple students.
- The system shall prevent duplicate registration records when multiple registration requests are processed concurrently.
- The system shall keep course registration data consistent after concurrent operations.
- Course registration transactions shall be processed atomically to prevent partial or duplicate registration records.
- The system shall correctly process concurrent registration requests without lost transactions or data inconsistency.

###### Backup and Recovery
- The system shall support scheduled backup of important user, course, registration, teaching-assignment, and grade data.
- The system shall provide a recovery mechanism for restoring valid data after a critical failure.
- The system shall support restoration of normal operation after an unexpected failure.
- Recovered data shall not contain duplicate, partial, or inconsistent registration records.

#### Security Requirements
###### Authentication

- The system shall require users to authenticate using a valid username and password before accessing protected functions.
- User passwords shall not be stored as plain text and shall be protected using a secure password-storage mechanism.
- After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.
- The system shall allow authenticated users to change their password after verifying the current password.

###### Authorization
- The system shall enforce role-based access control for Student, Lecturer, and Administrator accounts.
- Students shall only access student functions such as viewing courses, registering courses, dropping registered courses, viewing registration status, and viewing their own grades.
- Lecturers shall only access Courses assigned to them by an Administrator.
- Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
- Students shall only view their own Grades.
- Administrators shall have authority to manage users, majors, courses, semesters, registration periods, registration information, teaching qualifications, and lecturer assignments.
- Unauthorized access attempts shall be rejected by the system.

### 2. Organizational Requirements
#### Operational Requirements

###### Maintenance
- The system shall be designed to support easy maintenance and updates.
- Major functions such as user management, course management, semester management, registration, teaching assignment, and grade management should be separated into manageable modules.
- Maintenance and software updates shall preserve existing user, academic, registration, teaching-assignment, and grade data.

#### Development Requirements
###### Design Constraints
- The Course Registration System shall be implemented using Python and a relational database management system.
- The system shall use PostgreSQL as the relational database management system.
- The system shall use DBeaver to connect to and manage the PostgreSQL database.


## III. Data Flow Diagram
### Level 0:
<img width="1132" height="542" alt="Untitled Diagram" src="https://github.com/user-attachments/assets/7564516e-08c7-4f20-bb80-57619e83c80d" />

### Level 1:
<img width="2479" height="2253" alt="qaqaqaq drawio" src="https://github.com/user-attachments/assets/bb9fac43-8e25-4ee3-bb5d-e87d02260270" />

### Level 2:
<img width="867" height="582" alt="DFD" src="https://github.com/user-attachments/assets/541e1abe-b35c-4071-9aa5-026cf348835c" />

## IV. Use case Diagram
### 1. Overview Diagram
<img width="1602" height="2172" alt="UCFINAL" src="https://github.com/user-attachments/assets/1a95c490-e634-46f1-838d-a9e3e8f21c32" />

### 1.1. List of Actor
| STT | Actor | Meaning |
| :--- | :--- | :--- |
| 1 | Student | Users who register, search and manage their courses in the system. |
| 2 | Lecturer | Users who teach courses and view teaching-related information. |
| 3 | Administrator | System administrators who manage courses, lecturers, and registration policies. |
### 1.2. List of Use-cases
| STT | Use Case | Meaning |
| :--- | :--- | :--- |
| 1 | Login | Allows the Student, Lecturer, Admin to log in to the system using valid account credentials and access functions according to their role. |
| 2 | Manage Account | Allows the Student, Lecturer, Admin to log in, view personal account information, change password, and log out. |
| 3 | View Course | Allows the Student to view and search for courses belonging to their major. |
| 4 | Register Course | Allows the Student to select and register for courses during an open registration period. |
| 5 | Drop Course | Allows the Student to drop a successfully registered course while the drop period is open. |
| 6 | View Registration Status | Allows the Student to view registered/dropped courses and registration period details for a semester. |
| 7 | View Grades | Allows the Student to view their own grades and pass/fail status for each semester. |
| 8 | Manage Teaching Course | Allows the Lecturer to view courses assigned by the Admin for a selected semester. |
| 9 | Manage Student Grades | Allows the Lecturer to view registered students and enter or update grades for courses assigned to them. |
| 10 | Manage User | Allows the Admin to create, view, search, edit, and deactivate Student/Lecturer accounts. |
| 11 | Manage Major | Allows the Admin to create, view, edit, and delete majors. |
| 12 | Manage Curriculum | Allows the Admin to add or remove courses from a selected major's curriculum. |
| 13 | Manage Course | Allows the Admin to create, view, search, edit, and delete courses. |
| 14 | Manage Semester | Allows the Admin to create, view, edit, and delete academic semesters. |
| 15 | Manage Registration Period | Allows the Admin to set, open, and close the course registration period for a semester. |
| 16 | Manage Registration Demand | Allows the Admin to view registration demand, student lists, and generate reports. |
| 17 | Assign Lecturer | Allows the Admin to assign qualified lecturers to courses. |

### 2. Use Case: Login

#### 2.1 Summary

This use case allows Admin, Lecturer, and Student to log in to the Course Registration System using valid account credentials and access functions according to their role.

#### 2.2 Flow of Events

##### 2.2.1 Main Flow

1. The user selects the Login function.
2. The system requests the username and password.
3. The user enters the username and password.
4. The system verifies whether the username exists.
5. The system verifies whether the password is correct.
6. The system verifies whether the account is active.
7. If all credentials are valid, the system authenticates the user and determines access permissions based on the role.
8. The system grants access to the functions available for that role.

##### 2.2.2 Alternative Flows

A1. Invalid Username: If the username does not exist, the system displays an appropriate error message and requests reentry.
A2. Incorrect Password: If the password is incorrect, the system displays an appropriate error message and requests reentry.
A3. Inactive Account: If the account is not active, the system does not grant access.
A4. Too Many Failed Login Attempts: After 5 consecutive failed login attempts for the same account, the system temporarily blocks further login attempts for 15 minutes.

#### 2.3 Special Requirements

The system shall respond to login requests within 3 seconds under normal operating conditions.
Passwords shall not be stored as plain text and shall use a secure password-storage mechanism.
The system shall enforce role-based access control.

#### 2.4 Preconditions

The user has a valid account in the system.
The account is active.
The user is not currently logged in.

#### 2.5 Postconditions

Success: The user is authenticated and granted access according to the assigned role.
Failure: Access is not granted and an appropriate error message is displayed.

#### 2.6 Extension Points

None specified in the FR.

### 3. Use Case: Manage Account

#### 3.1 Summary

This use case allows an authenticated Admin, Lecturer, or Student to view their account information, change their password, and log out. The displayed information varies by role.

#### 3.2 Flow of Events

##### 3.2.1 Main Flow

1. The user selects Manage Account.
2. The system displays the user's account information according to their role.
3. The user views their account information.
4. The user may choose Change Password or Log out.
5. The system processes the selected action. Account information displayed by role:
   - Admin: username, full name, email, and role.
   - Lecturer: lecturer ID, username, full name, email, and role.
   - Student: student ID, username, full name, email, major, and role.

##### 3.2.2 Alternative Flows

A1. Duplicate ID: If the entered Student ID or Lecturer ID already exists, the system rejects the account creation and displays an appropriate error message.
A2. Invalid Email: If the entered Email format is invalid, the system rejects the input and displays an appropriate error message.
A3. Missing or Invalid User Information: If required user information is missing or invalid, the system does not save the information and displays an appropriate error message.
A4. Deactivation Cancelled: If the Admin does not confirm the deactivation, the system cancels the operation and the account remains active.

#### 3.3 Special Requirements

The current password must be verified before changing the password.
Passwords shall be protected using a secure password-storage mechanism.

#### 3.4 Preconditions

The user has successfully logged in.

#### 3.5 Postconditions

If the password is changed successfully, the new password is stored securely.
Otherwise, account information remains unchanged.

#### 3.6 Extension Points

Change Password.

## Admin Use Cases

### 4. Use Case: Manage User

#### 4.1 Summary

This use case allows the Admin to manage Student and Lecturer accounts by viewing, searching, creating, editing, and deactivating users.

#### 4.2 Flow of Events

##### 4.2.1 Main Flow

1. The Admin selects Manage User.
2. The system displays a list of Students and Lecturers.
3. The Admin chooses an action: View User, Search User, Create User Account, Edit User, or Deactivate User.
4. The system processes the selected action and displays the result.

##### 4.2.2 Alternative Flows

A1. Duplicate Major Code: If the entered Major Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Invalid Major Information: If the Admin enters missing or invalid Major information, the system does not save it and displays an appropriate error message.
A3. Major Cannot Be Deleted: If the selected Major is still referenced by existing Students or Curriculum data, the system rejects the deletion and displays an appropriate message.
A4. Deletion Not Confirmed: If the Admin does not confirm the deletion, the Major remains unchanged.

#### 4.3 Special Requirements

Student ID and Lecturer ID must be unique.
Email addresses must follow a valid format.
Confirmation is required before deactivating an account.
The system shall ensure that only one Admin account exists in the system.

#### 4.4 Preconditions

The Admin has successfully logged in.

#### 4.5 Postconditions

Success: Student or Lecturer accounts are created, updated, or deactivated according to the Admin's action.
Failure: No user data is changed.

#### 4.6 Extension Points

None specified in the FR.

### 5. Use Case: Manage Major

#### 5.1 Summary

This use case allows the Admin to create, view, edit, and delete Majors.

#### 5.2 Flow of Events

##### 5.2.1 Main Flow

1. The Admin selects Manage Major.
2. The system displays a list of Majors, including Major Code and Major Name.
3. The Admin chooses Create, View, Edit, or Delete Major.
4. The system processes the selected action.

##### 5.2.2 Alternative Flows

A1. Course Already in Curriculum: If the selected Course already exists in the selected Major's Curriculum, the system does not add the Course and displays an appropriate message.
A2. Invalid Recommended Semester: If the entered Recommended Semester is invalid, the system does not save the change and displays an appropriate error message.
A3. Removal Not Confirmed: If the Admin does not confirm the removal, the system cancels the operation and the Curriculum remains unchanged.

#### 5.3 Special Requirements

Major Code must be unique.
A Major may only be deleted if it is not referenced by any Student or Curriculum.
Confirmation is required before deletion.

#### 5.4 Preconditions

The Admin has successfully logged in.

#### 5.5 Postconditions

Success: The Major is created, updated, or deleted accordingly.
Failure: No Major data is changed.

#### 5.6 Extension Points

None specified in the FR.

### 6. Use Case: Manage Curriculum

#### 6.1 Summary

This use case allows the Admin to select a Major and manage the Courses belonging to that Major's Curriculum, including setting the Recommended Semester for each Course.

#### 6.2 Flow of Events

##### 6.2.1 Main Flow

1. The Admin selects Manage Curriculum.
2. The Admin selects a Major.
3. The system displays Courses belonging to the selected Major's Curriculum, including Course Code, Course Name, Credit, and Recommended Semester.
4. The Admin chooses Add Course to Curriculum or Remove Course from Curriculum, depending on whether the Course is already included in the selected Major's Curriculum.
5. The system processes the selected action.

##### 6.2.2 Alternative Flows

A1. Duplicate Course Code: If the entered Course Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Missing Required Information: If the Admin does not provide all required Course information, the system does not save the Course and displays an appropriate message.
A3. Invalid Prerequisite Selection: If the Admin selects the Course itself as its Prerequisite, the system rejects the selection and requests the Admin to select another Course.
A4. Changes Not Confirmed: If the Admin does not confirm the changes, the system cancels the operation and keeps the existing Course information unchanged.

#### 6.3 Special Requirements

A Course cannot be added to the same Major's Curriculum more than once.
The Course must exist in the Course Catalog before it can be added to a Curriculum.
Recommended Semester must be a valid value.
Confirmation is required before removing a Course.

#### 6.4 Preconditions

The Admin has successfully logged in.
At least one Major exists in the system.

#### 6.5 Postconditions

Success: The Curriculum is updated with the added or removed Course.
Failure: The Curriculum remains unchanged.

#### 6.6 Extension Points

None specified in the FR.

### 7. Use Case: Manage Course

#### 7.1 Summary

This use case allows the Admin to create, view, search, edit, and delete Courses, and to set a Prerequisite for a Course.

#### 7.2 Flow of Events

##### 7.2.1 Main Flow

1. The Admin selects Manage Course.
2. The system displays a list of Courses.
3. The Admin selects the appropriate action based on the intended task: View Course, Search Course, Create Course, Edit Course, Delete Course, or Set Prerequisite.
4. The system processes the selected action.

##### 7.2.2 Alternative Flows

A1. Duplicate Course Code: If the entered Course Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Missing or Invalid Course Information: If required Course information is missing or invalid, the system rejects the input and displays an appropriate error message.
A3. Invalid Prerequisite: If the selected Prerequisite does not exist or the Course is selected as its own Prerequisite, the system rejects the selection and displays an appropriate error message.
A4. Deletion Not Confirmed: If the Admin does not confirm the deletion, the Course remains unchanged.

#### 7.3 Special Requirements

Course Code must be unique.
A Course cannot be its own Prerequisite.
Credit must be a positive valid number.
Confirmation is required before deletion, and deletion must preserve data integrity.

#### 7.4 Preconditions

The Admin has successfully logged in.

#### 7.5 Postconditions

Success: The Course is created, updated, or deleted, or its Prerequisite is set accordingly.
Failure: No Course data is changed.

#### 7.6 Extension Points

Set Prerequisite.

### 8. Use Case: Manage Semester

#### 8.1 Summary

This use case allows the Admin to create, view, edit, and delete academic Semesters.

#### 8.2 Flow of Events

##### 8.2.1 Main Flow

1. The Admin selects Manage Semester.
2. The system displays a list of Semesters.
3. The Admin chooses Create Semester, View Semester, Edit Semester, or Delete Semester.
4. The system processes the selected action.

##### 8.2.2 Alternative Flows

A1. Invalid Semester Dates: If the Start Date is not earlier than the End Date, the system rejects the operation and displays an appropriate error message.
A2. Semester Date Overlap: If the Semester dates overlap with an existing Semester, the system rejects the operation and displays an appropriate error message.
A3. Semester In Use: If the selected Semester is referenced by existing Registration or academic data, the system does not allow the Semester to be deleted and displays an appropriate message.
A4. Deletion Not Confirmed: If the Admin does not confirm the deletion, the system cancels the operation and the Semester remains unchanged.

#### 8.3 Special Requirements

Start Date must be earlier than End Date.
Semesters must not overlap.
Confirmation is required before deletion.
A Semester referenced by Registration or academic data shall not be deleted.

#### 8.4 Preconditions

The Admin has successfully logged in.

#### 8.5 Postconditions

Success: The Semester is created, updated, or deleted accordingly.
Failure: No Semester data is changed.

#### 8.6 Extension Points

None specified in the FR.

### 9. Use Case: Manage Registration Period

#### 9.1 Summary

This use case allows the Admin to select a Semester its Course Registration Period. The Registration Period's status (Scheduled, Open, or Closed) is determined automatically by the system based on the current date, without requiring the Admin to manually open or close it.

#### 9.2 Flow of Events

##### 9.2.1 Main Flow

1. The Admin selects Manage Registration Period.
2. The Admin selects a Semester.
3. The Admin enters the Registration Start Date and Registration End Date.
4. The Admin confirms the schedule.
5. The system validates the Registration Start and End dates.
6. The system saves the Registration Period.
7. The system automatically determines the Registration Status (Scheduled, Open, or Closed) based on the current date.
8. The system displays the Registration Start Date/Time, Registration End Date/Time, and the current Registration Status.

##### 9.2.2 Alternative Flows

A1. Invalid Registration Period: If the Registration Start Date/Time is not earlier than the Registration End Date/Time, the system rejects the input and displays an appropriate error message..

#### 9.3 Special Requirements

Registration Start Date/Time must be earlier than Registration End Date/Time.
The Registration Period must fall within the selected Semester.
The Registration Status shall be automatically determined by the system based on the current date and the configured Start/End dates — the Admin does not manually open or close Registration.
Each Semester may have zero or more Registration Periods.
The system shall remain responsive during peak course-registration periods.

#### 9.4 Preconditions

The Admin has successfully logged in. clicked on Semester
At least one Semester exists.

#### 9.5 Postconditions

Success: The Registration Period is configured for the selected Semester, and its status is automatically reflected as Scheduled, Open, or Closed.
Failure: The Registration Period remains unchanged.

#### 9.6 Extension Points

None specified in the FR.

### 10. Use Case: Manage Registration Demand

#### 10.1 Summary

This use case allows the Admin to select a Semester and a Major, view registration demand per Course within that Major, view the Student registration list, search Courses, and generate a Registration Demand Report.

#### 10.2 Flow of Events

##### 10.2.1 Main Flow

1. The Admin selects Manage Registration Demand.
2. The Admin selects a Registration Period.
3. The Admin selects a Major.
4. The system displays the Courses belonging to the selected Major.
5. For each Course, the system displays the Number of Registered Students.
6. The Admin selects a Course.
7. The system displays the list of Students registered for the selected Course.

##### 10.2.2 Alternative Flows

A1. No Courses Found: If no Courses are found for the selected Major, the system displays an appropriate message.
A2. No Students Registered: If no Students have registered for the selected Course during the selected Registration Period, the system displays an appropriate message.

#### 10.3 Special Requirements

Registration Demand data must remain consistent with the current registration records.
Generated reports must accurately reflect the registration data.
Requests shall be processed within 3 seconds under normal operating conditions.

#### 10.4 Preconditions

The Admin has successfully logged in.
At least one Semester exists.

#### 10.5 Postconditions

Registration demand information is displayed and, when requested, a report is generated.
No Registration data is modified.

#### 10.6 Extension Points

Generate Registration Demand Report.

### 11. Use Case: Assign Lecturer

#### 11.1 Summary

This use case allows the Admin to select a Major and a Course, view Lecturers who are qualified to teach that Course, and assign a qualified Lecturer to the Course.

#### 11.2 Flow of Events

##### 11.2.1 Main Flow

1. The Admin selects Assign Lecturer.
2. The Admin selects a Major.
3. The Admin selects a Course.
4. The system identifies Lecturers who are qualified to teach the selected Course.
5. The system displays the list of qualified Lecturers.
6. The Admin selects a qualified Lecturer.
7. The system validates the Lecturer's qualification.
8. The system assigns the Lecturer to the Course.
9. The system displays a success message.

##### 11.2.2 Alternative Flows

A1. No Assigned Courses: If no Courses are assigned to the Lecturer for the selected Semester, the system displays an appropriate message.

#### 11.3 Special Requirements

Only Lecturers who are qualified to teach the selected Course can be assigned.
A Teaching Assignment shall reference an existing Lecturer and a valid Course.
The system shall prevent invalid Lecturer-Course assignments.
Requests shall be processed within 3 seconds under normal operating conditions.

#### 11.4 Preconditions

The Admin has successfully logged in.
At least one Course exists.

#### 11.5 Postconditions

Success: The Teaching Assignment is saved and a success message is displayed.
Failure: No Teaching Assignment is created.

#### 11.6 Extension Points

None specified in the FR.

## Lecturer Use Cases

### 12. Use Case: Manage Teaching Course

#### 12.1 Summary

This use case allows the Lecturer to select a Semester and view the Courses directly assigned to them by the Admin. The Lecturer cannot self-select, request, or modify their teaching assignment.

#### 12.2 Flow of Events

##### 12.2.1 Main Flow

1. The Lecturer selects Manage Teaching Course.
2. The Lecturer selects a Semester.
3. The system retrieves Courses assigned to the Lecturer by the Admin for the selected Semester.
4. The system displays Course Code, Course Name, Credit, and Prerequisite.
5. The Lecturer selects an assigned Course.
6. The system displays the details of the selected Course.

##### 12.2.2 Alternative Flows

A1. No Courses Assigned: If no Courses have been assigned to the Lecturer for the selected Semester, the system displays an appropriate message.
A2. Assignment Changed by Admin: When the Admin creates, changes, or removes a Teaching Assignment, the system updates the Lecturer's teaching Course list accordingly.

#### 12.3 Special Requirements

Teaching-course viewing shall respond within 3 seconds under normal operating conditions.
Lecturers shall only access Courses assigned to them by the Admin.
The Lecturer shall not independently select, register for, request, self-assign, or modify a Course assignment.

#### 12.4 Preconditions

The Lecturer has successfully logged in.
A Semester is selected.

#### 12.5 Postconditions

The Lecturer can view the current list of Courses assigned by the Admin.
No Teaching Assignment is modified by the Lecturer.
Display the list of subjects analyzed by the administrator.

#### 12.6 Extension Points

None specified in the FR.

### 13. Use Case: Manage Student Grades

#### 13.1 Summary

This use case allows the Lecturer to select a Semester and a Course assigned to them, view Students registered in that Course, view a Student's Prerequisite status, and enter or update the Student's Grade.

#### 13.2 Flow of Events

##### 13.2.1 Main Flow

1. The Lecturer selects Manage Student Grades.
2. The Lecturer selects a Semester.
3. The system checks that the Registration Period for the selected Semester has ended.
4. The system displays the Courses assigned to the Lecturer by the Admin for the selected Semester.
5. The Lecturer selects an assigned Course.
6. The system displays the Students registered in the selected Course, including Student ID, Student Name, and Email.
7. The Lecturer selects a Student to view the Student's information.
8. The Lecturer enters or updates the Student's Grade.
9. The system validates the Grade, the Student's Registration, and the Lecturer's Course assignment.
10. If the validation succeeds, the system saves the Grade.
11. The system displays a success message.

##### 13.2.2 Alternative Flows

A1. Invalid Grade: If the entered Grade is invalid, the system does not save the Grade and displays an appropriate error message.
A2. Student Not Registered: If the Student is not registered in the selected Course, the system does not allow the Lecturer to enter or update the Grade and displays an appropriate message.
A3. Course Not Assigned: If the selected Course is not assigned to the Lecturer, the system does not allow the Lecturer to manage Grades for that Course and displays an appropriate message.
A4. Grade Save Failed: If the Grade cannot be saved, the system displays an appropriate error message and the existing Grade data remains unchanged.

#### 13.3 Special Requirements

Grade entry and updating shall respond within 3 seconds under normal operating conditions.
A Grade shall reference an existing Student and Course.
Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
The Lecturer may view the Student's Prerequisite status for the selected Course but shall not modify it. Failed transactions shall not leave partial or invalid data.

#### 13.4 Preconditions

The Lecturer has successfully logged in.
The selected Semester exists.
The selected Course is assigned to the Lecturer.
The Student is registered in the selected Course.

#### 13.5 Postconditions

Success: The valid Grade is stored or updated for the correct Student and Course.
Failure: Existing Grade data remains valid and no invalid Grade is stored.

#### 13.6 Extension Points

None specified in the FR.

## Student Use Cases

### 14. Use Case: View Courses

#### 14.1 Summary

This use case allows the Student to view Courses belonging to their Major, search Courses by Course Code or Course Name, and view detailed Course information.

#### 14.2 Flow of Events

##### 14.2.1 Main Flow

1. The Student selects View Courses.
2. The system identifies the Student's Major.
3. The system displays Courses belonging to the Student's Major.
4. The Student may search for a Course using Course Code or Course Name.
5. The Student selects a Course.
6. The system displays Course Code, Course Name, Credit, Prerequisite, and Recommended Semester.
7. The Student views the Course information.

##### 14.2.2 Alternative Flows

A1. Course Not Found: If no Course matches the entered Course Code or Course Name, the system displays an appropriate message.

#### 14.3 Special Requirements

Course, prerequisite, and recommended-semester information shall be presented clearly.
Course viewing requests shall be processed within 3 seconds under normal operating conditions.

#### 14.4 Preconditions

The Student has successfully logged in.
The student's major is already in the system.

#### 14.5 Postconditions

The requested Course information is displayed.
No Course or Student data is modified.

#### 14.6 Extension Points

None specified in the FR.

### 15. Use Case: Course Registration

#### 15.1 Summary

This use case allows the Student to select and register for an available Course belonging to the Student's Major/Curriculum. Before confirmation, the system validates the Registration Period, Prerequisite requirements, and duplicate registration.

#### 15.2 Flow of Events

##### 15.2.1 Main Flow

1. The Student selects a Course to register from the available Courses. The Student may select a recommended Course or another available Course.
2. The system checks whether the Registration Period is open.
3. The system checks whether the Student has satisfied the required Prerequisite.
4. The system verifies that the Student does not already have an active registration for the same Course.
5. If all checks pass, the system allows the Student to confirm the registration.
6. The Student confirms the registration.
7. The system saves the Registration.
8. The system displays a success message.

##### 15.2.2 Alternative Flows

A1. Registration Period Not Open: If the Registration Period is not open, the system rejects the registration and displays an appropriate error message.
A2. Prerequisite Not Satisfied: If the Student has not satisfied the required Prerequisite, the system rejects the registration and displays an appropriate error message.
A3. Duplicate Registration: If the Student already has an active Registration for the selected Course, the system rejects the registration and displays an appropriate error message.
A4. Student Does Not Confirm: If the Student does not confirm the registration, no Registration record is created.

#### 15.3 Special Requirements

Registration shall be processed within 3 seconds under normal operating conditions.
The system shall prevent duplicate active registrations.
Registration transactions shall be processed atomically.
Simultaneous registration requests shall not result in lost transactions or inconsistent data.
A Student shall only register for Courses belonging to the Student's assigned Major.

#### 15.4 Preconditions

The Student has successfully logged in.
The Student has selected an available Course to register.

#### 15.5 Postconditions

Success: A valid Registration record is saved and a success message is displayed.
Failure: No invalid or partial Registration record is stored.

#### 15.6 Extension Points

None specified in the FR.

### 16. Use Case: View Registration Status

#### 16.1 Summary

This use case allows the Student to select a Semester and view registered Courses, Course registration status, and Registration Period information.

#### 16.2 Flow of Events

##### 16.2.1 Main Flow

1. The Student selects View Registration Status.
2. The Student selects a Semester.
3. The system retrieves the Student's Course registration information.
4. The system displays Course Code, Course Name, Credit, and Registration Status.
5. The system displays Semester, Registration Start Date, Registration End Date, and Current Registration Status.
6. The system displays the Course registration status as Registered or Dropped.

##### 16.2.2 Alternative Flows

A1. No Registration Record: If the Student has no registration information for the selected Semester, the system displays an appropriate message.

#### 16.3 Special Requirements

Registration status shall be displayed clearly, including Registered and Dropped.
Registration information must remain associated with the correct Student and Course.

#### 16.4 Preconditions

The Student has successfully logged in.
A Semester has been selected.

#### 16.5 Postconditions

The Student's Registration Status and Registration Period information are displayed.
No Registration data is modified.

#### 16.6 Extension Points

None specified in the FR.

### 17. Use Case: Drop Course

#### 17.1 Summary

This use case allows the Student to select and drop a previously registered Course when the Drop Period is still open.

#### 17.2 Flow of Events

##### 17.2.1 Main Flow

1. The Student selects Drop Course.
2. The system displays the Student's actively registered Courses.
3. The Student selects a Course to drop.
4. The system verifies that the Drop Period is still open.
5. If the Drop Period is open, the system asks the Student to confirm the drop.
6. The Student confirms dropping the Course.
7. The system updates the Registration Status to Dropped.
8. The system displays a success message.

##### 17.2.2 Alternative Flows

A1. Drop Period Closed: If the Drop Period is no longer open, the system rejects the drop request and displays an appropriate error message.
A2. Student Does Not Confirm: If the Student does not confirm the drop, the system cancels the operation and the Registration remains unchanged.

#### 17.3 Special Requirements

Course dropping shall be processed within 3 seconds under normal operating conditions.
The system shall reliably process the operation and roll back incomplete changes if the transaction fails.
Registration data shall remain consistent after the Course is dropped.

#### 17.4 Preconditions

The Student has successfully logged in.
The Student has previously registered for the selected Course.

#### 17.5 Postconditions

Success: The Registration Status is updated to Dropped, and the Course is no longer active.
Failure: The existing Registration information remains unchanged.

#### 17.6 Extension Points

None specified in the FR.

### 18. Use Case: View Grades

#### 18.1 Summary

This use case allows the Student to select a Semester and view their own Grades and Result Status for Courses.

#### 18.2 Flow of Events

##### 18.2.1 Main Flow

1. The Student selects View Grades.
2. The Student selects a Semester.
3. The system retrieves the Student's Grade information.
4. The system displays Course Code, Course Name, Credit, Grade, and Semester.
5. The system automatically uses the Grade to determine the Result Status.
6. The system displays the Result Status as Passed or Not Passed.
7. The Student views their Grade information.

##### 18.2.2 Alternative Flows

A1. Grade Not Yet Entered: If a Grade has not yet been entered, the system displays an appropriate message instead of presenting a completed Grade result.

#### 18.3 Special Requirements

The Student shall only be able to view their own Grades.
Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
Grade viewing requests shall be processed within 3 seconds under normal operating conditions.
Unauthorized access to another Student's Grades shall be rejected.

#### 18.4 Preconditions

The Student has successfully logged in.

#### 18.5 Postconditions

The Student's Grade and Result Status information is displayed.
No Grade data is modified.

#### 18.6 Extension Points

None specified in the FR.

## V. Class Diagram
<img width="803" height="974" alt="classFinal" src="https://github.com/user-attachments/assets/6701f9b6-81e4-49ef-be4d-b8c251302111" />

## VI. Data Model
<img width="1172" height="1012" alt="DATA_MODEL_final drawio" src="https://github.com/user-attachments/assets/df33eb66-ab00-42b3-a99e-77b2473790d7" />

## VII. Interface Design Description

### 1. Admin
### 2. Student
<img width="928" height="846" alt="Screenshot 2026-08-23 220015" src="https://github.com/user-attachments/assets/15a2ac31-d85f-4579-8902-82db5dff824c" />
<img width="1916" height="844" alt="Screenshot 2026-08-23 220106" src="https://github.com/user-attachments/assets/d6056093-c8bf-4c37-9ca6-a46731422b98" />
<img width="1919" height="847" alt="Screenshot 2026-08-23 220116" src="https://github.com/user-attachments/assets/2b4b8dd4-0a50-4a9a-ae1e-4d424b97b2b8" />
<img width="1919" height="840" alt="Screenshot 2026-08-23 220132" src="https://github.com/user-attachments/assets/29a0c0c5-1894-452a-b5a8-f890883ad1a7" />
<img width="1919" height="845" alt="Screenshot 2026-08-23 220156" src="https://github.com/user-attachments/assets/50066f46-39fc-4b10-bcc7-69fe72bc60e2" />
<img width="1919" height="844" alt="Screenshot 2026-08-23 220202" src="https://github.com/user-attachments/assets/b3cb20ce-4535-447d-962a-a79b03c4d60e" />
<img width="1919" height="842" alt="Screenshot 2026-08-23 220214" src="https://github.com/user-attachments/assets/a6d23f20-51a0-48f7-b07c-3c837b63c5e8" />
<img width="1919" height="914" alt="Screenshot 2026-08-23 220222" src="https://github.com/user-attachments/assets/67b20618-31b6-4292-9e67-ca1e4ca18ee8" />
<img width="1919" height="910" alt="Screenshot 2026-08-23 220228" src="https://github.com/user-attachments/assets/993faec2-5cc9-416d-b95e-b1ef6adb5d7a" />
<img width="1919" height="842" alt="Screenshot 2026-08-23 220246" src="https://github.com/user-attachments/assets/93fe0c1e-0d0a-440c-b62f-f6050a2a733e" />
<img width="1919" height="910" alt="Screenshot 2026-08-23 220301" src="https://github.com/user-attachments/assets/7f5d847f-60d7-49e5-9c60-82f1c540df5a" />
<img width="1919" height="842" alt="Screenshot 2026-08-23 220309" src="https://github.com/user-attachments/assets/45e243d1-22f3-4ee4-a77e-9020283a297d" />




### 3. Lect
<img width="1920" height="910" alt="image" src="https://github.com/user-attachments/assets/1693840e-4ce3-47d6-b6b3-3b83aa098e39" />
<img width="1920" height="914" alt="image" src="https://github.com/user-attachments/assets/925f8ca2-2757-4498-8ad9-8f26a6557f0f" />
<img width="1920" height="913" alt="image" src="https://github.com/user-attachments/assets/4e4ecd7b-b3ed-40c8-8668-945dff5194cd" />
<img width="1920" height="913" alt="image" src="https://github.com/user-attachments/assets/c0f56f78-532c-4e2e-b0ef-167429c33591" />
<img width="1920" height="910" alt="image" src="https://github.com/user-attachments/assets/fcfdb4d0-0801-4f13-9c57-d64f31ea3557" />
<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/490741b2-fd06-4842-91e0-602d53040903" />












