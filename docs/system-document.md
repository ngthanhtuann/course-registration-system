# COURSE REGISTRATION SYSTEM SPECIFICATION

## I. Functional Requirements

### 1. Login (User Authentication)
- The system shall allow Admin, Lecturer, and Student to log in using valid account credentials.
- The system shall require users to enter:
  - Username.
  - Password.
- The system shall verify:
  - Whether the username exists.
  - Whether the password is correct.
  - Whether the account is active.
- If the credentials are valid, the system shall grant access according to the user's role:
  - Admin.
  - Lecturer.
  - Student.
- If the credentials are invalid, the system shall display an appropriate error message and request re-entry.

### 2. Manage Account
- The system shall allow Admin, Lecturer, and Student to view account information.
- The system shall display the following account information according to the user's role:
  - Admin: username, full name, email, and role.
  - Lecturer: lecturer ID, username, full name, email and role.
  - Student: student ID, username, full name, email, major, and role.
- The system shall allow Admin, Lecturer, and Student to change their password.
- The user shall enter the current password.
- The user shall enter the new password.
- The user shall confirm the new password.
- The system shall validate the entered password information.
- The system shall display a success or error message after the password change.
- The system shall allow Admin, Lecturer, and Student to log out of the system.
  
### 3. Manage user
#### 3.1 Manage Student
- The system shall allow the Admin to view Students.
- The system shall display:
  - Student ID.
  - Student Name.
  - Date of Birth.
  - Email.
  - Major.
  - Account Status.
- The system shall allow the Admin to search Students by:
  - Student ID.
  - Student Name.
  - Major.
- The system shall allow the Admin to create a Student.
- When creating a Student, the system shall require:
  - Student ID.
  - Full Name.
  - Date of Birth.
  - Email.
  - Major.
- The system shall validate that the Student ID is unique.
- The system shall validate that the Email is valid.
- The system shall allow the Admin to edit Student information.
- The system shall allow the Admin to change:
  - Full Name.
  - Date of Birth.
  - Email.
  - Major.
- The system shall allow the Admin to delete or deactivate a Student.
- The system shall require confirmation before deleting or deactivating a Student.
- The system shall allow the Admin to view detailed Student information.
#### 3.2 Manage Lecturer
- The system shall allow the Admin to view Lecturers.
- The system shall display:
  - Lecturer ID.
  - Lecturer Name.
  - Email.
  - Qualification for teaching.
  - Account Status.
- The system shall allow the Admin to search Lecturers by:
  - Lecturer ID.
  - Lecturer Name.
- The system shall allow the Admin to create a Lecturer.
- When creating a Lecturer, the system shall require:
  - Lecturer ID.
  - Full Name.
  - Email.
  - Qualified Courses.
- The system shall validate that the Lecturer ID is unique.
- The system shall validate that the Email is valid.
- The system shall allow the Admin to edit Lecturer information.
- The system shall allow the Admin to delete or deactivate a Lecturer.
- The system shall allow the Admin to set the teaching qualifications of a Lecturer.
- The system shall allow the Admin to view detailed Lecturer information.
- The system shall ensure that only one Admin account exists in the system.

### 4. Manage Major
- The system shall allow the Admin to view Majors.
- The system shall display:
  - Major Code.
  - Major Name.
- The system shall allow the Admin to create a Major.
- When creating a Major, the system shall require:
  - Major Code.
  - Major Name.
- The system shall validate that the Major Code is unique.
- The system shall allow the Admin to edit Major information.
- The system shall allow the Admin to delete a Major.
- The system shall check whether the Major is being used before deletion.
- The system shall allow the Admin to view Major information.

### 5. Manage Curriculum
- The system shall allow the Admin to select a Major.
- The system shall allow the Admin to view Courses belonging to the selected Major.
- The system shall display:
  - Course Code.
  - Course Name.
  - Credit.
  - Prerequisite
  - Recommended Semester.
- The system shall allow the Admin to add a Course to the selected Major's Curriculum.
- When adding a Course, the system shall allow the Admin to:
  - Select a Course.
  - Set the Recommended Semester.
- The system shall allow the Admin to remove a Course from the Curriculum.
- The system shall require confirmation before removing a Course.
  
### 6. Manage Courses (Admin)
* The system shall allow the Admin to view Courses.
* The system shall allow the Admin to search Courses by:
  * Course Code.
  * Course Name.
* The system shall allow the Admin to create a Course.
* When creating a Course, the system shall require:
  * Course Code.
  * Course Name.
  * Credit.
  * Prerequisite.
* The system shall allow the Admin to select a Course.
* The system shall allow the Admin to view Course information, including:
  * Course Code.
  * Course Name.
  * Credit.
  * Prerequisite.
* The system shall allow the Admin to edit Course information.
* The system shall allow the Admin to delete a Course.
* The system shall require confirmation before deleting a Course.
* The system shall allow the Admin to set a prerequisite for a Course.
* The system shall validate that:
  * The Course Code is unique.
  * The Credit is valid.
  * The prerequisite is an existing Course.
  * A Course cannot be its own prerequisite.

### 7. Manage Semester (Admin)
* The system shall allow the Admin to create a Semester.
* When creating a Semester, the system shall require:
* The system shall allow the Admin to set:
  * Semester Name.
  * Start Date.
  * End Date.
* The system shall allow the Admin to select a Semester.
* The system shall allow the Admin to view Semester information, 
including:
  * Semester Name.
  * Start Date.
  * End Date.
  * Semester Status.
* The system shall allow the Admin to edit Semester information.
* The system shall allow the Admin to delete a Semester.
* The system shall require confirmation before deleting a Semester.
* The system shall validate that:
  *  The Start Date is earlier than the End Date.
  *  Semesters do not overlap.
  *  Semester dates are valid.  

### 8. Manage Registration Period (Admin)
* The system shall allow the Admin to select a Semester.
* The system shall allow the Admin to set the Registration Period by specifying:
  * Registration Period's name.
  * Start Date
  * End Date
* The system shall validate the entered Registration Period:
  * Start Date and End Date must not be empty.
  * Start Date must be earlier than End Date.
* The system shall automatically manage and update the Registration Status based on the current system date:
  * Upcoming: Current date is before Start Date.
  * Open: Current date is between Start Date and End Date.
  * Closed: Current date is after End Date.
* The system shall display the Registration Period information:
  * Registration Period's name.
  * Start Date.
  * End Date.
  * Current Registration Status (Upcoming, Open, Closed).

### 9. Manage Registration Demand (Admin)
* The system shall allow the Admin to select a Registration Period.
* The system shall display a list of Majors for the selected Registration Period.
* The system shall allow the Admin to select a Major to view its Course List.
* The Course List shall display:
  * Course Code.
  * Course Name.
  * Number of Registered Students.
* The system shall allow the Admin to generate a Registration Demand Report.
* The Registration Demand Report shall include:
* Course Code.
* Course Name.
* Number of Students.
* Registered student list.

### 10. Assign Lecturer (Admin)
* The system shall allow the Admin to select a Major.
* The system shall allow the Admin to select a Course.
* The system shall display Lecturers who are qualified to teach the selected Course.
* The system shall allow the Admin to view Lecturer qualifications.
* The system shall allow the Admin to select a qualified Lecturer.
* The system shall allow the Admin to assign the selected Lecturer to the Course.
* The system shall validate that:
  * The Lecturer is qualified to teach the Course.
* The system shall display a success message when the assignment is completed successfully.
* The system shall display an error message if the assignment cannot be completed.

### 11. Manage Teaching Course (Lecturer)
* The system shall allow the Lecturer to select a Semester.
* The system shall allow the Lecturer to view the Courses information directly assigned to them by the Admin for the selected Semester.
* The system shall display:
  * Course Code
  * Course Name
  * Credit
  * Prerequisite
* The system shall **not** allow the Lecturer to select or register for a Course independently.
* The system shall **not** allow the Lecturer to request or assign themselves to a Course.
* The system shall **not** allow the Lecturer to modify the Course assignment made by the Admin.
* The system shall allow the Lecturer to view their teaching Courses according to the Admin's assignments.
* The system shall update the Lecturer's teaching Course list when the Admin creates, changes, or removes a teaching assignment.
### 12. Manage Student Grades (Lecturer)

* The system shall allow the Lecturer to select a Semester.
* The system shall allow the Lecturer to view Courses assigned to them by the Admin.
* The system shall allow the Lecturer to select a Course.
* The system shall allow the Lecturer to view only Course taught by them.
* The system shall display:
  * Course Code.
  * Course Name.
* The system shall allow the Lecturer to view Students registered in the selected Course.
* The system shall display:
  * Student ID.
  * Student Name.
  * Email.
* The system shall allow the Lecturer to select a Student.
* The system shall allow the Lecturer to view Student information.
* The system shall allow the Lecturer to enter or update the Student's Grade.
* The Lecturer shall enter a Grade.
* The system shall validate the Grade.
* The system shall save the Grade if the validation is successful.
* The system shall display a success or error message after saving the Grade.
* The system shall ensure that:
  * The Student is registered in the selected Course.
  * The Course is assigned to the Lecturer by the Admin.
  * The Grade is within the valid grading range.
* The system shall not allow the Lecturer to enter or update Grades for Students in Course taught by another Lecturer.
* The system shall not allow the Lecturer to enter or update Grades for Courses that were not assigned to them by the Admin.

### 13. View Courses (Student)
* The system shall allow the Student to view Courses belonging to their Major.
* The system shall allow the Student to search for Courses by:
  * Course Code.
  * Course Name.
* The system shall allow the Student to select a Course to view detailed information.
* The system shall display:
  * Course Code.
  * Course Name.
  * Credit.
  * Prerequisite.
  * Recommended Semester.
### 14. Course Registration (Student)
* The system shall allow the Student to select a Course to register.
* The system shall validate the registration before allowing the Student to confirm.
* The system shall check that:
  * The Registration Period is open.
  * The Course belongs to the Student's Major / Curriculum.
  * The Prerequisite has been satisfied.
* If any validation fails, the system shall reject the registration and display an appropriate error message.
* If all validations pass, the system shall allow the Student to confirm the registration.
* After successful registration, the system shall:
  * Save the registration.
  * Display a success message.

### 15. View Registration Status (Student)
* The system shall allow the Student to select a Semester.
* The system shall allow the Student to view their registered Course.
* The system shall display:
  * Course Code.
  * Course Name.
  * Credit.
  * Registration Status.
* The system shall allow the Student to view the Registration Period.
* The system shall display:
  * Semester.
  * Registration Start Date.
  * Registration End Date.
  * Current Registration Status.
* The system shall display whether the Course registration was:
  * Registered.
  * Dropped.

### 16. Drop Course (Student)
* The system shall allow the Student to view registered Course.
* The system shall allow the Student to select a registered Course.
* The system shall display:
  * Course ID
  * Courses Name
* The system shall allow the Student to confirm dropping the Course.
* The system shall validate that:
  * The Course was registered by the Student.
  * The Drop Period is still open.
* If the validation is successful, the system shall:
  * Remove the Student's registration.
  * Update the Registration Status.
  * Display a success message.
* If the validation fails, the system shall display an appropriate error message.

### 17. View Grades (Student)
* The system shall allow the Student to select a Semester.
* The system shall allow the Student to view their Grades.
* The system shall display:
  * Course Code.
  * Course Name.
  * Credit.
  * Grade.
  * Semester.
  * Result Status (passed / not passed)
* The system shall automatically calculate grade to check result status.
* The system shall display an appropriate message when a Grade has not yet been entered.
* The Student shall only be able to view their own Grades.
## II. Non-Functional Requirements

### Product Requirements
#### Usability Requirements

###### Usability
* The system shall provide a clear, consistent, and user-friendly interface for Students, Lecturers, and Administrators.
* Course, prerequisite, recommended-semester, registration-status, and lecturer information shall be presented clearly.
* Course registration status shall be displayed clearly, including Registered, Dropped, and Failed where applicable.
* Lecturer-assignment status shall clearly indicate whether a course is Assigned or Unassigned.
* Error messages and notifications shall clearly explain the reason for failed operations.

#### Efficiency Requirements
###### Performance
* The system shall respond to common user requests such as login, course viewing, course registration, course dropping, teaching-course viewing, grade entry, grade updating, and grade viewing within 3 seconds under normal operating conditions.
* The system shall remain responsive during peak course-registration periods.

###### Scalability
* The system shall support an increasing number of students, lecturers, majors, courses, semesters, registration records, teaching assignments, and grade records.
* The system architecture shall support future functional expansion without requiring a complete redesign of the core system.

#### Dependability Requirements
###### Availability
* The system shall be available during normal academic operations and throughout active registration periods, except during scheduled maintenance.
* Scheduled maintenance should be performed outside active registration periods whenever possible.

###### Reliability
* The system shall ensure correct and reliable processing of course registration, course dropping, lecturer assignment, grade entry, and grade updates.
* If a transaction fails, incomplete changes shall be rolled back so that no partial or invalid data remains.
* The system shall prevent duplicate registration of the same course by the same student.

###### Data Integrity
* The system shall maintain valid relationships among Major, Student, Course, Lecturer, Teaching Qualification, Registration, Teaching Assignment, and Grade data.
* A student shall only register for courses belonging to the student's assigned major.
* A registered course shall reference an existing course.
* A lecturer assignment shall reference an existing lecturer and a valid course.
* A teaching assignment shall reference a valid Course and Lecturer.
* A Grade shall reference an existing Student and Course.
* A Lecturer shall only enter or update Grades for Students registered in Courses assigned to that Lecturer.
* A Student shall only view their own Grades.
* Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
* Deleting or updating records shall not create orphaned or inconsistent data.

###### Concurrency
* The system shall correctly handle simultaneous registration requests from multiple students.
* The system shall prevent duplicate registration records when multiple registration requests are processed concurrently.
* The system shall keep course registration data consistent after concurrent operations.
* Course registration transactions shall be processed atomically to prevent partial or duplicate registration records.
* The system shall correctly process concurrent registration requests without lost transactions or data inconsistency.

###### Backup and Recovery
* The system shall support scheduled backup of important user, course, registration, teaching-assignment, and grade data.
* The system shall provide a recovery mechanism for restoring valid data after a critical failure.
* The system shall support restoration of normal operation after an unexpected failure.
* Recovered data shall not contain duplicate, partial, or inconsistent registration records.

#### Security Requirements
###### Authentication

* The system shall require users to authenticate using a valid username and password before accessing protected functions.
* User passwords shall not be stored as plain text and shall be protected using a secure password-storage mechanism.
* After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.
* The system shall allow authenticated users to change their password after verifying the current password.

###### Authorization
* The system shall enforce role-based access control for Student, Lecturer, and Administrator accounts.
* Students shall only access student functions such as viewing courses, registering courses, dropping registered courses, viewing registration status, and viewing their own grades.
* Lecturers shall only access Courses assigned to them by an Administrator.
* Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
* Students shall only view their own Grades.
* Administrators shall have authority to manage users, majors, courses, semesters, registration periods, registration information, teaching qualifications, and lecturer assignments.
* Unauthorized access attempts shall be rejected by the system.

### 2. Organizational Requirements
#### Operational Requirements

###### Maintenance
* The system shall be designed to support easy maintenance and updates.
* Major functions such as user management, course management, semester management, registration, teaching assignment, and grade management should be separated into manageable modules.
* Maintenance and software updates shall preserve existing user, academic, registration, teaching-assignment, and grade data.

#### Development Requirements
###### Design Constraints
* The Course Registration System shall be implemented using Python and a relational database management system.
* The system shall use PostgreSQL as the relational database management system.
* The system shall use DBeaver to connect to and manage the PostgreSQL database.
---

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
* This use case allows Admin, Lecturer, and Student to log in to the Course Registration System using valid account
credentials and access functions according to their role.

#### 2.2 Flow of Events
##### 2.2.1 Main Flow
  * 1.The user selects the Login function.
  * 2.The system requests the username and password.
  * 3.The user enters the username and password.
  * 4.The system verifies whether the username exists.
  * 5.The system verifies whether the password is correct.
  * 6.The system verifies whether the account is active.
  * 7.If all credentials are valid, the system authenticates the user and determines access
permissions based on the role.
  * 8.The system grants access to the functions available for that role.

##### 2.2.2 Alternative Flows
* A1. Invalid Username: If the username does not exist, the system displays an appropriate error message and requests re-entry.
* A2. Incorrect Password: If the password is incorrect, the system displays an appropriate error message and requests re-entry.
* A3. Inactive Account: If the account is not active, the system does not grant access.
* A4. Too Many Failed Login Attempts: After 5 consecutive failed login attempts for the same account, the system temporarily blocks further login attempts for 15 minutes.

#### 2.3 Special Requirements
* The system shall respond to login requests within 3 seconds under normal operating conditions.
* Passwords shall not be stored as plain text and shall use a secure password-storage mechanism.
* The system shall enforce role-based access control.

#### 2.4 Preconditions
* The user has a valid account in the system.
* The account is active.
* The user is not currently logged in.

#### 2.5 Postconditions
* Success: The user is authenticated and granted access according to the assigned role.
* Failure: Access is not granted and an appropriate error message is displayed.

#### 2.6 Extension Points
* None.

### 3. Use Case: Manage Account
#### 3.1 Summary
* This use case allows an authenticated Admin, Lecturer, or Student to view their account information, change their
password, and log out. The displayed information varies by role.

#### 3.2 Flow of Events
##### 3.2.1 Main Flow
  * 1.The user selects Manage Account.
  * 2.The system displays the user's account information according to their role.
  * 3.The user views their account information.
  * 4.The user may choose Change Password or Log out.
  * 5.The system processes the selected action.
  * Account information displayed by role:
    - Admin: username, full name, email, and role.
    - Lecturer: lecturer ID, username, full name, email, and role.
    - Student: student ID, username, full name, email, major, and role.

##### 3.2.2 Alternative Flows
* A1. Change Password: The user enters the current password and a new password. The system validates the
entered password information. If valid, the system updates the password and displays a success message.
* A2. Invalid Password Information: If password validation fails, the system displays an error message and does not
change the password.
* A3. Log out: The user selects Log out. The system terminates the current session and redirects the user to the Login
page.

#### 3.3 Special Requirements
* The current password must be verified before changing the password.
* Passwords shall be protected using a secure password-storage mechanism.

#### 3.4 Preconditions
* The user has successfully logged in.

#### 3.5 Postconditions
* If the password is changed successfully, the new password is stored securely.
Otherwise, account information remains unchanged.

#### 3.6 Extension Points
* Change Password.

### 4. Use Case: Manage User
#### 4.1 Summary
* This use case allows the Admin to manage Student and Lecturer accounts by viewing, searching, creating, editing, and
deactivating users.

#### 4.2 Flow of Events
##### 4.2.1 Main Flow
* 1.The Admin selects Manage User.
* 2.The system displays a list of Students and Lecturers.
* 3.The Admin chooses an action: View User, Search User, Create User Account, Edit User, or Deactivate User.
* 4.The system processes the selected action and displays the result.

##### 4.2.2 Alternative Flows
* A1. Create User Account: The Admin enters the required information: Student ID/Lecturer ID, Full Name, Email,
Major for Student, or Teaching Qualifications for Lecturer. The system validates ID uniqueness and email format, creates
the account, and displays a success message.
* A2. Duplicate ID or Invalid Email: If the entered ID already exists or the Email format is invalid, the system rejects the
creation and displays an error message.
* A3. View User: The Admin selects a user and the system displays detailed information according to the user's role.
* A4. Search User: The Admin enters criteria such as ID, Name, or Major. The system filters and displays matching users.
* A5. Edit User: The Admin selects a user, modifies the allowed information, and the system validates and saves the
changes.
* A6. Deactivate User: The Admin selects a user and chooses Deactivate. The system requests confirmation, deactivates
the account upon confirmation, and displays a success message.

#### 4.3 Special Requirements
* Student ID and Lecturer ID must be unique.
* Email addresses must follow a valid format.
* Confirmation is required before deactivating an account.
* The system shall ensure that only one Admin account exists in the system.

#### 4.4 Preconditions
* The Admin has successfully logged in.

#### 4.5 Postconditions
* Success: Student or Lecturer accounts are created, updated, or deactivated according to the Admin's action.
* Failure: No user data is changed.

#### 4.6 Extension Points
* None.

### 5. Use Case: Manage Major
#### 5.1 Summary
* This use case allows the Admin to create, view, edit, and delete Majors.

#### 5.2 Flow of Events
##### 5.2.1 Main Flow
* 1. The Admin selects Manage Major.
* 2. The system displays a list of Majors, including Major Code and Major Name.
* 3. The Admin chooses Create, View, Edit, or Delete Major.
* 4. The system processes the selected action.

##### 5.2.2 Alternative Flows
* A1. Create Major: The Admin enters Major Code and Major Name. The system validates that the
Major Code is unique, creates the Major, and displays a success message.
* A2. Duplicate Major Code: If the entered Major Code already exists, the system rejects the creation
and displays an error message.
* A3. Edit Major: The Admin selects a Major, updates the allowed information, and the system
validates and saves the changes.
* A4. Delete Major: The Admin selects a Major to delete. The system checks whether the Major is
referenced by any Student or Curriculum. If not in use, the system requests confirmation and
deletes it upon confirmation.
* A5. Major In Use: If the Major is currently referenced by a Student or Curriculum, the system rejects
the deletion and displays an appropriate error message.

#### 5.3 Special Requirements

* Major Code must be unique.
* A Major may only be deleted if it is not referenced by any Student or Curriculum.
* Confirmation is required before deletion.

#### 5.4 Preconditions
* The Admin has successfully logged in.

#### 5.5 Postconditions
* Success: The Major is created, updated, or deleted accordingly.
* Failure: No Major data is changed.
#### 5.6 Extension Points
* None.

### 6. Use Case: Manage Curriculum
#### 6.1 Summary
* This use case allows the Admin to select a Major and manage the Courses belonging to that Major&#39;s
Curriculum, including setting the Recommended Semester for each Course.

#### 6.2 Flow of Events
##### 6.2.1 Main Flow
* 1. The Admin selects Manage Curriculum.
* 2. The Admin selects a Major.
* 3. The system displays Courses belonging to the selected Major&#39;s Curriculum, including Course Code,
Course Name, Credit, and Recommended Semester.
* 4. The Admin chooses Add Course to Curriculum or Remove Course from Curriculum, depending on
whether the Course is already included in the selected Major&#39;s Curriculum.
* 5. The system processes the selected action.

##### 6.2.2 Alternative Flows
* A1. Add Course to Curriculum: The Admin selects an existing Course and sets its Recommended
Semester. The system validates the information, adds the Course to the Curriculum, and displays a
success message.
* A2. Course Already in Curriculum: If the selected Course already exists in the Curriculum, the system
rejects the addition and displays an appropriate error message.
* A3. Remove Course from Curriculum: The Admin selects a Course to remove. The system requests
confirmation and removes the Course upon confirmation.

#### 6.3 Special Requirements
* A Course cannot be added to the same Major&#39;s Curriculum more than once.
* The Course must exist in the Course Catalog before it can be added to a Curriculum.
* Recommended Semester must be a valid value.
* Confirmation is required before removing a Course.

#### 6.4 Preconditions
* The Admin has successfully logged in.
* At least one Major exists in the system.

#### 6.5 Postconditions
* Success: The Curriculum is updated with the added or removed Course.
* Failure: The Curriculum remains unchanged.

#### 6.6 Extension Points
* None.

### 7. Use Case: Manage Course
#### 7.1 Summary
* This use case allows the Admin to create, view, search, edit, and delete Courses, and to set a
Prerequisite for a Course.

#### 7.2 Flow of Events
##### 7.2.1 Main Flow
* 1. The Admin selects Manage Course.
* 2. The system displays a list of Courses.
* 3. The Admin selects the appropriate action based on the intended task: View Course, Search
Course, Create Course, Edit Course, or Delete Course.
* 4. The system processes the selected action.

##### 7.2.2 Alternative Flows
* A1. Create Course: The Admin enters Course Code, Course Name, Credit, and an optional
Prerequisite. The system validates that the Course Code is unique, the Credit is valid, the
Prerequisite exists if specified, and the Course is not its own Prerequisite. The system creates the
Course and displays a success message.
* A2. Invalid Course Data: If the Course Code is not unique, the Credit is not valid, or the Prerequisite
is invalid, the system rejects the creation and displays an error message.
* A3. View / Search Course: The Admin searches by Course Code or Course Name, or selects a Course.
The system displays Course Code, Course Name, Credit, and Prerequisite.
* A4. Edit Course: The Admin selects a Course, updates the allowed information, and the system
validates and saves the changes.
* A5. Delete Course: The Admin selects a Course and chooses Delete. The system requests
confirmation and checks for existing integrity constraints or references before deleting.
* A6. Course In Use: If the Course is referenced by an existing Curriculum or Registration, the system
rejects the deletion and displays an appropriate error message.

#### 7.3 Special Requirements
* Course Code must be unique.
* A Course cannot be its own Prerequisite.
* Credit must be a positive valid number.
* Confirmation is required before deletion, and deletion must preserve data integrity.

#### 7.4 Preconditions
* The Admin has successfully logged in.

#### 7.5 Postconditions
* Success: The Course is created, updated, or deleted, or its Prerequisite is set accordingly.
* Failure: No Course data is changed.
#### 7.6 Extension Points
* Set Prerequisite.

### 8. Use Case: Manage Semester
#### 8.1 Summary
* This use case allows the Admin to create, view, edit, and delete academic Semesters.

#### 8.2 Flow of Events
##### 8.2.1 Main Flow
* 1. The Admin selects Manage Semester.
* 2. The system displays a list of Semesters.
* 3. The Admin chooses Create Semester, View Semester, Edit Semester, or Delete Semester.
* 4. The system processes the selected action.

##### 8.2.2 Alternative Flows
* A1. Create Semester: The Admin enters Semester Name, Start Date, and End Date. The system
validates that the Start Date is earlier than the End Date, the dates are valid, and the Semester does
not overlap with an existing Semester. The system creates the Semester and displays a success
message.
* A2. Invalid Semester Dates: If the Start Date is not earlier than the End Date, or the Semester
overlaps with an existing Semester, the system rejects the creation and displays an error message.
* A3. Edit Semester: The Admin selects a Semester, updates the allowed fields, and the system re-
validates the dates and saves the changes.
* A4. Delete Semester: The Admin selects a Semester and chooses Delete. The system requests
confirmation and checks whether deletion is permitted before deleting the Semester.
* A5. Semester In Use: If the Semester is referenced by Registration or academic data, the system
rejects the deletion and displays an appropriate error message.

#### 8.3 Special Requirements
* Start Date must be earlier than End Date.
* Semesters must not overlap.
* Confirmation is required before deletion.
* A Semester referenced by Registration or academic data shall not be deleted.

#### 8.4 Preconditions
* The Admin has successfully logged in.

#### 8.5 Postconditions
* Success: The Semester is created, updated, or deleted accordingly.
* Failure: No Semester data is changed.

#### 8.6 Extension Points
* None.

### 9. Use Case: Manage Registration Period
#### 9.1 Summary
* This use case allows the Admin to select a Semester and configure its Course Registration Period.
The Registration Period&#39;s status (Scheduled, Open, or Closed) is determined automatically by the
system based on the current date, without requiring the Admin to manually open or close it.

#### 9.2 Flow of Events
##### 9.2.1 Main Flow
* 1. The Admin selects Manage Registration Period.
* 2. The Admin selects a Semester.
* 3. The Admin enters the Registration Start Date and Registration End Date.
* 4. The Admin confirms the schedule.
* 5. The system validates the Registration Start and End dates.
* 6. The system saves the Registration Period.
* 7. The system automatically determines the Registration Status (Scheduled, Open, or Closed) based
on the current date.
* 8. The system displays the Registration Start Date/Time, Registration End Date/Time, and the
current Registration Status.

##### 9.2.2 Alternative Flows
* A1. Invalid Registration Period: If the Registration Start Date/Time is not earlier than the Registration
End Date/Time, or the Registration Period falls outside the selected Semester, the system rejects the
input and displays an error message.
* A2. Registration Period Already Configured: If a Registration Period has already been configured for
the selected Semester, the Admin may edit the existing Registration Period instead of creating a
new one.

#### 9.3 Special Requirements
* Registration Start Date/Time must be earlier than Registration End Date/Time.
* The Registration Period must fall within the selected Semester.
* The Registration Status shall be automatically determined by the system based on the current date
and the configured Start/End dates — the Admin does not manually open or close Registration.
* Each Semester shall have at most one Registration Period.
* The system shall remain responsive during peak course-registration periods.

#### 9.4 Preconditions
* The Admin has successfully logged in.
* At least one Semester exists.

#### 9.5 Postconditions
* Success: The Registration Period is configured for the selected Semester, and its status is
automatically reflected as Scheduled, Open, or Closed.
* Failure: The Registration Period remains unchanged.

#### 9.6 Extension Points
* None.

### 10. Use Case: Manage Registration Demand
#### 10.1 Summary
* This use case allows the Admin to select a Semester and a Major, view registration demand per
Course within that Major, view the Student registration list, search Courses, and generate a
Registration Demand Report.

#### 10.2 Flow of Events
##### 10.2.1 Main Flow
* 1. The Admin selects Manage Registration Demand.
* 2. The Admin selects a Semester.
* 3. The Admin selects a Major.
* 4. The system displays Registration Demand for Courses belonging to the selected Major, including
Course Code, Course Name, and Number of Registered Students.
* 5. The Admin may search for a Course, select a Course to view its Student Registration List, or
generate a Registration Demand Report.
* 6. The system processes the selected action.

##### 10.2.2 Alternative Flows
* A1. View Student Registration List: The Admin selects a Course. The system then displays the
registered Students, including Student ID, Student Name, Email, and Registration Status.
* A2. Search Course: The Admin enters Course Code or Course Name. The system filters and displays
matching Courses.
* A3. Generate Report: The Admin selects Generate Report. The system generates a report containing
Course Code, Course Name, Number of Registered Students, and Student Registration List.
* A4. No Registration Data: If no registration data exists for the selected Semester, the system displays
an appropriate message.

#### 10.3 Special Requirements
* Registration Demand data must remain consistent with the current registration records.
* Generated reports must accurately reflect the registration data.
* Requests shall be processed within 3 seconds under normal operating conditions.

#### 10.4 Preconditions
* The Admin has successfully logged in.
* At least one Semester exists.

#### 10.5 Postconditions
* Success: Registration demand information is displayed and, when requested, a report is generated.
* Failure: No Registration data is modified.

#### 10.6 Extension Points
* Generate Registration Demand Report.

### 11. Use Case: Assign Lecturer
#### 11.1 Summary
* This use case allows the Admin to select a Major and a Course, view Lecturers who are qualified to
teach that Course, and assign a qualified Lecturer to the Course.

#### 11.2 Flow of Events
##### 11.2.1 Main Flow
* 1. The Admin selects Assign Lecturer.
* 2. The Admin selects a Major.
* 3. The Admin selects a Course.
* 4. The system identifies Lecturers who are qualified to teach the selected Course.
* 5. The system displays the list of qualified Lecturers.
* 6. The Admin selects a qualified Lecturer.
* 7. The system validates the Lecturer&#39;s qualification.
* 8. The system assigns the Lecturer to the Course.
* 9. The system displays a success message.

##### 11.2.2 Alternative Flows
* A1. Lecturer Not Qualified: If the selected Lecturer does not have the required teaching
qualification, the system rejects the assignment and displays an error message.
* A2. No Qualified Lecturer Available: If no Lecturer is qualified to teach the selected Course, the
system displays an appropriate message.

#### 11.3 Special Requirements
* Only Lecturers who are qualified to teach the selected Course can be assigned.
* A Teaching Assignment shall reference an existing Lecturer and a valid Course.
* The system shall prevent invalid Lecturer-Course assignments.
* Requests shall be processed within 3 seconds under normal operating conditions.

#### 11.4 Preconditions
* The Admin has successfully logged in.
* At least one Course exists.

#### 11.5 Postconditions
* Success: The Teaching Assignment is saved and a success message is displayed.
* Failure: No Teaching Assignment is created.

#### 11.6 Extension Points
* None.

### 12. Use Case: Manage Teaching Course
#### 12.1 Summary
* This use case allows the Lecturer to select a Semester and view the Courses directly assigned to
them by the Admin. The Lecturer cannot self-select, request, or modify their teaching assignment.

#### 12.2 Flow of Events
##### 12.2.1 Main Flow
* 1. The Lecturer selects Manage Teaching Course.
* 2. The Lecturer selects a Semester.
* 3. The system retrieves Courses assigned to the Lecturer by the Admin for the selected Semester.
* 4. The system displays Course Code, Course Name, Credit, and Prerequisite.
* 5. The Lecturer selects an assigned Course.
* 6. The system displays the details of the selected Course.

##### 12.2.2 Alternative Flows
* A1. No Courses Assigned: If no Courses have been assigned to the Lecturer for the selected
Semester, the system displays an appropriate message.
* A2. Assignment Changed by Admin: When the Admin creates, changes, or removes a Teaching
Assignment, the system updates the Lecturer&#39;s teaching Course list accordingly.

#### 12.3 Special Requirements
* Teaching-course viewing shall respond within 3 seconds under normal operating conditions.
* Lecturers shall only access Courses assigned to them by the Admin.
* The Lecturer shall not independently select, register for, request, self-assign, or modify a Course
assignment.

#### 12.4 Preconditions
* The Lecturer has successfully logged in.
* A Semester is selected.

#### 12.5 Postconditions
* Success: The Lecturer can view the current list of Courses assigned by the Admin.
* Failure: No Teaching Assignment is modified by the Lecturer.

#### 12.6 Extension Points
* None.

### 13. Use Case: Manage Student Grades
#### 13.1 Summary
* This use case allows the Lecturer to select a Semester and a Course assigned to them, view Students
registered in that Course, view a Student&#39;s Prerequisite status, and enter or update the Student&#39;s
Grade.

#### 13.2 Flow of Events
##### 13.2.1 Main Flow
* 1. The Lecturer selects Manage Student Grades.
* 2. The Lecturer selects a Semester.
* 3. The system displays Courses assigned to the Lecturer by the Admin.
* 4. The Lecturer selects a Course assigned to them.
* 5. The system displays Course Code and Course Name.
* 6. The system displays Students registered in the selected Course, including Student ID, Student
Name, and Email.
* 7. The Lecturer selects a Student and views the Student&#39;s information.
* 8. The Lecturer enters or updates the Student&#39;s Grade.
* 9. The system validates the Grade, the Student&#39;s registration, and the Course assignment.
* 10. If validation succeeds, the system saves the Grade.
* 11. The system displays a success message.

##### 13.2.2 Alternative Flows
* A1. Invalid Grade: If the Grade is outside the valid grading range, the system rejects the Grade and
displays an error message.
* A2. Student Not Registered: If the Student is not registered in the selected Course, the system does
not allow the Grade to be saved.
* A3. Course Not Assigned to Lecturer: If the Course is not assigned to the Lecturer by the Admin, the
system rejects the Grade entry or update.
* A4. Course Taught by Another Lecturer: The system does not allow the Lecturer to enter or update
Grades for Students in a Course assigned to another Lecturer.
* A5. Save Failure: If the Grade cannot be saved, the system displays an error message and no invalid
or partial Grade data is stored.

#### 13.3 Special Requirements
* Grade entry and updating shall respond within 3 seconds under normal operating conditions.
* A Grade shall reference an existing Student and Course.
* Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
* Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
* The Lecturer may view the Student&#39;s Prerequisite status for the selected Course but shall not modify
it.
* Failed transactions shall not leave partial or invalid data.

#### 13.4 Preconditions
* The Lecturer has successfully logged in.
* The selected Semester exists.
* The selected Course is assigned to the Lecturer.
* The Student is registered in the selected Course.

#### 13.5 Postconditions
* Success: The valid Grade is stored or updated for the correct Student and Course.
* Failure: Existing Grade data remains valid and no invalid Grade is stored.

#### 13.6 Extension Points
*None. 

### 14. Use Case: View Courses
#### 14.1 Summary
* This use case allows the Student to view Courses belonging to their Major, search Courses by Course
Code or Course Name, and view detailed Course information.

#### 14.2 Flow of Events
##### 14.2.1 Main Flow
* 1. The Student selects View Courses.
* 2. The system identifies the Student&#39;s Major.
* 3. The system displays Courses belonging to the Student&#39;s Major.
* 4. The Student may search for a Course using Course Code or Course Name.
* 5. The Student selects a Course.
* 6. The system displays Course Code, Course Name, Credit, Prerequisite, and Recommended
Semester.
* 7. The Student views the Course information.

##### 14.2.2 Alternative Flows
* A1. Course Not Found: If no Course matches the entered Course Code or Course Name, the system
displays an appropriate message.

#### 14.3 Special Requirements
* Course, prerequisite, and recommended-semester information shall be presented clearly.
* Course viewing requests shall be processed within 3 seconds under normal operating conditions.

#### 14.4 Preconditions
* The Student has successfully logged in.
* The Student has an assigned Major.

#### 14.5 Postconditions
* Success: The requested Course information is displayed.
* Failure: No Course or Student data is modified.

#### 14.6 Extension Points
* None.

### 15. Use Case: Course Registration
#### 15.1 Summary
* This use case allows the Student to select and register for a Course. Before confirmation, the system
validates the Registration Period, Major/Curriculum eligibility, Prerequisite requirements, and
duplicate registration.

#### 15.2 Flow of Events
##### 15.2.1 Main Flow
* 1. The Student selects a Course to register.
* 2. The system checks whether the Registration Period is open.
* 3. The system checks whether the selected Course belongs to the Student&#39;s Major/Curriculum.
* 4. The system checks whether the required Prerequisite has been satisfied.
* 5. The system verifies that the Student does not already have an active registration for the same
Course.
* 6. If all checks pass, the system allows the student to confirm the registration.
* 7. The Student confirms the registration.
* 8. The system saves the registration.
* 9. The system displays a success message.

##### 15.2.2 Alternative Flows
* A1. Registration Period Not Open: If the Registration Period is not open, the system rejects the
registration and displays an appropriate error message.
* A2. Prerequisite Not Satisfied: If the Student has not satisfied the required Prerequisite, the system
rejects the registration and displays an appropriate error message.
* A3. Duplicate Registration: If the Student already has an active registration for the selected Course,
the system rejects the duplicate registration.
* A4. Student Does Not Confirm: If the Student does not confirm the registration, no Registration
record is created.

#### 15.3 Special Requirements
* Registration shall be processed within 3 seconds under normal operating conditions.
* The system shall prevent duplicate active registrations.
* Registration transactions shall be processed atomically.
* Simultaneous registration requests shall not result in lost transactions or inconsistent data.
* A Student shall only register for Courses belonging to the Student&#39;s assigned Major.

#### 15.4 Preconditions
* The Student has successfully logged in.
* The Student has selected an existing Course.
* The Student has successfully completed the required Prerequisite Course(s).

#### 15.5 Postconditions
* Success: A valid Registration record is saved and a success message is displayed.
* Failure: No invalid or partial Registration record is stored.

#### 15.6 Extension Points
* None.

### 16. Use Case: View Registration Status
#### 16.1 Summary
* This use case allows the Student to select a Semester and view registered Courses, Course
registration status, and Registration Period information.

#### 16.2 Flow of Events
##### 16.2.1 Main Flow
* 1. The Student selects View Registration Status.
* 2. The Student selects a Semester.
* 3. The system retrieves the Student&#39;s Course registration information.
* 4. The system displays Course Code, Course Name, Credit, and Registration Status.
* 5. The system displays Semester, Registration Start Date, Registration End Date, and Current
Registration Status.
* 6. The system displays the Course registration status as Registered or Dropped.

##### 16.2.2 Alternative Flows
* A1. No Registration Record: If the Student has no registration information for the selected Semester,
the system displays an appropriate message.

#### 16.3 Special Requirements
* Registration status shall be displayed clearly, including Registered and Dropped.
* Registration information must remain associated with the correct Student and Course.

#### 16.4 Preconditions
* The Student has successfully logged in.
* A Semester has been selected.

#### 16.5 Postconditions
* Success: The Student&#39;s Registration Status and Registration Period information are displayed.
* Failure: No Registration data is modified.

#### 16.6 Extension Points
* None.

### 17. Use Case: Drop Course
#### 17.1 Summary
* This use case allows the Student to select and drop a previously registered Course when the Drop
Period is still open.

#### 17.2 Flow of Events
##### 17.2.1 Main Flow
* 1. The Student selects Drop Course.
* 2. The system displays the Student&#39;s registered Courses.
* 3. The Student selects a registered Course.
* 4. The Student confirms dropping the Course.
* 5. The system verifies that the Course was registered by the Student.
* 6. The system verifies that the Drop Period is still open.
* 7. The system updates the Registration Status to Dropped, removing the Course from active
registration.
* 8. The system displays a success message.

##### 17.2.2 Alternative Flows
* A1. Course Not Registered: If the selected Course was not registered by the Student, the system
rejects the request and displays an appropriate error message.
* A2. Drop Period Closed: If the Drop Period is no longer open, the system rejects the request and
displays an appropriate error message.
* A3. Student Does Not Confirm: If the Student does not confirm the operation, the Course
registration remains unchanged.

#### 17.3 Special Requirements
* Course dropping shall be processed within 3 seconds under normal operating conditions.
* The system shall reliably process the operation and roll back incomplete changes if the transaction
fails.
* Registration data shall remain consistent after the Course is dropped.

#### 17.4 Preconditions
* The Student has successfully logged in.
* The Student has previously registered for the selected Course.

#### 17.5 Postconditions
* Success: The Registration Status is updated to Dropped, and the Course is no longer active.
* Failure: The existing Registration information remains unchanged.

#### 17.6 Extension Points
* None.

### 18. Use Case: View Grades
#### 18.1 Summary
* This use case allows the Student to select a Semester and view their own Grades and Result Status
for Courses.

#### 18.2 Flow of Events
##### 18.2.1 Main Flow
* 1. The Student selects View Grades.
* 2. The Student selects a Semester.
* 3. The system retrieves the Student&#39;s Grade information.
* 4. The system displays Course Code, Course Name, Credit, Grade, and Semester.
* 5. The system automatically uses the Grade to determine the Result Status.
* 6. The system displays the Result Status as Passed or Not Passed.
* 7. The Student views their Grade information.

##### 18.2.2 Alternative Flows
* A1. Grade Not Yet Entered: If a Grade has not yet been entered, the system displays an appropriate
message instead of presenting a completed Grade result.

#### 18.3 Special Requirements
* The Student shall only be able to view their own Grades.
* Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
* Grade viewing requests shall be processed within 3 seconds under normal operating conditions.
* Unauthorized access to another Student&#39;s Grades shall be rejected.

#### 18.4 Preconditions
* The Student has successfully logged in.

#### 18.5 Postconditions
* Success: The Student&#39;s Grade and Result Status information is displayed.
* Failure: No Grade data is modified.

#### 18.6 Extension Points
* None.

## V. Class Diagram
<img width="803" height="974" alt="Class_Diagram thyy" src="https://github.com/user-attachments/assets/69d23003-0669-41ad-abf0-35354460bd03" />

## VI. Data Model
