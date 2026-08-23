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
- The system shall allow the Admin to view Courses.
- The system shall allow the Admin to search Courses by:
  - Course Code.
  - Course Name.
- The system shall allow the Admin to create a Course.
- When creating a Course, the system shall require:
  - Course Code.
  - Course Name.
  - Credit.
  - Prerequisite.
- The system shall allow the Admin to select a Course.
- The system shall allow the Admin to view Course information, including:
  - Course Code.
  - Course Name.
  - Credit.
  - Prerequisite.
- The system shall allow the Admin to edit Course information.
- The system shall allow the Admin to delete a Course.
- The system shall require confirmation before deleting a Course.
- The system shall allow the Admin to set a prerequisite for a Course.
- The system shall validate that:
  - The Course Code is unique.
  - The Credit is valid.
  - The prerequisite is an existing Course.
  - A Course cannot be its own prerequisite.

### 7. Manage Semester (Admin)
- The system shall allow the Admin to create a Semester.
- When creating a Semester, the system shall require:
- The system shall allow the Admin to set:
  - Semester Name.
  - Start Date.
  - End Date.
- The system shall allow the Admin to select a Semester.
- The system shall allow the Admin to view Semester information,
including:
  - Semester Name.
  - Start Date.
  - End Date.
  - Semester Status.
- The system shall allow the Admin to edit Semester information.
- The system shall allow the Admin to delete a Semester.
- The system shall require confirmation before deleting a Semester.
- The system shall validate that:
  - The Start Date is earlier than the End Date.
  - Semesters do not overlap.
  - Semester dates are valid.

### 8. Manage Registration Period (Admin)
- The system shall allow the Admin to select a Semester.
- The system shall allow the Admin to set the Registration Period by specifying:
  - Registration Period's name.
  - Start Date
  - End Date
- The system shall validate the entered Registration Period:
  - Start Date and End Date must not be empty.
  - Start Date must be earlier than End Date.
- The system shall automatically manage and update the Registration Status based on the current system date:
  - Upcoming: Current date is before Start Date.
  - Open: Current date is between Start Date and End Date.
  - Closed: Current date is after End Date.
- The system shall display the Registration Period information:
  - Registration Period's name.
  - Start Date.
  - End Date.
  - Current Registration Status (Upcoming, Open, Closed).

### 9. Manage Registration Demand (Admin)
- The system shall allow the Admin to select a Registration Period.
- The system shall display a list of Majors for the selected Registration Period.
- The system shall allow the Admin to select a Major to view its Course List.
- The Course List shall display:
  - Course Code.
  - Course Name.
  - Number of Registered Students.
- The system shall allow the Admin to generate a Registration Demand Report.
- The Registration Demand Report shall include:
- Course Code.
- Course Name.
- Number of Students.
- Registered student list.

### 10. Assign Lecturer (Admin)
- The system shall allow the Admin to select a Major.
- The system shall allow the Admin to select a Course.
- The system shall display Lecturers who are qualified to teach the selected Course.
- The system shall allow the Admin to view Lecturer qualifications.
- The system shall allow the Admin to select a qualified Lecturer.
- The system shall allow the Admin to assign the selected Lecturer to the Course.
- The system shall validate that:
  - The Lecturer is qualified to teach the Course.
- The system shall display a success message when the assignment is completed successfully.
- The system shall display an error message if the assignment cannot be completed.

### 11. Manage Teaching Course (Lecturer)
- The system shall allow the Lecturer to select a Semester.
- The system shall allow the Lecturer to view the Courses information directly assigned to them by the Admin for the selected Semester.
- The system shall display:
  - Course Code
  - Course Name
  - Credit
  - Prerequisite
- The system shall **not** allow the Lecturer to select or register for a Course independently.
- The system shall **not** allow the Lecturer to request or assign themselves to a Course.
- The system shall **not** allow the Lecturer to modify the Course assignment made by the Admin.
- The system shall allow the Lecturer to view their teaching Courses according to the Admin's assignments.
- The system shall update the Lecturer's teaching Course list when the Admin creates, changes, or removes a teaching assignment.
### 12. Manage Student Grades (Lecturer)

- The system shall allow the Lecturer to select a Semester.
- The system shall allow the Lecturer to view Courses assigned to them by the Admin.
- The system shall allow the Lecturer to select a Course.
- The system shall allow the Lecturer to view only Course taught by them.
- The system shall display:
  - Course Code.
  - Course Name.
- The system shall allow the Lecturer to view Students registered in the selected Course.
- The system shall display:
  - Student ID.
  - Student Name.
  - Email.
- The system shall allow the Lecturer to select a Student.
- The system shall allow the Lecturer to view Student information.
- The system shall allow the Lecturer to enter or update the Student's Grade.
- The Lecturer shall enter a Grade.
- The system shall validate the Grade.
- The system shall save the Grade if the validation is successful.
- The system shall display a success or error message after saving the Grade.
- The system shall ensure that:
  - The Student is registered in the selected Course.
  - The Course is assigned to the Lecturer by the Admin.
  - The Grade is within the valid grading range.
- The system shall not allow the Lecturer to enter or update Grades for Students in Course taught by another Lecturer.
- The system shall not allow the Lecturer to enter or update Grades for Courses that were not assigned to them by the Admin.

### 13. View Courses (Student)
- The system shall allow the Student to view Courses belonging to their Major.
- The system shall allow the Student to search for Courses by:
  - Course Code.
  - Course Name.
- The system shall allow the Student to select a Course to view detailed information.
- The system shall display:
  - Course Code.
  - Course Name.
  - Credit.
  - Prerequisite.
  - Recommended Semester.
### 14. Course Registration (Student)
- The system shall allow the Student to select a Course to register.
- The system shall validate the registration before allowing the Student to confirm.
- The system shall check that:
  - The Registration Period is open.
  - The Course belongs to the Student's Major / Curriculum.
  - The Prerequisite has been satisfied.
- If any validation fails, the system shall reject the registration and display an appropriate error message.
- If all validations pass, the system shall allow the Student to confirm the registration.
- After successful registration, the system shall:
  - Save the registration.
  - Display a success message.

### 15. View Registration Status (Student)
- The system shall allow the Student to select a Semester.
- The system shall allow the Student to view their registered Course.
- The system shall display:
  - Course Code.
  - Course Name.
  - Credit.
  - Registration Status.
- The system shall allow the Student to view the Registration Period.
- The system shall display:
  - Semester.
  - Registration Start Date.
  - Registration End Date.
  - Current Registration Status.
- The system shall display whether the Course registration was:
  - Registered.
  - Dropped.

### 16. Drop Course (Student)
- The system shall allow the Student to view registered Course.
- The system shall allow the Student to select a registered Course.
- The system shall display:
  - Course ID
  - Courses Name
- The system shall allow the Student to confirm dropping the Course.
- The system shall validate that:
  - The Course was registered by the Student.
  - The Drop Period is still open.
- If the validation is successful, the system shall:
  - Remove the Student's registration.
  - Update the Registration Status.
  - Display a success message.
- If the validation fails, the system shall display an appropriate error message.

### 17. View Grades (Student)
- The system shall allow the Student to select a Semester.
- The system shall allow the Student to view their Grades.
- The system shall display:
  - Course Code.
  - Course Name.
  - Credit.
  - Grade.
  - Semester.
  - Result Status (passed / not passed)
- The system shall automatically calculate grade to check result status.
- The system shall display an appropriate message when a Grade has not yet been entered.
- The Student shall only be able to view their own Grades.
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

### 1. General Interface

**Actors:** Administrator, Lecturer, Student.  
**Supported devices:** Desktop, Tablet, Mobile.

Administrator • Lecturer • Student

Desktop • Tablet • Mobile

### 1. Common Interfaces

#### 1.1. Login Screen

Actor: Administrator, Lecturer, Student.

Purpose: Authenticate the user and redirect them to the correct role-based dashboard.

#### Suggested layout

- Desktop: centered login card with system name/logo at the top and a simple background.
- Tablet: centered card with reduced width.
- Mobile: full-width login panel with safe side margins and large tap targets.

#### Main GUI components

- Course Registration System logo/title.
- Username input.
- Password input with show/hide icon.
- Login button.
- Error-message area below the fields.

#### User actions

- Enter username and password.
- Press Login.
- On success, redirect to the dashboard for the detected role.

#### Validation and system feedback

- Invalid username: show an error and keep focus near Username.
- Incorrect password: show an error without clearing Username.
- Inactive account: show a clear account-status message.
- After 5 consecutive failed attempts, show the temporary 15-minute blocking message.

#### Responsive behavior

- Desktop/tablet: card layout.
- Mobile: card becomes nearly full width; Login button becomes full width.

#### 1.2. Manage Account

Actor: Administrator, Lecturer, Student.

Purpose: Allow the logged-in user to view personal account information, change password, and log out.

#### Suggested layout

- Use a profile card at the top and a Change Password card below.
- Use read-only fields for personal information.
- Keep Logout visible in the top-right account menu or bottom of the page.

#### Main GUI components

- Username, Full Name, Email, Role.
- Student: Student ID and Major.
- Lecturer: Lecturer ID.
- Current Password and New Password fields.
- Change Password button.
- Logout button.

#### User actions

- View account information.
- Enter current password and new password.
- Submit Change Password.
- Log out.

#### Validation and system feedback

- Current password must be correct before password change.
- Display success after password update.
- Display error for invalid password input.
- Logout ends the current session.

#### Responsive behavior

- Desktop: profile and password sections may be placed side-by-side.
- Tablet/mobile: stack sections vertically.
- Mobile buttons become full width.

### 2. Administrator Interfaces

Administrator uses a persistent dashboard layout. On desktop, the left sidebar remains visible. On tablet it becomes collapsible, and on mobile it is hidden behind a hamburger menu.

#### 2.1. Administrator Dashboard

- Sidebar menu: Dashboard, Manage User, Manage Major, Manage Curriculum, Manage Course, Manage Semester, Manage Registration Period, Manage Registration Demand, Assign Lecturer, Manage Account, Logout.
- Topbar: page title, current account, logout shortcut.
- Main area may use simple navigation cards such as Users, Courses, Semesters, Registration Period, and Teaching Assignments.
- Dashboard cards are navigation aids only; they should not introduce new business logic.

#### 2.2. Manage User

Actor: Administrator.

Purpose: Create, view, search, edit, and deactivate Student and Lecturer accounts.

#### Suggested layout

- Page header with title and Create User button.
- Search and filter row below the title.
- Main data table in the center.
- Create/Edit form appears as a modal or side drawer.

#### Main GUI components

- Search box: ID, Name, or Major.
- User Type filter: Student / Lecturer.
- Table columns: ID, Full Name, Email, Role, Major/Qualification, Status, Actions.
- Create User button.
- Action buttons: View, Edit, Deactivate.
- Student form: Student ID, Full Name, Email, Major.
- Lecturer form: Lecturer ID, Full Name, Email, Teaching Qualifications.

#### User actions

- Search/filter users.
- Open Create User.
- View detail.
- Edit allowed information.
- Deactivate account after confirmation.

#### Validation and system feedback

- Duplicate Student/Lecturer ID: reject creation and show message.
- Invalid Email: highlight the Email field.
- Missing or invalid user information: prevent save.
- If deactivation is cancelled, keep the account active.

#### Responsive behavior

- Desktop: full table.
- Tablet: scroll horizontally if needed.
- Mobile: each user becomes a card with ID, Name, Role, Status and action menu.

#### 2.3. Manage Major

Actor: Administrator.

Purpose: Create, view, edit, and delete academic Majors.

#### Suggested layout

- Header with Create Major button.
- Compact table in the main content.
- Create/Edit form in modal.

#### Main GUI components

- Table columns: Major Code, Major Name, Actions.
- Form fields: Major Code, Major Name.
- Actions: View, Edit, Delete.

#### User actions

- Create a Major.
- View Major information.
- Edit Major information.
- Delete after confirmation.

#### Validation and system feedback

- Duplicate Major Code: reject creation.
- Missing or invalid Major information: prevent save.
- Major referenced by Students/Curriculum: reject deletion.
- Deletion cancelled: leave Major unchanged.

#### Responsive behavior

- Desktop/tablet: simple table.
- Mobile: Major cards with Edit/Delete action menu.

#### 2.4. Manage Curriculum

Actor: Administrator.

Purpose: Manage Courses belonging to a selected Major's Curriculum and set Recommended Semester.

#### Suggested layout

- Major selector at the top.
- Curriculum table below.
- Add Course button near table title.
- Remove action in each row.

#### Main GUI components

- Major dropdown.
- Table columns: Course Code, Course Name, Credit, Recommended Semester, Action.
- Add Course modal: Course dropdown and Recommended Semester input.
- Remove Course button.

#### User actions

- Select Major.
- View current Curriculum.
- Add a Course.
- Remove a Course.

#### Validation and system feedback

- Course already in Curriculum: do not add again.
- Invalid Recommended Semester: do not save.
- Removal cancelled: keep Curriculum unchanged.

#### Responsive behavior

- Desktop: standard table.
- Tablet: scroll table horizontally if necessary.
- Mobile: each Course is a card showing Code, Name, Credit and Recommended Semester.

#### 2.5. Manage Course

Actor: Administrator.

Purpose: Create, view, search, edit, delete Courses, and set Prerequisite.

#### Suggested layout

- Search bar at top.
- Create Course button.
- Course table.
- Create/Edit modal or side drawer.

#### Main GUI components

- Search by Course Code / Course Name.
- Table columns: Course Code, Course Name, Credit, Prerequisite, Actions.
- Form fields: Course Code, Course Name, Credit, Prerequisite.
- Actions: View, Edit, Delete, Set Prerequisite.

#### User actions

- Search and open a Course.
- Create new Course.
- Edit Course.
- Set/update Prerequisite.
- Delete after confirmation.

#### Validation and system feedback

- Duplicate Course Code: reject creation.
- Missing or invalid Course information: prevent save.
- Invalid Prerequisite or self-prerequisite: reject selection.
- Deletion cancelled: keep Course unchanged.

#### Responsive behavior

- Desktop: table + modal.
- Tablet: table can scroll horizontally.
- Mobile: card list; Edit/Delete/Prerequisite actions grouped in overflow menu.

#### 2.6. Manage Semester

Actor: Administrator.

Purpose: Create, view, edit, and delete academic Semesters.

#### Suggested layout

- Header with Create Semester button.
- Semester table.
- Date form in modal.

#### Main GUI components

- Table columns: Semester Name, Start Date, End Date, Status, Actions.
- Form fields: Semester Name, Start Date, End Date.
- Actions: View, Edit, Delete.

#### User actions

- Create Semester.
- View Semester.
- Edit dates/information.
- Delete after confirmation.

#### Validation and system feedback

- Start Date must be earlier than End Date.
- Overlapping Semester dates: reject operation.
- Semester in use: prevent deletion.
- Deletion cancelled: keep Semester unchanged.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: semester cards with date range and status.

#### 2.7. Manage Registration Period

Actor: Administrator.

Purpose: Configure the Registration Period for a selected Semester while the system automatically determines Scheduled/Open/Closed status.

#### Suggested layout

- Semester selector at top.
- Registration-period form below.
- Read-only status badge near the form title.

#### Main GUI components

- Semester dropdown.
- Registration Start Date/Time.
- Registration End Date/Time.
- Save Schedule button.
- Read-only Current Status badge: Scheduled, Open, Closed.

#### User actions

- Select Semester.
- Enter start and end date/time.
- Confirm/save schedule.
- View current status.

#### Validation and system feedback

- Start Date/Time must be earlier than End Date/Time.
- Registration Period must fall within the selected Semester.
- Status is never manually changed by Admin.

#### Responsive behavior

- Desktop: form can use two columns for Start/End fields.
- Tablet/mobile: stack all fields vertically.
- Status badge remains visible near the top.

#### 2.8. Manage Registration Demand

Actor: Administrator.

Purpose: View Course registration demand and the list of Students registered for a selected Course.

#### Suggested layout

- Registration Period selector and Major selector at top.
- Course demand table in upper section.
- Student registration list appears after selecting a Course.

#### Main GUI components

- Registration Period dropdown.
- Major dropdown.
- Course table: Course Code, Course Name, Number of Registered Students.
- Student table: Student ID, Student Name, Email, Registration Status.
- Generate Report button if retained by the group.

#### User actions

- Select Registration Period.
- Select Major.
- Select Course.
- View registered Students.
- Generate report if needed.

#### Validation and system feedback

- No Courses Found: display empty state.
- No Students Registered: display empty state in Student list.

#### Responsive behavior

- Desktop: Course and Student tables may be stacked vertically.
- Tablet: same stacked layout with scrollable tables.
- Mobile: Course cards first; tapping a card opens Student cards.

#### 2.9. Assign Lecturer

Actor: Administrator.

Purpose: Assign a qualified Lecturer to a Course.

#### Suggested layout

- Major selector and Course selector at top.
- Qualified Lecturer table below.
- Assign action on selected Lecturer.

#### Main GUI components

- Major dropdown.
- Course dropdown.
- Table: Lecturer ID, Lecturer Name, Qualification, Assignment Status, Action.
- Assign Lecturer button.

#### User actions

- Select Major.
- Select Course.
- Review qualified Lecturers.
- Select Lecturer.
- Assign Lecturer.

#### Validation and system feedback

- Only qualified Lecturers are displayed/selectable.
- If no qualified Lecturer is available, show an empty-state message.
- Invalid assignment must not be saved.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: lecturer cards with qualification and Assign button.

### 3. Lecturer Interfaces

Lecturer dashboard contains only teaching-related functions and account management.

#### 3.1. Lecturer Dashboard

- Sidebar: Dashboard, Manage Teaching Course, Manage Student Grades, Manage Account, Logout.
- Main area may show simple navigation cards for Assigned Courses and Student Grades.
- Lecturer cannot access Administrator functions.

#### 3.2. Manage Teaching Course

Actor: Lecturer.

Purpose: View Courses assigned by Administrator for a selected Semester.

#### Suggested layout

- Semester selector at top.
- Assigned Courses table below.
- Course details panel/modal opens when a Course is selected.

#### Main GUI components

- Semester dropdown.
- Table: Course Code, Course Name, Credit, Prerequisite, Action.
- View Details button.

#### User actions

- Select Semester.
- View assigned Courses.
- Select Course.
- View Course details.

#### Validation and system feedback

- No Courses Assigned: show empty state.
- Lecturer cannot add, remove, request, or modify Teaching Assignment.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: assigned Course cards with View Details.

#### 3.3. Manage Student Grades

Actor: Lecturer.

Purpose: Select an assigned Course, view registered Students, and enter or update Grade.

#### Suggested layout

- Semester dropdown at top.
- Assigned Course dropdown below.
- Student list table in the main area.
- Grade form appears in modal or right-side panel after selecting a Student.

#### Main GUI components

- Semester dropdown.
- Assigned Course dropdown.
- Student table: Student ID, Student Name, Email, Prerequisite Status, Grade, Action.
- Student detail area.
- Grade input.
- Save Grade button.
- Update Grade button.

#### User actions

- Select Semester.
- Select assigned Course.
- Select Student.
- View Student information and Prerequisite Status.
- Enter or update Grade.
- Save.

#### Validation and system feedback

- Invalid Grade: prevent save and show validation.
- Student not registered: prevent grade operation.
- Course not assigned to Lecturer: prevent access.
- Save failure: show error and keep existing Grade data unchanged.
- Prerequisite Status is read-only.

#### Responsive behavior

- Desktop: Student table + side grade panel works well.
- Tablet: grade panel may become modal.
- Mobile: Student list becomes cards; tapping a Student opens a full-screen/bottom-sheet Grade form.

### 4. Student Interfaces

Student dashboard focuses on course viewing, registration, registration status, dropping Courses, grades, and account management.

#### 4.1. Student Dashboard

- Sidebar: Dashboard, View Courses, Course Registration, View Registration Status, Drop Course, View Grades, Manage Account, Logout.
- Main area may use navigation cards such as Available Courses, Registration Status, and Grades.
- Student cannot access Lecturer or Administrator functions.

#### 4.2. View Courses

Actor: Student.

Purpose: View and search Courses belonging to the Student's Major and inspect Course information.

#### Suggested layout

- Student Major shown near the page title.
- Search bar below.
- Course table/list in main area.
- Course detail panel/modal after selection.

#### Main GUI components

- Major label.
- Search by Course Code or Course Name.
- Table: Course Code, Course Name, Credit, Prerequisite, Recommended Semester, Action.
- View Details button.

#### User actions

- Search Course.
- Select Course.
- View details.

#### Validation and system feedback

- Course Not Found: show empty-state message.
- Course data is read-only.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: Course cards with Code, Name, Credit, Prerequisite and Recommended Semester.

#### 4.3. Course Registration

Actor: Student.

Purpose: Register for an available Course during an open Registration Period.

#### Suggested layout

- Registration Period status banner at the top.
- Available Course list below.
- Recommended Course visually indicated but not mandatory.
- Confirmation modal before final registration.

#### Main GUI components

- Status banner: Open / Scheduled / Closed.
- Course list: Course Code, Course Name, Credit, Recommended, Prerequisite Status, Registration Status, Action.
- Register button.
- Confirm Registration modal.

#### User actions

- Select recommended Course or another available Course.
- Press Register.
- Review confirmation.
- Confirm registration.

#### Validation and system feedback

- Registration Period Not Open: disable Register and show message.
- Prerequisite Not Satisfied: block registration.
- Duplicate Registration: block registration.
- If Student does not confirm, do not create Registration.

#### Responsive behavior

- Desktop: full Course table.
- Tablet: scrollable table.
- Mobile: Course registration cards with a full-width Register button.

#### 4.4. View Registration Status

Actor: Student.

Purpose: View registered/dropped Courses and Registration Period information for a selected Semester.

#### Suggested layout

- Semester selector at top.
- Registration Period information card.
- Course registration table below.

#### Main GUI components

- Semester dropdown.
- Registration Period card: Start Date, End Date, Current Status.
- Table: Course Code, Course Name, Credit, Registration Status.

#### User actions

- Select Semester.
- View Registration Period.
- View Course registration statuses.

#### Validation and system feedback

- No Registration Record: show clear empty-state message.
- Statuses are read-only.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: Registration Period card followed by Course status cards.

#### 4.5. Drop Course

Actor: Student.

Purpose: Drop an actively registered Course when the Drop Period is open.

#### Suggested layout

- Drop Period status displayed at the top.
- Only actively registered Courses are shown.
- Confirmation dialog before final drop.

#### Main GUI components

- Drop Period badge.
- Table/card: Course Code, Course Name, Credit, Registration Status, Action.
- Drop Course button.
- Confirm Drop dialog.

#### User actions

- Select registered Course.
- Press Drop.
- Confirm operation.

#### Validation and system feedback

- Drop Period Closed: disable Drop and show message.
- If Student cancels confirmation, keep Registration unchanged.
- After success, show Dropped status.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: Course cards with clearly visible Drop button or disabled state.

#### 4.6. View Grades

Actor: Student.

Purpose: View Grade and Result Status for Courses in a selected Semester.

#### Suggested layout

- Semester selector at top.
- Grade table below.
- Result statuses shown with clear badges.

#### Main GUI components

- Semester dropdown.
- Table: Course Code, Course Name, Credit, Grade, Result Status.
- Status badge: Passed / Not Passed.
- Not Entered display for missing Grade.

#### User actions

- Select Semester.
- View Grade information.

#### Validation and system feedback

- Grade Not Yet Entered: show Not Entered or an appropriate message.
- Student can view only their own Grades.

#### Responsive behavior

- Desktop/tablet: table.
- Mobile: grade cards showing Course, Grade and Result Status.

### 5. Reusable Figma Components

- Sidebar with expanded/collapsed/mobile variants.
- Topbar.
- Primary, Secondary, Danger and Disabled Button variants.
- Text Input, Password Input, Date/Time Input.
- Dropdown / Select.
- Search Box.
- Data Table.
- Mobile Data Card.
- Status Badge.
- Form Card.
- Modal Dialog.
- Confirmation Dialog.
- Empty State.
- Loading State.
- Pagination.

### 6. Recommended Figma Page Structure

| Figma Page | Contents |
| --- | --- |
| 01 - Design System | Colors, typography, buttons, inputs, tables, status badges, modal components |
| 02 - Common | Login, Manage Account |
| 03 - Administrator | Admin Dashboard and all Admin screens |
| 04 - Lecturer | Lecturer Dashboard, Manage Teaching Course, Manage Student Grades |
| 05 - Student | Student Dashboard and all Student screens |
| 06 - Responsive Components | Desktop 1440, Tablet 768, Mobile 390 variants |

### 7. Screen Count and Prototype Strategy

The group does not need to draw every use case as a completely unique visual layout. Several functions share the same structure. Create a standard List + Table layout and a standard Create/Edit Form, then duplicate and adjust them. A practical complete prototype should contain approximately 12–15 main screens, with responsive Desktop, Tablet, and Mobile variants for the important screens.

### 8. Final GUI Navigation

- Login → system identifies role → corresponding Dashboard.
- Administrator → User / Major / Curriculum / Course / Semester / Registration Period / Registration Demand / Assign Lecturer.
- Lecturer → Manage Teaching Course / Manage Student Grades.
- Student → View Courses / Course Registration / View Registration Status / Drop Course / View Grades.
- All roles → Manage Account / Logout.

