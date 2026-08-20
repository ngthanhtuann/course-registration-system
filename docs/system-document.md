# COURSE REGISTRATION SYSTEM SPECIFICATION

## I. Functional Requirements

### Login (User Authentication)
* The system shall allow Admin, Lecturer, and Student to log in using valid account credentials.
* The system shall require users to enter their credentials before accessing system functions.
* The system shall verify the correctness of the entered credentials.
* If the credentials are valid, the system shall grant access according to the user's role.
* If the credentials are invalid, the system shall display an error message and request re-entry.

### Manage Account
* The system shall allow Admin, Lecturer, and Student to view account information.
* The system shall display the following account information according to the user's role:
  * Admin: username and role.
  * Lecturer: username and role.
  * Student: username, role, and major.
* The system shall allow Admin, Lecturer, and Student to change their password
  * The user shall enter the current password.
  * The user shall enter the new password.
  * The user shall confirm the new password.
* The system shall validate the entered password information.
* The system shall display a success or error message after the password change.
* The system shall allow Admin, Lecturer, and Student to log out of the system.

### Manage User
* The system shall allow the Admin to manage Student and Lecturer information.
* For Students, the system shall allow the Admin to:
  * Create a Student.
  * Edit Student information.
  * Delete a Student.
  * Assign a Major to a Student.
* For Lecturer, the system shall allow the Admin to:
  * Create a Lecturer.
  * Edit Lecturer information.
  * Delete a Lecturer.
  * Set teaching qualifications for a Lecturer.
* The system shall ensure that only one Admin account exists in the system.

### Manage Courses
This function allows the Admin to manage course catalog data and set up prerequisite constraints.
* The system shall allow the Admin to view and search Courses by Course Code or Course Name.
* The system shall allow the Admin to create a Course requiring Course Code, Course Name, Credit, and Prerequisite.
* The system shall allow the Admin to view Course details, edit Course information, delete a Course (requiring confirmation), and set prerequisite courses.
* The system shall validate constraints: Course Code is unique, Credit value is valid, Prerequisite is an existing Course, and a Course cannot be its own prerequisite.  

### Manage Semester
* The system shall allow the Admin to create a Semester.
* The system shall require the Admin to provide:
  * Semester name.
  * Start Date.
  * End Date.
  * Registration Period.
* The system shall allow the Admin to view Semester information.
* The system shall allow the Admin to edit Semester information.
* The system shall allow the Admin to delete a Semester.
* The system shall validate that:
  * The Start Date is earlier than the End Date.
  * The Registration Start Date is earlier than the Registration End Date.
  * The Registration Period is within the Semester period.
  * Semesters do not overlap.

### Manage Registration
* The system shall allow the Admin to select a Major.
* The system shall allow the Admin to view the Courses belonging to the selected Major.
* The system shall allow the Admin to select a Course.
* The system shall allow the Admin to view the Course Sections of the selected Course.
* The system shall allow the Admin to select a Course Section.
* The system shall allow the Admin to view enrollment information of the selected Course Section.
* The system shall display:
  * Section Capacity.
  * Number of Registered Students.
  * Available Seats.
* The system shall allow the Admin to view the registered Students, including their Student ID and Name.
* The system shall allow the Admin to view the registration status of the Course Section, including Registered and Dropped.

### Manage Course Section
* The system shall allow the Admin to select a Course and view its Course Sections.
* The system shall allow the Admin to add a Course Section.
* The system shall allow the Admin to set:
  * Section Capacity.
  * Section Schedule.
  * Section Room.
* The system shall allow the Admin to view Course Section information.
* The system shall allow the Admin to edit Course Section information.
* The system shall allow the Admin to delete a Course Section.
* The system shall ensure that the Course Section capacity is greater than zero.

### Assign Lecturer
* The system shall allow the Admin to select a Major and Course.
* The system shall filter and display Lecturers who are qualified to teach the selected Course.
* The system shall allow the Admin to view qualified Lecturers.
* The system shall allow the Admin to select one or more qualified Lecturers.
* The system shall allow the Admin to assign the selected Lecturers to the Course.
* The system shall display a success message when the assignment is completed successfully.
* The system shall display an error message if the assignment cannot be completed.

### View Lecturer Teaching Assignment
* The system shall allow the Admin to select a Major and Course.
* The system shall allow the Admin to view the Lecturers assigned to the selected Course.
* The system shall allow the Admin to select a Lecturer.
* The system shall allow the Admin to view the selected Lecturer's teaching assignments.
* The system shall display the Course Sections assigned to the Lecturer.
* The system shall display the Lecturer's teaching schedule.

---

### Lecturer

#### Manage Teaching Course Selection
* The system shall allow lecturers to select a semester before viewing and selecting teaching courses.
* The system shall allow lecturers to view the list of courses assigned to them by the Administrator for the selected semester.
* The system shall display relevant course information, including course code, course name, and assignment status.
* The system shall allow lecturers to search for courses from their assigned course list by course code or course name.
* The system shall allow lecturers to select a course only from the courses assigned to them by the Administrator.
* The system shall not allow lecturers to select courses that have not been assigned to them by the Administrator.
* The system shall display the selected course information before the lecturer confirms the teaching course selection.
* The system shall allow lecturers to confirm their teaching course selection.
* The system shall validate that the lecturer is authorized to teach the selected course in the selected semester before storing the course selection.
* The system shall prevent a lecturer from selecting the same course more than once within the same semester.
* If the course selection is valid, the system shall store the lecturer's selection and display a success message.
* If the course selection is invalid, the system shall reject the selection and display an appropriate error message.
* After confirmation, the system shall display the list of teaching courses selected by the lecturer for the selected semester.
* Multiple lecturers may be assigned to and may select the same course, provided that each lecturer has been authorized for that course by the Administrator.
* The system shall display an appropriate message if no courses have been assigned to the lecturer for the selected semester.

#### Select Course Section
After a lecturer has selected teaching courses as described in Section 2, the following requirements apply to selecting a specific course section within those courses.

* The system shall allow lecturers to select a semester before viewing available course sections.
* The system shall allow lecturers to view course sections belonging only to courses they have selected and that were assigned to them by the Administrator.
* The system shall display relevant course section information, including course, course section, schedule, room, capacity where applicable, and assignment status.
* The system shall display the assignment status of each course section as Available or Assigned.
* A course section with Available status shall be selectable by a lecturer.
* A course section with Assigned status shall not be selectable because another lecturer has already been assigned to that section.
* The system shall allow a lecturer to select an available course section.
* The system shall display the selected course section information before the lecturer confirms the selection.
* The system shall validate that the lecturer is eligible to select the section before assigning the course section.
* The system shall validate that the selected course section belongs to a course selected by the lecturer.
* The system shall validate that the selected course section has not already been assigned to another lecturer.
* The system shall check whether the selected course section conflicts with the lecturer's existing teaching schedule and shall prevent the lecturer from selecting two or more course sections with overlapping teaching schedules.
* If a schedule conflict exists, the system shall reject the selection and display an appropriate error message indicating the conflicting teaching assignment.
* If the course section selection is valid, the system shall assign the lecturer to the selected course section.
* After successful assignment, the system shall update the course section status from Available to Assigned.
* After successful assignment, the system shall display a confirmation message and update the lecturer's selected course section list.
* Each course section shall have at most one lecturer assigned at a time.
* A lecturer may be assigned to multiple course sections as long as the sections do not have conflicting schedules and all other assignment conditions are satisfied.
* If the selected course section has already been assigned to another lecturer between the time it was displayed and the time the lecturer confirms the selection, the system shall reject the selection.
* In this situation, the system shall notify the lecturer that the course section is no longer available and shall refresh the course section status.
* If the lecturer is not eligible to select the course section, the system shall reject the selection and display an appropriate error message.
* The system shall allow lecturers to withdraw from a previously selected course section only when withdrawal is permitted by the system's course section selection period or applicable semester rules.
* The system shall verify that the selected course section belongs to the logged-in lecturer before processing the withdrawal.
* If the withdrawal is valid, the system shall remove the lecturer from the course section and update the section status from Assigned to Available.
* After a successful withdrawal, the system shall update the lecturer's teaching course section list and display a success message.
* If withdrawal is not permitted, the system shall reject the request and display an appropriate error message.
* The system shall display an appropriate message if no course sections are available for the lecturer's selected course.

#### View Teaching Schedule
* The system shall allow lecturers to view their teaching schedule by semester.
* The system shall allow lecturers to select a semester before viewing the teaching schedule.
* The system shall display only teaching assignments belonging to the logged-in lecturer.
* The teaching schedule shall display relevant information for each teaching assignment, including course code, course name, course section, teaching day, teaching time, and room.
* The system shall allow lecturers to filter the teaching schedule by day.
* When a day is selected, the system shall display only teaching assignments scheduled for that day.
* The teaching schedule shall reflect the lecturer's current course section assignments.
* If a lecturer successfully selects a new course section, the system shall update the lecturer's teaching schedule accordingly.
* If a lecturer successfully withdraws from a course section, the system shall remove that course section from the lecturer's teaching schedule.
* The system shall prevent lecturers from viewing teaching schedules belonging to other lecturers.
* If no teaching assignment exists for the selected semester, the system shall display an appropriate message indicating that no teaching schedule is available.
* If no teaching assignment exists for the selected day, the system shall display an appropriate message indicating that no teaching schedule is available for that day.

---

### Student

#### View Courses
* The system shall allow the Student to view Courses belonging to their Major. 
* The system shall allow the Student to search for a Course.
* The system shall allow the Student to select a Course to view detailed information.
* The system shall display the Course Code, Course Name, Major, Credits, and Prerequisite.

#### View Course Sections
* The system shall allow the Student to select a Course and view its Course Sections.
* The system shall allow the Student to search or filter Sections.
* The system shall allow the Student to select a Course Section to view Section information.
* The system shall display the Section Code, Lecturer, Capacity, Available Seats, Schedule, Room, and Section Status.
* The system shall specify if the Section Status is Available (can register), Full (cannot register), or Not Available (due to no instructor or registration not being open).

#### Register Course Section
* The system shall allow the Student to select a Course Section to attempt registration.
* The system shall reject registration if the registration period is not open or is closed.
* The system shall hide registration if the Course belongs to a different major.
* The system shall check the prerequisite against the Student's academic record, rejecting registration if it is not passed.
* The system shall check the Section capacity, rejecting registration if the section is full.
* The system shall check for Instructor assignment, rejecting registration if no instructor is assigned.
* The system shall check for duplicate registrations, rejecting if the student is already registered for the section.
* The system shall check for schedule conflicts, rejecting registration if a conflict exists.
* The system shall require the Student to confirm the registration if all checks pass, subsequently updating available seats and displaying a success or error message.

#### Drop Course Section
* The system shall allow the Student to view registered Course Sections.
* The system shall allow the Student to select a Course Section to view registration details like Course, Section, Instructor, Schedule, and Registration Status.
* The system shall allow the Student to confirm dropping a course section.
* The system shall validate that the section was registered by the Student and conforms to drop rules.
* The system shall process the drop, update available seats, and display a success message if valid, or show an error if invalid.

#### View Registered Courses
* The system shall allow the Student to select a Semester to view their registered Course Sections.
* The system shall allow the Student to select a Course Section to view detailed registration metrics.
* The system shall display the corresponding Course, Course Section, Instructor, Schedule, Room, and Registration Status.

---

## II. Non-Functional Requirements

### Product Requirements

#### Usability Requirements

##### Usability
* The system shall automatically adjust the interface layout according to the user's screen size.
* The system shall provide a clear, consistent, and user-friendly interface for Students, Lecturers, and Administrators.
* Course, course-section, room, schedule, capacity, and lecturer information shall be presented clearly.
* Course-section status shall be displayed clearly, including Available, Full, and Not Available where applicable.
* Lecturer-assignment status shall clearly indicate whether a course section is Assigned or Unassigned.
* Error messages and notifications shall clearly explain the reason for failed operations.

#### Efficiency Requirements

##### Performance
* The system shall respond to common user requests such as login, course viewing, course-section viewing, registration, course dropping, and teaching-schedule viewing within 3 seconds under normal operating conditions.
* The system shall remain responsive during peak course-registration periods.

##### Scalability
* The system shall support an increasing number of students, lecturers, majors, courses, course sections, semesters, and registration records.

#### Dependability Requirements

##### Availability
* The system shall be available during normal academic operations and throughout active registration periods, except during scheduled maintenance.
* Scheduled maintenance should be performed outside active registration periods whenever possible.

##### Reliability
* The system shall ensure correct and reliable processing of course-section registration, course dropping, lecturer assignment, and course-section selection.
* If a transaction fails, incomplete changes shall be rolled back so that no partial or invalid data remains.
* The system shall prevent duplicate registration of the same course section by the same student.

##### Data Integrity
* The system shall maintain valid relationships among Major, Student, Course, Course Section, Lecturer, Teaching Qualification, Registration, and Teaching Assignment data.
* A student shall only register for courses belonging to the student's assigned major.
* A course section shall belong to an existing course.
* A lecturer assignment shall reference an existing lecturer and a valid course.
* A course section shall not be assigned to more than one lecturer at the same time.
* Deleting or updating records shall not create orphaned or inconsistent data.

##### Concurrency
* The system shall correctly handle simultaneous registration requests from multiple students.
* When only one seat remains in a course section, the system shall allow at most one student to successfully register for that seat.
* The system shall keep course-section capacity and enrollment data consistent after concurrent operations.
* Course-section registration transactions shall be processed atomically to prevent the section capacity from being exceeded.
* The system shall process concurrent registration requests without lost transactions, data inconsistency, or over-enrolment.

##### Backup and Recovery
* The system shall support scheduled backup of important user, course, course-section, registration, and teaching-assignment data.
* The system shall provide a recovery mechanism for restoring valid data after a critical failure.
* The system shall support restoration of normal operation after an unexpected failure.
* Recovered data shall not contain duplicate, partial, or inconsistent registration records.

#### Security Requirements

##### Authentication
* The system shall require users to authenticate using a valid username and password before accessing protected functions.
* User passwords shall not be stored as plain text and shall be protected using a secure password-storage mechanism.
* After 5 consecutive failed login attempts for the same account, the system shall temporarily block further login attempts for 15 minutes.
* The system shall allow authenticated users to change their password after verifying the current password.

##### Authorization
* The system shall enforce role-based access control for Student, Lecturer, and Administrator accounts.
* Students shall only access student functions such as viewing courses, viewing course sections, registering, dropping, and viewing registered courses.
* Lecturers shall only select course sections belonging to courses that have been assigned to them by an Administrator.
* Administrators shall have authority to manage users, majors, courses, semesters, course sections, registration information, teaching qualifications, and lecturer assignments.
* The system will reject unauthorized access attempts.

### Organizational requirements

#### Operational Requirements

##### Maintenance
* The system shall be designed to support easy maintenance and updates.
* Major functions such as user management, course management, semester management, course-section management, registration, and teaching assignment should be separated into manageable modules.
* Maintenance and software updates shall preserve existing user, academic, and registration data.

#### Development Requirements

##### Design Constraints
* The Course Registration System shall be implemented using Python as the primary programming language.
* The system shall use PostgreSQL as the relational database management system.
* The system shall use DBeaver to connect to and manage the PostgreSQL database.

---

## III. Data Flow Diagram

## IV. Use case Diagram

## V. Class Diagram

## VI. Data Model
