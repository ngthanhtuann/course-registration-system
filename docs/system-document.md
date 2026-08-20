# COURSE REGISTRATION SYSTEM SPECIFICATION

## I. Functional Requirements

### Login (User Authentication)

### Manage Account

### Manage Student

### Manage Lecturer

### Manage Major

### Manage Curriculum

### Manage Courses (Admin)
This function allows the Admin to manage course catalog data and set up prerequisite constraints.
* The system shall allow the Admin to view and search Courses by Course Code or Course Name.
* The system shall allow the Admin to create a Course requiring Course Code, Course Name, Credit, and Prerequisite.
* The system shall allow the Admin to view Course details, edit Course information, delete a Course (requiring confirmation), and set prerequisite courses.
* The system shall validate constraints: Course Code is unique, Credit value is valid, Prerequisite is an existing Course, and a Course cannot be its own prerequisite.  

### Manage Semester (Admin)
This function allows the Admin to create and manage academic semesters and their timeframes.
* The system shall allow the Admin to create a Semester by providing Semester Name, Start Date, and End Date.
* The system shall allow the Admin to select a Semester to view information (Semester Name, Start Date, End Date, Semester Status), edit information, or delete a Semester (requiring confirmation).
* The system shall validate that Start Date is earlier than End Date, Semesters do not overlap, and dates are valid.

### Manage Registration Period (Admin)
This function allows the Admin to define, open, close, and monitor course registration timeframes for semesters.
* The system shall allow the Admin to select a Semester and manage the Course Registration Period.
* The system shall allow the Admin to set Registration Start Date/Time and Registration End Date/Time.
* The system shall allow the Admin to Open, Close, and view Registration Status (Not Started, Open, Closed).
* The system shall validate that Start Date/Time is earlier than End Date/Time, the period is within the Semester duration, and another Round 1 registration is not active.

### Manage Registration Demand (Admin)
This function allows the Admin to monitor student course registration demands and generate registration summary reports.  
* The system shall allow the Admin to select a Semester and view Registration Demand (Course Code, Course Name, Number of Registered Students).
* The system shall allow the Admin to view the Student List for a Course (Student ID, Student Name, Email, Registration Status).
* The system shall allow the Admin to search Courses by Course Code or Course Name.
* The system shall allow the Admin to generate a Registration Demand Report containing Course Code, Course Name, Number of Students, and Registration List.

### Assign Lecturer (Admin)
This function allows the Admin to assign qualified lecturers to teach specific offered courses.
* The system shall allow the Admin to select a Major, select a Course, and view Lecturers qualified to teach the selected Course.
* The system shall allow the Admin to view Lecturer qualifications, select a qualified Lecturer, and assign the selected Lecturer to the Course.
* The system shall validate that the Lecturer is qualified to teach the Course and display appropriate success/error messages.

### View Lecturer Teaching Assignment
* The system shall allow the Admin to select a Major and Course.
* The system shall allow the Admin to view the Lecturers assigned to the selected Course.
* The system shall allow the Admin to select a Lecturer.
* The system shall allow the Admin to view the selected Lecturer's teaching assignments.
* The system shall display the Course Sections assigned to the Lecturer.
* The system shall display the Lecturer's teaching schedule.

#### Manage Teaching Course (Lecturer)
This function allows Lecturers to view the list of courses officially assigned to them by the Admin for a specific semester.
* The system shall allow the Lecturer to select a Semester and view Courses directly assigned to them by the Admin (Course Code, Course Name, Credit, Prerequisite).  
* The system shall allow the Lecturer to view the details of each assigned Course.
* The system shall prevent Lecturers from independently registering, requesting, self-assigning, or modifying Course assignments.
* The system shall display an appropriate message if no Courses are assigned for the selected Semester and automatically update the teaching list when assignments change.

#### Manage Student Grades (Lecturer)

#### View Courses (Student)

#### Course Registration (Student)

#### View Registration Status (Student)

#### Drop Course (Student)

#### DView Grades (Student)

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
