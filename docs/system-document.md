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
* The system shall allow the Admin to manage the Course Registration Period.
* The system shall allow the Admin to set:
  * Registration Start Date / Time
  * Registration End Date / Time
* The system shall allow the Admin to open Registration.
* The system shall allow the Admin to close Registration.
* The system shall allow the Admin to view Registration status.
* The system shall display:
  * Start Date / Time
  * End Date / Time
  * Current Status (Not Started, Open, Closed)
* The system shall validate that:
  * Registration Start Date / Time is earlier than Registration End Date / Time.
  * The Registration Period is within the Semester period.
  * Another Round 1 is not already active.

### 9. Manage Registration Demand (Admin)
* The system shall allow the Admin to select a Semester.
* The system shall allow the Admin to view Registration Demand.
* The system shall display:
  * Course Code
  * Course Name
  * Number of Registered Students
* The system shall allow the Admin to view the Student List for a Course.
  * The Student List shall display: Student ID, Student Name, Email, Registration Status (registered, unregistered).
* The system shall allow the Admin to search Courses by:
  * Course Code
  * Course Name
* The system shall allow the Admin to generate a Registration Demand Report.
  * The Registration Demand Report shall include: Course Code, Course Name, Number of Students, Registration List.

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
* The system shall allow the Lecturer to view the Courses directly assigned to them by the Admin for the selected Semester.
* The system shall display:
  * Course Code
  * Course Name
  * Credit
  * Prerequisite
* The system shall allow the Lecturer to view the details of each Course assigned by the Admin.
* The system shall **not** allow the Lecturer to select or register for a Course independently.
* The system shall **not** allow the Lecturer to request or assign themselves to a Course.
* The system shall **not** allow the Lecturer to modify the Course assignment made by the Admin.
* The system shall allow the Lecturer to view their teaching Courses according to the Admin's assignments.
* The system shall display an appropriate message if no Courses have been assigned to the Lecturer for the selected Semester.
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
*Level 0:

<img width="1132" height="542" alt="Untitled Diagram" src="https://github.com/user-attachments/assets/7564516e-08c7-4f20-bb80-57619e83c80d" />


*Level 1:
<img width="2479" height="2253" alt="qaqaqaq drawio" src="https://github.com/user-attachments/assets/bb9fac43-8e25-4ee3-bb5d-e87d02260270" />




## IV. Use case Diagram

## V. Class Diagram

## VI. Data Model
