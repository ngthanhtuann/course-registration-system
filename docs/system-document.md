UNIVERSITY OF TRANSPORT HO CHI MINH CITY



Project Requirement Specification and Design Document
Course Registration System
   

Instructor: Trần Thị Mỹ Tiên











HCMC, 2026 8thGROUP 3
TABLE OF CONTENT
Function Requirement	7
Login (User Authentication)	7
Manage Account	7
Manage Users	7
Manage Major	7
Manage Curriculum	7
Manage Course	7
Manage Semester	8
Manage Registration Period	8
Manage Registration Demand	8
Assign Lecturer	8
Manage Teaching Course	8
Manage Student Grades	8
View Courses	9
Course Registration	9
View Registration Status	9
Drop Course	9
View Grades	9
Non-Functional Requirements	10
Product Requirements	10
1 Usability Requirements	10
2 Efficiency Requirements	10
3 Dependability Requirements	10
4 Security Requirements	11
Organizational Requirements	12
1 Operational Requirements	12
2 Development Requirements	12
Data Flow Diagram	12
Level 0	12
Level 1	13
Level 2	13
Use case Diagram	14
Overview Diagram	14
1 List of Actor	15
2 List of Use-cases	15
2. Use Case: Login	17
2.1 Summary	17
2.2 Flow of Events	17
2.2.1 main flow	17
2.2.2 alternative flows	18
2.3 Special Requirements	18
2.4 Preconditions	18
2.5 Postconditions	18
2.6 Extension Points	18
3. Use Case: Manage Account	18
3.1 Summary	18
3.2 Flow of Events	18
3.2.1 main flow	18
3.2.2 alternative flows	19
3.3 Special Requirements	19
3.4 Preconditions	19
3.5 Postconditions	19
3.6 Extension Points	19
4. Use Case: Manage User	19
4.1 Summary	19
4.2 Flow of Events	19
4.2.1 main flow	19
4.2.2 alternative flows	20
4.3 Special Requirements	20
4.4 Preconditions	20
4.5 Postconditions	20
4.6 Extension Points	20
5. Use Case: Manage Major	20
5.1 Summary	20
5.2 Flow of Events	20
5.2.1 main flow	20
5.2.2 alternative flows	20
5.3 Special Requirements	21
5.4 Preconditions	21
5.5 Postconditions	21
5.6 Extension Points	21
6. Use Case: Manage Curriculum	21
6.1 Summary	21
6.2 Flow of Events	21
6.2.1 Main Flow	21
6.2.2 Alternative Flows	21
6.3 Special Requirements	22
6.4 Preconditions	22
6.5 Postconditions	22
6.6 Extension Points	22
7. Use Case: Manage Course	22
7.1 Summary	22
7.2 Flow of Events	22
7.2.1 Main Flow	22
7.2.2 Alternative Flows	23
7.3 Special Requirements	23
7.4 Preconditions	23
7.5 Postconditions	23
7.6 Extension Points	23
8. Use Case: Manage Semester	23
8.1 Summary	23
8.2 Flow of Events	23
8.2.1 Main Flow	23
8.2.2 Alternative Flows	24
V. Class Diagram	38
VI. Data Model	38
VII. Interface Design Description	38
1. Common Interfaces	38
COURSE REGISTRATION SYSTEM SPECIFICATION
Function Requirement
Login (User Authentication)
The system shall allow Admin, Lecturer, and Student to log in using a valid username and password.
The system shall verify the username, password, and account status.
If the credentials are valid, the system shall grant access according to the user's role; otherwise, it shall display an appropriate error message.
After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.

Manage Account
The system shall allow Admin, Lecturer, and Student to view their account information, change their password, and log out.
The system shall validate the current password before saving a new password.

Manage Users
The system shall allow the Admin to view, search, create, edit, and deactivate Student and Lecturer accounts.
Student ID and Lecturer ID shall be unique, and email addresses shall be valid.
The Admin shall be able to set Lecturer teaching qualifications.
The system shall ensure that only one Admin account exists.

Manage Major
The system shall allow the Admin to view, create, edit, and delete Majors.
Major Code shall be unique.
The system shall prevent deletion of a Major that is still referenced by existing data.

Manage Curriculum
The system shall allow the Admin to select a Major and view the Courses in its Curriculum.
The Admin shall be able to add or remove Courses and set the Recommended Semester.
The system shall prevent the same Course from being added to the same Curriculum more than once.

Manage Course
The system shall allow the Admin to view, search, create, edit, and delete Courses.
Course information shall include Course Code, Course Name, Credit, Prerequisite, and Capacity. 
The system shall validate that Course Code is unique, Credit is valid, Capacity is a positive number, and a Course cannot be its own Prerequisite.

Manage Semester
The system shall allow the Admin to create, view, edit, and delete Semesters.
Semester information shall include Semester Name, Start Date, End Date, and Status.
The system shall validate that Start Date is earlier than End Date and that Semesters do not overlap.

Manage Registration Period
The system shall allow the Admin to select a Semester and configure a Registration Period with a name, Start Date, and End Date.
The system shall validate the dates and automatically update the Registration Status as Upcoming, Open, or Closed.
The system shall allow the Admin to configure a Drop Period, with a Start Date and End Date, for dropping registered Courses.  

Manage Registration Demand
The system shall allow the Admin to select a Registration Period and Major to view registration demand by Course.
The system shall display Course Code, Course Name, Number of Registered Students, and the registered Student list.
The system shall allow the Admin to generate a Registration Demand Report.

Assign Lecturer
The system shall allow the Admin to select a Major and Course and view Lecturers qualified to teach that Course.
The Admin shall be able to assign a qualified Lecturer to the Course.
The system shall reject assignments when the Lecturer is not qualified.

Manage Teaching Course
The system shall allow the Lecturer to select a Semester and view Courses assigned by the Admin.
The Lecturer shall not be allowed to self-select, request, or modify Course assignments.
The Lecturer's teaching Course list shall be updated when the Admin changes an assignment.

Manage Student Grades
The system shall allow the Lecturer to view Students registered in Courses assigned to them.
The system shall allow the Lecturer to view a Student's Prerequisite status for the Course, without allowing the Lecturer to modify it. 
The Lecturer shall be able to enter or update a Student's Grade.
The system shall validate the Grade and ensure that the Student is registered in the selected Course and the Course is assigned to that Lecturer.

View Courses
The system shall allow the Student to view and search Courses belonging to their Major.
The system shall exclude Courses the Student has already completed or is currently registered in from the displayed list. 
The system shall display Course Code, Course Name, Credit, Prerequisite, Recommended Semester, Capacity, and Available Seats.

Course Registration
The system shall allow the Student to select a Course to register.
The system shall validate that the Registration Period is Open, the Course belongs to the Student's Major/Curriculum, the Prerequisite is satisfied, the Student has not already completed the Course, and the Student is not already registered for the Course. 
The system shall check Course Capacity before registration. Registration shall be rejected when no seat is available.
If all validations pass, the system shall save the registration, decrease Available Seats by one, and display a success message.

View Registration Status
The system shall allow the Student to select a Semester and view registered Courses and Registration Period information.
The system shall display Course Code, Course Name, Credit, Registration Status, Registration Start Date, Registration End Date, and Current Registration Status.
Course registration status shall be shown as Registered or Dropped.

Drop Course
The system shall allow the Student to select and drop a previously registered Course while the Drop Period is open.
The system shall require confirmation and validate that the Course was registered by the Student.
After a successful drop, the system shall update the Registration Status to Dropped, increase Available Seats by one, and display a success message.

View Grades
The system shall allow the Student to select a Semester and view only their own Grades.
The system shall display Course Code, Course Name, Credit, Grade, Semester, and Result Status.
The system shall determine the Result Status as Passed or Not Passed and display an appropriate message when a Grade has not yet been entered.

Non-Functional Requirements
Product Requirements
1 Usability Requirements
Usability
The system shall provide a clear, consistent, and user-friendly interface for Students, Lecturers, and Administrators.
Course, prerequisite, recommended-semester, registration-status, and lecturer information shall be presented clearly.
Course registration status shall be displayed clearly, including Registered, Dropped, and Failed where applicable.
Lecturer-assignment status shall clearly indicate whether a course is Assigned or Unassigned.
Error messages and notifications shall clearly explain the reason for failed operations.

2 Efficiency Requirements
Performance
The system shall respond to common user requests such as login, course viewing, course registration, course dropping, teaching-course viewing, grade entry, grade updating, and grade viewing within 3 seconds under normal operating conditions.
The system shall remain responsive during peak course-registration periods.
Scalability
The system shall support an increasing number of students, lecturers, majors, courses, semesters, registration records, teaching assignments, and grade records.
The system architecture shall support future functional expansion without requiring a complete redesign of the core system.

3 Dependability Requirements
Availability
The system shall be available during normal academic operations and throughout active registration periods, except during scheduled maintenance.
Scheduled maintenance should be performed outside active registration periods whenever possible.
Reliability
The system shall ensure correct and reliable processing of course registration, course dropping, lecturer assignment, grade entry, and grade updates.
If a transaction fails, incomplete changes shall be rolled back so that no partial or invalid data remains.
The system shall prevent duplicate registration of the same course by the same student.
Data Integrity
The system shall maintain valid relationships among Major, Student, Course, Lecturer, Teaching Qualification, Registration, Teaching Assignment, and Grade data.
A student shall only register for courses belonging to the student's assigned major.
A registered course shall reference an existing course.
A lecturer assignment shall reference an existing lecturer and a valid course.
A teaching assignment shall reference a valid Course and Lecturer.
A Grade shall reference an existing Student and Course.
A Lecturer shall only enter or update Grades for Students registered in Courses assigned to that Lecturer.
A Student shall only view their own Grades.
Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
Deleting or updating records shall not create orphaned or inconsistent data.
Concurrency
The system shall correctly handle simultaneous registration requests from multiple students.
The system shall prevent duplicate registration records when multiple registration requests are processed concurrently.
The system shall keep course registration data consistent after concurrent operations.
Course registration transactions shall be processed atomically to prevent partial or duplicate registration records.
The system shall correctly process concurrent registration requests without lost transactions or data inconsistency.
Backup and Recovery
The system shall support scheduled backup of important user, course, registration, teaching-assignment, and grade data.
The system shall provide a recovery mechanism for restoring valid data after a critical failure.
The system shall support restoration of normal operation after an unexpected failure.
Recovered data shall not contain duplicate, partial, or inconsistent registration records.

4 Security Requirements
Authentication
The system shall require users to authenticate using a valid username and password before accessing protected functions.
User passwords shall not be stored as plain text and shall be protected using a secure password-storage mechanism.
After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.
The system shall allow authenticated users to change their password after verifying the current password.
Authorization
The system shall enforce role-based access control for Student, Lecturer, and Administrator accounts.
Students shall only access student functions such as viewing courses, registering courses, dropping registered courses, viewing registration status, and viewing their own grades.
Lecturers shall only access Courses assigned to them by an Administrator.
Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
Students shall only view their own Grades.
Administrators shall have authority to manage users, majors, courses, semesters, registration periods, registration information, teaching qualifications, and lecturer assignments.
Unauthorized access attempts shall be rejected by the system.
Organizational Requirements
1 Operational Requirements
Maintenance
The system shall be designed to support easy maintenance and updates.
Major functions such as user management, course management, semester management, registration, teaching assignment, and grade management should be separated into manageable modules.
Maintenance and software updates shall preserve existing user, academic, registration, teaching-assignment, and grade data.

2 Development Requirements
Design Constraints
The Course Registration System shall be implemented using Python and a relational database management system.
The system shall use PostgreSQL as the relational database management system.
The system shall use DBeaver to connect to and manage the PostgreSQL database.

Data Flow Diagram
Level 0

Level 1

Level 2
















Use case Diagram
Overview Diagram
1 List of Actor

2 List of Use-cases

2. Use Case: Login
2.1 Summary
This use case allows Admin, Lecturer, and Student to log in to the Course Registration System using valid account credentials and access functions according to their role.

2.2 Flow of Events
2.2.1 main flow
The user selects the Login function.
The system requests the username and password.
The user enters the username and password.
The system verifies whether the username exists.
The system verifies whether the password is correct.
The system verifies whether the account is active.
If all credentials are valid, the system authenticates the user and determines access permissions based on the role.
The system grants access to the functions available for that role.
2.2.2 alternative flows
A1. Invalid Username: If the username does not exist, the system displays an appropriate error message and requests reentry.
A2. Incorrect Password: If the password is incorrect, the system displays an appropriate error message and requests reentry.
A3. Inactive Account: If the account is not active, the system does not grant access.
A4. Too Many Failed Login Attempts: After 5 consecutive failed login attempts for the same account, the system temporarily blocks further login attempts for 15 minutes.

2.3 Special Requirements
The system shall respond to login requests within 3 seconds under normal operating conditions.
Passwords shall not be stored as plain text and shall use a secure password-storage mechanism.
The system shall enforce role-based access control.

2.4 Preconditions
The user has a valid account in the system.
The account is active.
The user is not currently logged in.

2.5 Postconditions
Success: The user is authenticated and granted access according to the assigned role.
Failure: Access is not granted and an appropriate error message is displayed.

2.6 Extension Points
None specified in the FR.

3. Use Case: Manage Account
3.1 Summary
This use case allows an authenticated Admin, Lecturer, or Student to view their account information, change their password, and log out. The displayed information varies by role.

3.2 Flow of Events
3.2.1 main flow
The user selects Manage Account.
The system displays the user's account information according to their role.
The user views their account information.
The user may choose Change Password or Log out.
The system processes the selected action. Account information displayed by role:
Admin: username, full name, email, and role.
Lecturer: lecturer ID, username, full name, email, and role.
Student: student ID, username, full name, email, major, and role.
3.2.2 alternative flows
A1. Duplicate ID: If the entered Student ID or Lecturer ID already exists, the system rejects the account creation and displays an appropriate error message.
A2. Invalid Email: If the entered Email format is invalid, the system rejects the input and displays an appropriate error message.
A3. Missing or Invalid User Information: If required user information is missing or invalid, the system does not save the information and displays an appropriate error message.
A4. Deactivation Cancelled: If the Admin does not confirm the deactivation, the system cancels the operation and the account remains active.

3.3 Special Requirements
The current password must be verified before changing the password.
Passwords shall be protected using a secure password-storage mechanism.

3.4 Preconditions
The user has successfully logged in.

3.5 Postconditions
If the password is changed successfully, the new password is stored securely.
Otherwise, account information remains unchanged.

3.6 Extension Points
Change Password.

Admin Use Cases
4. Use Case: Manage User
4.1 Summary
This use case allows the Admin to manage Student and Lecturer accounts by viewing, searching, creating, editing, and deactivating users.

4.2 Flow of Events
4.2.1 main flow
The Admin selects Manage User.
The system displays a list of Students and Lecturers.
The Admin chooses an action: View User, Search User, Create User Account, Edit User, or Deactivate User.
The system processes the selected action and displays the result.
4.2.2 alternative flows
A1. Duplicate Major Code: If the entered Major Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Invalid Major Information: If the Admin enters missing or invalid Major information, the system does not save it and displays an appropriate error message.
A3. Major Cannot Be Deleted: If the selected Major is still referenced by existing Students or Curriculum data, the system rejects the deletion and displays an appropriate message.
A4. Deletion Not Confirmed: If the Admin does not confirm the deletion, the Major remains unchanged.

4.3 Special Requirements
Student ID and Lecturer ID must be unique.
Email addresses must follow a valid format.
Confirmation is required before deactivating an account.
The system shall ensure that only one Admin account exists in the system.

4.4 Preconditions
The Admin has successfully logged in.

4.5 Postconditions
Success: Student or Lecturer accounts are created, updated, or deactivated according to the Admin's action.
Failure: No user data is changed.

4.6 Extension Points
None specified in the FR.

5. Use Case: Manage Major
5.1 Summary
This use case allows the Admin to create, view, edit, and delete Majors.

5.2 Flow of Events
5.2.1 main flow
The Admin selects Manage Major.
The system displays a list of Majors, including Major Code and Major Name.
The Admin chooses Create, View, Edit, or Delete Major.
The system processes the selected action.
5.2.2 alternative flows
A1. Course Already in Curriculum: If the selected Course already exists in the selected Major's Curriculum, the system does not add the Course and displays an appropriate message.
A2. Invalid Recommended Semester: If the entered Recommended Semester is invalid, the system does not save the change and displays an appropriate error message.
A3. Removal Not Confirmed: If the Admin does not confirm the removal, the system cancels the operation and the Curriculum remains unchanged.

5.3 Special Requirements
Major Code must be unique.
A Major may only be deleted if it is not referenced by any Student or Curriculum.
Confirmation is required before deletion.

5.4 Preconditions
The Admin has successfully logged in.

5.5 Postconditions
Success: The Major is created, updated, or deleted accordingly.
Failure: No Major data is changed.

5.6 Extension Points
None specified in the FR.

6. Use Case: Manage Curriculum
6.1 Summary
This use case allows the Admin to select a Major and manage the Courses belonging to that Major's Curriculum, including setting the Recommended Semester for each Course.

6.2 Flow of Events
6.2.1 Main Flow
The Admin selects Manage Curriculum.
The Admin selects a Major.
The system displays Courses belonging to the selected Major's Curriculum, including Course Code, Course Name, Credit, and Recommended Semester.
The Admin chooses Add Course to Curriculum or Remove Course from Curriculum, depending on whether the Course is already included in the selected Major's Curriculum.
The system processes the selected action.
6.2.2 Alternative Flows
A1. Duplicate Course Code: If the entered Course Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Missing Required Information: If the Admin does not provide all required Course information, the system does not save the Course and displays an appropriate message.
A3. Invalid Prerequisite Selection: If the Admin selects the Course itself as its Prerequisite, the system rejects the selection and requests the Admin to select another Course.
A4. Changes Not Confirmed: If the Admin does not confirm the changes, the system cancels the operation and keeps the existing Course information unchanged.

6.3 Special Requirements
A Course cannot be added to the same Major's Curriculum more than once.
The Course must exist in the Course Catalog before it can be added to a Curriculum.
Recommended Semester must be a valid value.
Confirmation is required before removing a Course.

6.4 Preconditions
The Admin has successfully logged in.
At least one Major exists in the system.

6.5 Postconditions
Success: The Curriculum is updated with the added or removed Course.
Failure: The Curriculum remains unchanged.

6.6 Extension Points
None specified in the FR.

7. Use Case: Manage Course
7.1 Summary
This use case allows the Admin to create, view, search, edit, and delete Courses, and to set a Prerequisite and Capacity for a Course.
7.2 Flow of Events
7.2.1 Main Flow
The Admin selects Manage Course.
The system displays a list of Courses.
The Admin selects the appropriate action based on the intended task:
View Course
Search Course
Create Course
Edit Course
Delete Course
Set Prerequisite
Set Capacity
If the Admin selects Create Course, the Admin enters the required Course information.
The system validates the entered Course information.
The Admin can set the Prerequisite and Capacity for the Course.
The system processes the selected action.
The system displays the result of the action.
7.2.2 Alternative Flows
A1. Duplicate Course Code: If the entered Course Code already exists, the system rejects the creation and displays an appropriate error message.
A2. Missing or Invalid Course Information: If required Course information is missing or invalid, the system rejects the input and displays an appropriate error message.
A3. Invalid Prerequisite: If the selected Prerequisite does not exist or the Course is selected as its own Prerequisite, the system rejects the selection and displays an appropriate error message.
A4. Invalid Course Capacity: If the entered Course Capacity is invalid, the system rejects the input and displays an appropriate error message.
A5. Deletion Not Confirmed: If the Admin does not confirm the deletion, the system does not delete the Course, and the Course remains unchanged.

7.3 Special Requirements
Course Code must be unique.
A Course cannot be its own Prerequisite.
Credit must be a positive valid number.
Course Capacity must be a valid positive number.
Confirmation is required before deleting a Course.
Course deletion must preserve data integrity.

7.4 Preconditions
The Admin has successfully logged in.

7.5 Postconditions
Success: The Course is created, updated, deleted, viewed, or searched successfully, or its Prerequisite or Capacity is set accordingly.
Failure: No Course data is changed when the selected action cannot be completed.

7.6 Extension Points
Set Prerequisite
Set Capacity

8. Use Case: Manage Semester
8.1 Summary
This use case allows the Admin to create, view, edit, and delete academic Semesters.
8.2 Flow of Events
8.2.1 Main Flow
The Admin selects Manage Semester.
The system displays a list of Semesters.
The Admin chooses Create Semester, View Semester, Edit Semester, or Delete Semester.
The system processes the selected action.
8.2.2 Alternative Flows
A1. Invalid Semester Dates: If the Start Date is not earlier than the End Date, the system rejects the operation and displays an appropriate error message.
A2. Semester Date Overlap: If the Semester dates overlap with an existing Semester, the system rejects the operation and displays an appropriate error message.
A3. Semester In Use: If the selected Semester is referenced by existing Registration or academic data, the system does not allow the Semester to be deleted and displays an appropriate message.
A4. Deletion Not Confirmed: If the Admin does not confirm the deletion, the system cancels the operation and the Semester remains unchanged.
8.3 Special Requirements
Start Date must be earlier than End Date.
Semesters must not overlap.
Confirmation is required before deletion.
A Semester referenced by Registration or academic data shall not be deleted.
8.4 Preconditions
The Admin has successfully logged in.
8.5 Postconditions
Success: The Semester is created, updated, or deleted accordingly.
Failure: No Semester data is changed.
8.6 Extension Points
None specified in the FR.
9. Use Case: Manage Registration Period
9.1 Summary
This use case allows the Admin to select a Semester its Course Registration Period. The Registration Period's status (Scheduled, Open, or Closed) is determined automatically by the system based on the current date, without requiring the Admin to manually open or close it.
9.2 Flow of Events
9.2.1 Main Flow
The Admin selects Manage Registration Period.
The Admin selects a Semester.
The Admin enters the Registration Start Date and Registration End Date.
The Admin confirms the schedule.
The system validates the Registration Start and End dates.
The system saves the Registration Period.
The system automatically determines the Registration Status (Scheduled, Open, or Closed) based on the current date.
The system displays the Registration Start Date/Time, Registration End Date/Time, and the current Registration Status.
9.2.2 Alternative Flows
A1. Invalid Registration Period: If the Registration Start Date/Time is not earlier than the Registration End Date/Time, the system rejects the input and displays an appropriate error message..
9.3 Special Requirements
Registration Start Date/Time must be earlier than Registration End Date/Time.
The Registration Period must fall within the selected Semester.
The Registration Status shall be automatically determined by the system based on the current date and the configured Start/End dates — the Admin does not manually open or close Registration.
Each Semester may have zero or more Registration Periods.
The system shall remain responsive during peak course-registration periods.
9.4 Preconditions
The Admin has successfully logged in. clicked on Semester
At least one Semester exists.
9.5 Postconditions
Success: The Registration Period is configured for the selected Semester, and its status is automatically reflected as Scheduled, Open, or Closed.
Failure: The Registration Period remains unchanged.
9.6 Extension Points
None specified in the FR.
10. Use Case: Manage Registration Demand
10.1 Summary
This use case allows the Admin to select a Semester and a Major, view registration demand per Course within that Major, view the Student registration list, search Courses, and generate a Registration Demand Report.
10.2 Flow of Events
10.2.1 Main Flow
The Admin selects Manage Registration Demand.
The Admin selects a Registration Period.
The Admin selects a Major.
The system displays the Courses belonging to the selected Major.
For each Course, the system displays the Number of Registered Students.
The Admin selects a Course.
The system displays the list of Students registered for the selected Course.
10.2.2 Alternative Flows
A1. No Courses Found: If no Courses are found for the selected Major, the system displays an appropriate message.
A2. No Students Registered: If no Students have registered for the selected Course during the selected Registration Period, the system displays an appropriate message.
10.3 Special Requirements
Registration Demand data must remain consistent with the current registration records.
Generated reports must accurately reflect the registration data.
Requests shall be processed within 3 seconds under normal operating conditions.
10.4 Preconditions
The Admin has successfully logged in.
At least one Semester exists.
10.5 Postconditions
Registration demand information is displayed and, when requested, a report is generated.
No Registration data is modified.
10.6 Extension Points
Generate Registration Demand Report.
11. Use Case: Assign Lecturer
11.1 Summary
This use case allows the Admin to select a Major and a Course, view Lecturers who are qualified to teach that Course, and assign a qualified Lecturer to the Course.
11.2 Flow of Events
11.2.1 Main Flow
The Admin selects Assign Lecturer.
The Admin selects a Major.
The Admin selects a Course.
The system identifies Lecturers who are qualified to teach the selected Course.
The system displays the list of qualified Lecturers.
The Admin selects a qualified Lecturer.
The system validates the Lecturer's qualification.
The system assigns the Lecturer to the Course.
The system displays a success message.
11.2.2 Alternative Flows
A1. No Assigned Courses: If no Courses are assigned to the Lecturer for the selected Semester, the system displays an appropriate message.
11.3 Special Requirements
Only Lecturers who are qualified to teach the selected Course can be assigned.
A Teaching Assignment shall reference an existing Lecturer and a valid Course.
The system shall prevent invalid Lecturer-Course assignments.
Requests shall be processed within 3 seconds under normal operating conditions.
11.4 Preconditions
The Admin has successfully logged in.
At least one Course exists.
11.5 Postconditions
Success: The Teaching Assignment is saved and a success message is displayed.
Failure: No Teaching Assignment is created.
11.6 Extension Points
None specified in the FR.
Lecturer Use Cases
12. Use Case: Manage Teaching Course
12.1 Summary
This use case allows the Lecturer to select a Semester and view the Courses directly assigned to them by the Admin. The Lecturer cannot self-select, request, or modify their teaching assignment.
12.2 Flow of Events
12.2.1 Main Flow
The Lecturer selects Manage Teaching Course.
The Lecturer selects a Semester.
The system retrieves Courses assigned to the Lecturer by the Admin for the selected Semester.
The system displays Course Code, Course Name, Credit, and Prerequisite.
The Lecturer selects an assigned Course.
The system displays the details of the selected Course.
12.2.2 Alternative Flows
A1. No Courses Assigned: If no Courses have been assigned to the Lecturer for the selected Semester, the system displays an appropriate message.
A2. Assignment Changed by Admin: When the Admin creates, changes, or removes a Teaching Assignment, the system updates the Lecturer's teaching Course list accordingly.
12.3 Special Requirements
Teaching-course viewing shall respond within 3 seconds under normal operating conditions.
Lecturers shall only access Courses assigned to them by the Admin.
The Lecturer shall not independently select, register for, request, self-assign, or modify a Course assignment.
12.4 Preconditions
The Lecturer has successfully logged in.
A Semester is selected.
12.5 Postconditions
The Lecturer can view the current list of Courses assigned by the Admin.
No Teaching Assignment is modified by the Lecturer.
Display the list of subjects analyzed by the administrator.
12.6 Extension Points
None specified in the FR.
13. Use Case: Manage Student Grades
13.1 Summary
This use case allows the Lecturer to select a Semester and a Course assigned to them, view Students registered in that Course, view a Student's Prerequisite status, and enter or update the Student's Grade.
13.2 Flow of Events
13.2.1 Main Flow
The Lecturer selects Manage Student Grades.
The Lecturer selects a Semester.
The system checks that the Registration Period for the selected Semester has ended.
The system displays the Courses assigned to the Lecturer by the Admin for the selected Semester.
The Lecturer selects an assigned Course.
The system displays the Students registered in the selected Course, including Student ID, Student Name, and Email.
The Lecturer selects a Student to view the Student's information.
The Lecturer enters or updates the Student's Grade.
The system validates the Grade, the Student's Registration, and the Lecturer's Course assignment.
If the validation succeeds, the system saves the Grade.
The system displays a success message.
13.2.2 Alternative Flows
A1. Invalid Grade: If the entered Grade is invalid, the system does not save the Grade and displays an appropriate error message.
A2. Student Not Registered: If the Student is not registered in the selected Course, the system does not allow the Lecturer to enter or update the Grade and displays an appropriate message.
A3. Course Not Assigned: If the selected Course is not assigned to the Lecturer, the system does not allow the Lecturer to manage Grades for that Course and displays an appropriate message.
A4. Grade Save Failed: If the Grade cannot be saved, the system displays an appropriate error message and the existing Grade data remains unchanged.
13.3 Special Requirements
Grade entry and updating shall respond within 3 seconds under normal operating conditions.
A Grade shall reference an existing Student and Course.
Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
Lecturers shall only view Students and enter or update Grades for Courses assigned to them.
The Lecturer may view the Student's Prerequisite status for the selected Course but shall not modify it. Failed transactions shall not leave partial or invalid data.
13.4 Preconditions
The Lecturer has successfully logged in.
The selected Semester exists.
The selected Course is assigned to the Lecturer.
The Student is registered in the selected Course.
13.5 Postconditions
Success: The valid Grade is stored or updated for the correct Student and Course.
Failure: Existing Grade data remains valid and no invalid Grade is stored.
13.6 Extension Points
None specified in the FR.
Student Use Cases
14. Use Case: View Courses
14.1 Summary
This use case allows the Student to view Courses belonging to their Major, search Courses by Course Code or Course Name, and view detailed Course information.
14.2 Flow of Events
14.2.1 Main Flow
The Student selects View Courses.
The system identifies the Student's Major.
The system displays Courses belonging to the Student's Major.
The Student may search for a Course using Course Code or Course Name.
The Student selects a Course.
The system displays Course Code, Course Name, Credit, Prerequisite, and Recommended Semester.
The Student views the Course information.
14.2.2 Alternative Flows
A1. Course Not Found: If no Course matches the entered Course Code or Course Name, the system displays an appropriate message.
14.3 Special Requirements
Course, prerequisite, and recommended-semester information shall be presented clearly.
Course viewing requests shall be processed within 3 seconds under normal operating conditions.
14.4 Preconditions
The Student has successfully logged in.
The student's major is already in the system.
14.5 Postconditions
The requested Course information is displayed.
No Course or Student data is modified.
14.6 Extension Points
None specified in the FR.



15. Use Case: Course Registration
15.1 Summary
This use case allows the Student to select and register for an available Course belonging to the Student's Major/Curriculum. Before confirmation, the system validates the Registration Period, Student eligibility, Prerequisite requirements, duplicate registration, and Course Capacity.
15.2 Flow of Events
15.2.1 Main Flow
The Student selects a Course to register from the available Courses.
The system checks whether the Registration Period is open.
The system checks whether the Student is eligible to register for the selected Course.
The system checks whether the Student has satisfied the required Prerequisite.
The system verifies that the Student does not already have an active Registration for the same Course.
The system checks whether the Course Capacity has been reached.
If all checks pass, the system allows the Student to confirm the registration.
The Student confirms the registration.
The system saves the Registration.
The system displays a success message.
15.2.2 Alternative Flows
A1. Registration Period Not Open: If the Registration Period is not open, the system rejects the registration and displays an appropriate error message.
A2. Student Not Eligible: If the Student is not eligible to register for the selected Course, the system rejects the registration and displays an appropriate error message.
A3. Prerequisite Not Satisfied: If the Student has not satisfied the required Prerequisite, the system rejects the registration and displays an appropriate error message.
A4. Duplicate Registration: If the Student already has an active Registration for the selected Course, the system rejects the registration and displays an appropriate error message.
A5. Course Capacity Reached: If the Course Capacity has been reached, the system rejects the registration and displays an appropriate error message.
A6. Student Does Not Confirm: If the Student does not confirm the registration, no Registration record is created.
15.3 Special Requirements
Registration shall be processed within 3 seconds under normal operating conditions.
The system shall prevent duplicate active Registrations.
Registration transactions shall be processed atomically.
Simultaneous registration requests shall not result in lost transactions or inconsistent data.
A Student shall only register for Courses belonging to the Student's assigned Major/Curriculum.
The system shall prevent registration when the Course Capacity has been reached.
15.4 Preconditions
The Student has successfully logged in.
The Student has selected an available Course to register.
15.5 Postconditions
Success: A valid Registration record is saved, and the Course's registration information is updated accordingly. A success message is displayed.
Failure: No invalid or partial Registration record is stored, and the Course's registration information remains unchanged.
15.6 Extension Points
Check Eligibility
Check Prerequisite
Check Duplicate Registration
Check Course Capacity



16. Use Case: View Registration Status
16.1 Summary
This use case allows the Student to select a Semester and view registered Courses, Course registration status, and Registration Period information.
16.2 Flow of Events
16.2.1 Main Flow
The Student selects View Registration Status.
The Student selects a Semester.
The system retrieves the Student's Course registration information.
The system displays Course Code, Course Name, Credit, and Registration Status.
The system displays Semester, Registration Start Date, Registration End Date, and Current Registration Status.
The system displays the Course registration status as Registered or Dropped.
16.2.2 Alternative Flows
A1. No Registration Record: If the Student has no registration information for the selected Semester, the system displays an appropriate message.
16.3 Special Requirements
Registration status shall be displayed clearly, including Registered and Dropped.
Registration information must remain associated with the correct Student and Course.
16.4 Preconditions
The Student has successfully logged in.
A Semester has been selected.
16.5 Postconditions
The Student's Registration Status and Registration Period information are displayed.
No Registration data is modified.
16.6 Extension Points
None specified in the FR.
17. Use Case: Drop Course
17.1 Summary
This use case allows the Student to select and drop a previously registered Course when the Drop Period is still open.
17.2 Flow of Events
17.2.1 Main Flow
The Student selects Drop Course.
The system displays the Student's actively registered Courses.
The Student selects a Course to drop.
The system verifies that the Drop Period is still open.
If the Drop Period is open, the system asks the Student to confirm the drop.
The Student confirms dropping the Course.
The system updates the Registration Status to Dropped.
The system displays a success message.
17.2.2 Alternative Flows
A1. Drop Period Closed: If the Drop Period is no longer open, the system rejects the drop request and displays an appropriate error message.
A2. Student Does Not Confirm: If the Student does not confirm the drop, the system cancels the operation and the Registration remains unchanged.
17.3 Special Requirements
Course dropping shall be processed within 3 seconds under normal operating conditions.
The system shall reliably process the operation and roll back incomplete changes if the transaction fails.
Registration data shall remain consistent after the Course is dropped.
17.4 Preconditions
The Student has successfully logged in.
The Student has previously registered for the selected Course.
17.5 Postconditions
Success: The Registration Status is updated to Dropped, and the Course is no longer active.
Failure: The existing Registration information remains unchanged.
17.6 Extension Points
None specified in the FR.
18. Use Case: View Grades
18.1 Summary
This use case allows the Student to select a Semester and view their own Grades and Result Status for Courses.
18.2 Flow of Events
18.2.1 Main Flow
The Student selects View Grades.
The Student selects a Semester.
The system retrieves the Student's Grade information.
The system displays Course Code, Course Name, Credit, Grade, and Semester.
The system automatically uses the Grade to determine the Result Status.
The system displays the Result Status as Passed or Not Passed.
The Student views their Grade information.
18.2.2 Alternative Flows
A1. Grade Not Yet Entered: If a Grade has not yet been entered, the system displays an appropriate message instead of presenting a completed Grade result.
18.3 Special Requirements
The Student shall only be able to view their own Grades.
Grade data shall remain associated with the correct Student, Course, Lecturer, and Semester.
Grade viewing requests shall be processed within 3 seconds under normal operating conditions.
Unauthorized access to another Student's Grades shall be rejected.
18.4 Preconditions
The Student has successfully logged in.
18.5 Postconditions
The Student's Grade and Result Status information is displayed.
No Grade data is modified.
18.6 Extension Points
None specified in the FR.
V. Class Diagram

VI. Data Model

VII. Interface Design Description
1. Common Interfaces
