# === PART 1 : IMPORTS, DATA CREATION & DEFAULT SETUP ===
import pandas as pd
import numpy as np

# Initialize DataFrames for all core entities
users = pd.DataFrame(columns=["username", "password", "role"])
students = pd.DataFrame(columns=["username", "name", "roll_no", "department", "year"])
exams = pd.DataFrame(columns=["exam_id", "subject", "date"])
enrollments = pd.DataFrame(columns=["username", "exam_id"])
results = pd.DataFrame(columns=["username", "exam_id", "marks"])
messages = pd.DataFrame(columns=["sender", "receiver", "role", "message", "timestamp"])
help_box = pd.DataFrame(columns=["username", "query", "status", "timestamp"])
reexam_requests = pd.DataFrame(columns=["username", "exam_id", "reason", "status", "timestamp"])
leave_requests = pd.DataFrame(columns=["username", "exam_id", "reason", "status", "timestamp"])
feedback = pd.DataFrame(columns=["username", "type", "target", "rating", "comments", "timestamp"])
exam_schedule = pd.DataFrame(columns=["exam_id", "venue", "seat_no", "slot_time"])

# Create default admin users
users.loc[len(users)] = ["vignesh", "1234", "admin"]
users.loc[len(users)] = ["sandhya", "5678", "admin"]

# Default student data (username, name, roll_no, dept, year)
students_data = [
    ("arman", "Arman Sinha", "101", "CSE", "2nd"),
    ("akarsh", "Akarsh Mehta", "102", "ECE", "2nd"),
    ("hitesh", "Hitesh Rao", "103", "EEE", "2nd"),
    ("advaith", "Advaith Sharma", "104", "MECH", "2nd"),
    ("ashankk", "Ashank Kumar", "105", "CIVIL", "2nd"),
]

# Add students and create user accounts for each
for s in students_data:
    users.loc[len(users)] = [s[0], "pass123", "student"]
    students.loc[len(students)] = s

# Create default exam data
exams_data = [
    ("E101", "Maths", "2025-11-20"),
    ("E102", "Physics", "2025-11-25"),
    ("E103", "Chemistry", "2025-12-01"),
]
for e in exams_data:
    exams.loc[len(exams)] = e

# Default exam schedule setup
exam_schedule.loc[len(exam_schedule)] = ["E101", "Hall A", "A1", "09:00-12:00"]
exam_schedule.loc[len(exam_schedule)] = ["E102", "Hall B", "B1", "13:00-16:00"]
exam_schedule.loc[len(exam_schedule)] = ["E103", "Hall C", "C1", "09:00-12:00"]

# Enroll all default students in all exams and assign random marks
for u in ["arman", "akarsh", "hitesh", "advaith", "ashankk"]:
    for e in ["E101", "E102", "E103"]:
        enrollments.loc[len(enrollments)] = [u, e]
        results.loc[len(results)] = [u, e, np.random.randint(40, 100)]

# Create sample messages, help requests, and feedback for realism
ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
for u in ["arman", "akarsh", "hitesh", "advaith", "ashankk"]:
    messages.loc[len(messages)] = [u, "vignesh", "admin", f"Hello from {u}", ts]
    messages.loc[len(messages)] = ["vignesh", u, "student", f"Hi {u}, got your message", ts]
    help_box.loc[len(help_box)] = [u, f"I need help with portal access - {u}", "resolved", ts]
    reexam_requests.loc[len(reexam_requests)] = [u, "E101", "Low marks", "approved", ts]
    leave_requests.loc[len(leave_requests)] = [u, "E102", "Medical reason", "approved", ts]
    feedback.loc[len(feedback)] = [u, "exam", "E101", np.random.randint(3, 5), "Good exam", ts]
    feedback.loc[len(feedback)] = [u, "faculty", "vignesh", np.random.randint(4, 5), "Helpful teacher", ts]

print("System initialized with default admins and student data!\n")
# === PART 2 : REGISTRATION, LOGIN & MAIN SUPPORT ===

# Register a new student and add their details
def register_student():
    username = input("Enter username: ")
    password = input("Enter password: ")
    name = input("Enter full name: ")
    roll_no = input("Enter roll number: ")
    dept = input("Enter department: ")
    year = input("Enter year of study: ")

    if username in users["username"].values:
        print("Username already exists!")
        return

    users.loc[len(users)] = [username, password, "student"]
    students.loc[len(students)] = [username, name, roll_no, dept, year]
    print("Student registered successfully!\n")

# Login system for both admins and students
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    user = users[(users["username"] == username) & (users["password"] == password)]

    if not user.empty:
        print("Login successful!\n")
        return user.iloc[0]["role"], username
    else:
        print("Invalid credentials.\n")
        return None, None
# === PART 3 : STUDENT MENU (PROFILE, EXAMS, RESULTS, MESSAGES) ===

# Show performance report summary
def show_performance_reports():
    if results.empty:
        print("No results available.")
        return

    totals = []
    for u in results["username"].unique():
        total = np.sum(results[results["username"] == u]["marks"].astype(float))
        totals.append((u, total))
    totals_df = pd.DataFrame(totals, columns=["username", "total_marks"]).sort_values(by="total_marks", ascending=False)
    print("\nRankings:\n", totals_df.head(10))

    # Display average per subject
    for eid in results["exam_id"].unique():
        subject = exams[exams["exam_id"] == eid]["subject"].iloc[0]
        marks = results[results["exam_id"] == eid]["marks"].astype(float).values
        avg = np.mean(marks)
        print(f"\n{subject} ({eid}) Average: {avg:.2f}")

# Core student menu for general activities
def student_menu(username):
    while True:
        print("\n--- Student Menu ---")
        print("1. View Profile\n2. Enroll in Exam\n3. View Enrollments & Schedule\n4. View Results\n5. Send Message\n6. Read Messages\n7. Submit Help Query\n8. View Help Queries\n9. Apply for Re-Exam\n10. View Re-Exam Requests\n11. Request Leave/Postpone\n12. View Leave Requests\n13. Submit Feedback\n14. View Rankings\n15. Logout")
        c = input("Enter choice: ")

        if c == "1":
            print(students[students["username"] == username])
        elif c == "2":
            print(exams)
            eid = input("Enter Exam ID: ")
            if eid in exams["exam_id"].values:
                enrollments.loc[len(enrollments)] = [username, eid]
                print("Enrolled successfully!")
        elif c == "3":
            data = enrollments[enrollments["username"] == username]
            print(data)
            for eid in data["exam_id"].values:
                print(exam_schedule[exam_schedule["exam_id"] == eid])

        elif c == "4":
            data = results[results["username"] == username]
            print(data)
            for eid in data["exam_id"].values:
                subject = exams[exams["exam_id"] == eid]["subject"].iloc[0]
                avg = np.mean(results[results["exam_id"] == eid]["marks"].astype(float))
                print(f"{subject} average: {avg:.2f}")

        elif c == "5":
            receiver = input("Enter receiver username: ")
            msg = input("Enter message: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            role = users[users["username"] == receiver]["role"].iloc[0]
            messages.loc[len(messages)] = [username, receiver, role, msg, ts]

        elif c == "6":
            print(messages[messages["receiver"] == username])

        elif c == "7":
            q = input("Enter query: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            help_box.loc[len(help_box)] = [username, q, "open", ts]

        elif c == "8":
            print(help_box[help_box["username"] == username])

        elif c == "9":
            eid = input("Enter Exam ID: ")
            r = input("Enter reason: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            reexam_requests.loc[len(reexam_requests)] = [username, eid, r, "pending", ts]

        elif c == "10":
            print(reexam_requests[reexam_requests["username"] == username])

        elif c == "11":
            eid = input("Enter Exam ID: ")
            reason = input("Enter reason: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            leave_requests.loc[len(leave_requests)] = [username, eid, reason, "pending", ts]

        elif c == "12":
            print(leave_requests[leave_requests["username"] == username])

        elif c == "13":
            ftype = input("Type (exam/faculty): ")
            target = input("Target (exam id/faculty name): ")
            rating = input("Rating (1-5): ")
            comments = input("Comments: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            feedback.loc[len(feedback)] = [username, ftype, target, rating, comments, ts]

        elif c == "14":
            show_performance_reports()
        elif c == "15":
            break
# === PART 5 : ADMIN MENU & MAIN PROGRAM LOOP ===

def admin_menu(username):
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Exam\n2. View Exams\n3. Add Result\n4. View All Results\n5. View Messages\n6. Broadcast Message\n7. View Help Box\n8. View Re-Exam Requests\n9. View Leave Requests\n10. Set Exam Schedule\n11. View Feedback\n12. View Rankings\n13. Logout")
        c = input("Enter choice: ")

        if c == "1":
            eid = input("Exam ID: "); sub = input("Subject: "); date = input("Date: ")
            exams.loc[len(exams)] = [eid, sub, date]
        elif c == "2":
            print(exams)
        elif c == "3":
            u = input("Student Username: "); e = input("Exam ID: "); m = input("Marks: ")
            results.loc[len(results)] = [u, e, m]
        elif c == "4":
            print(results)
            for eid in results["exam_id"].unique():
                s = exams[exams["exam_id"] == eid]["subject"].iloc[0]
                print(s, np.mean(results[results["exam_id"] == eid]["marks"].astype(float)))
        elif c == "5":
            print(messages)
        elif c == "6":
            msg = input("Message: ")
            ts = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            for s in users[users["role"] == "student"]["username"].values:
                messages.loc[len(messages)] = [username, s, "student", msg, ts]
        elif c == "7":
            print(help_box)
        elif c == "8":
            print(reexam_requests)
        elif c == "9":
            print(leave_requests)
        elif c == "10":
            eid = input("Exam ID: "); v = input("Venue: "); s = input("Seat: "); slot = input("Slot: ")
            exam_schedule.loc[len(exam_schedule)] = [eid, v, s, slot]
        elif c == "11":
            print(feedback)
        elif c == "12":
            show_performance_reports()
        elif c == "13":
            break

# === MAIN PROGRAM LOOP ===
while True:
    print("\n===== UNIVERSITY EXAM PORTAL =====")
    print("1. Login\n2. Register as Student\n3. Exit")
    c = input("Enter choice: ")

    if c == "1":
        role, username = login()
        if role == "admin":
            admin_menu(username)
        elif role == "student":
            student_menu(username)
    elif c == "2":
        register_student()
    elif c == "3":
        print("Goodbye!")
        break
