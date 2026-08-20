# COURSE REGISTRATION SYSTEM SPECIFICATION

## I. Functional Requirements

### 1.Login (User Authentication)
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

### 2.Manage Account
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
  
### 3.Manage user
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

### 4.Manage Major
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

### 5.Manage Curriculum
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
  
### 6.Manage Courses (Admin)
This function allows the Admin to manage course catalog data and set up prerequisite constraints.
* The system shall allow the Admin to view and search Courses by Course Code or Course Name.
* The system shall allow the Admin to create a Course requiring Course Code, Course Name, Credit, and Prerequisite.
* The system shall allow the Admin to view Course details, edit Course information, delete a Course (requiring confirmation), and set prerequisite courses.
* The system shall validate constraints: Course Code is unique, Credit value is valid, Prerequisite is an existing Course, and a Course cannot be its own prerequisite.  

### 7.Manage Semester (Admin)
This function allows the Admin to create and manage academic semesters and their timeframes.
* The system shall allow the Admin to create a Semester by providing Semester Name, Start Date, and End Date.
* The system shall allow the Admin to select a Semester to view information (Semester Name, Start Date, End Date, Semester Status), edit information, or delete a Semester (requiring confirmation).
* The system shall validate that Start Date is earlier than End Date, Semesters do not overlap, and dates are valid.

### 8.Manage Registration Period (Admin)
This function allows the Admin to define, open, close, and monitor course registration timeframes for semesters.
* The system shall allow the Admin to select a Semester and manage the Course Registration Period.
* The system shall allow the Admin to set Registration Start Date/Time and Registration End Date/Time.
* The system shall allow the Admin to Open, Close, and view Registration Status (Not Started, Open, Closed).
* The system shall validate that Start Date/Time is earlier than End Date/Time, the period is within the Semester duration, and another Round 1 registration is not active.

### 9.Manage Registration Demand (Admin)
This function allows the Admin to monitor student course registration demands and generate registration summary reports.  
* The system shall allow the Admin to select a Semester and view Registration Demand (Course Code, Course Name, Number of Registered Students).
* The system shall allow the Admin to view the Student List for a Course (Student ID, Student Name, Email, Registration Status).
* The system shall allow the Admin to search Courses by Course Code or Course Name.
* The system shall allow the Admin to generate a Registration Demand Report containing Course Code, Course Name, Number of Students, and Registration List.

### 10.Assign Lecturer (Admin)
This function allows the Admin to assign qualified lecturers to teach specific offered courses.
* The system shall allow the Admin to select a Major, select a Course, and view Lecturers qualified to teach the selected Course.
* The system shall allow the Admin to view Lecturer qualifications, select a qualified Lecturer, and assign the selected Lecturer to the Course.
* The system shall validate that the Lecturer is qualified to teach the Course and display appropriate success/error messages.

### 11.View Lecturer Teaching Assignment
* The system shall allow the Admin to select a Major and Course.
* The system shall allow the Admin to view the Lecturers assigned to the selected Course.
* The system shall allow the Admin to select a Lecturer.
* The system shall allow the Admin to view the selected Lecturer's teaching assignments.
* The system shall display the Course Sections assigned to the Lecturer.
* The system shall display the Lecturer's teaching schedule.

#### 12.Manage Teaching Course (Lecturer)
This function allows Lecturers to view the list of courses officially assigned to them by the Admin for a specific semester.
* The system shall allow the Lecturer to select a Semester and view Courses directly assigned to them by the Admin (Course Code, Course Name, Credit, Prerequisite).  
* The system shall allow the Lecturer to view the details of each assigned Course.
* The system shall prevent Lecturers from independently registering, requesting, self-assigning, or modifying Course assignments.
* The system shall display an appropriate message if no Courses are assigned for the selected Semester and automatically update the teaching list when assignments change.

#### 13.Manage Student Grades (Lecturer)

#### 14.View Courses (Student)

#### 15.Course Registration (Student)

#### 16.View Registration Status (Student)

#### 17.Drop Course (Student)

#### 18.DView Grades (Student)

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

## IV. Use case Diagram

## V. Class Diagram

## VI. Data Model
