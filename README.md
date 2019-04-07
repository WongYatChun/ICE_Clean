# ICE_Clean

Please run under the env ICE:
Linux: source env/ICE/bin/activate
you may need to install other stuff to run the code as well,

Superuser: rex
pwd: 890-iop[

Instructor:
You need to create it in the admin page

Learner:
Please sign up at

http://127.0.0.1:8000/accounts/signup/

Email confirmation will be sent at the backend,

no need to provide a true email

The most important url:

http://127.0.0.1:8000/myaccounts/profile/

For student

http://127.0.0.1:8000/students/courses/

http://127.0.0.1:8000/

For instructor

http://127.0.0.1:8000/course/mine/


Has been implemented:

Course Creation and Review:

(for Instructors) Create courses and add modules. By default, adding a module will append that
module to any existing sequence;

(for Instructors) View their courses, modules and components;

(for Instructors) Have sole permission to modify courses and modules they have created.
Course Selection, Enrolment and Access:

(for Learners) Browse courses that are currently open for enrolment, including the possibility to
browse courses by category;

(for Learners) View details of a course, such as its description

(for Learners) Enrol in a course;

(for Learners) Access any course or module they have previously completed to refresh their
knowledge;

(for Learners) Register as a Learner, providing their Staff ID Number, and receive a token, link,
or similar by email to the address in their company account enabling them to register as a
Learner;

(for Learners) Use the token/link to register, specifying a username and password for subsequent
authentication;

(for Learners) Have their Staff ID Number, email address, first name and last name from their
company account added to their new ICE account;

(for Instructor and Learner) After successful registration, be able to log in and access ICE
features available for their role;

(for Administrators) Control access to ICE through user authentication based on username and
password;

(for Administrators) Restrict permission to create and modify components, modules and courses
to the subset of users registered as Instructors;


Not yet implemented: Send invitations to Instuctors, Quiz, CECUs related, statistics

(for Learners) Have a record kept of courses they have passed and the date of completion;

(for HR) Prevent Learners from enrolling in the same course more than once.
Registration and Authentication

(for Instructors) Receive a token, link, or similar by email enabling them to register as an
Instructor;

(for Instructors) Use the token/link to register, specifying:
    o a short autobiography/self-introduction for prospective Learners;

(for Instructors) Have their email address (the address to which the invitation was sent) added to
their new ICE account by default;

(for Learners) Have their Staff ID Numberadded to their new ICE account;

(for Learners) On achieving a passing mark in the quiz of the last module, pass the course;

Statistics
