"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
db_cursor = db_connection.cursor()


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ?
        """

    db_cursor.execute(QUERY, (github,))
    row = db_cursor.fetchone()

    if row == None:
        print "That student is not on file."
    else:
        print "Student: %s %s\nGithub account: %s" % (
            row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.
    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""

    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()

    print "Successfully added student: %s %s" %(first_name, last_name)


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """SELECT * FROM Projects WHERE title = ? """

    db_cursor.execute(QUERY, (title,))
    row = db_cursor.fetchone()

    if row == None:
        print "Invalid title."
    else:
        print "Project ID: %d, Project title: %s, Project description: %s, Max Grade: %d" % (
        row[0], row[1], row[2], row[3]) 


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""

    QUERY = """SELECT grade FROM Grades
                WHERE student_github = ? AND project_title = ?"""

    db_cursor.execute(QUERY, (github, title))
    row = db_cursor.fetchone()

    if row == None:
        print "Invalid student or project."
    else:
        print "Here's the grade for %s's %s: %s" % (github, title, row[0])


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""

    QUERY = """INSERT INTO Grades VALUES (?, ?, ?)"""

    db_cursor.execute(QUERY, (github, title, grade))
    db_connection.commit()

    print "Successfully added %s's grade for %s" % (github, title)

def assign_project(title, max_grade, description):
    """Create a project with a given title, max grade and description of any length."""

    QUERY = """INSERT INTO Projects (title, max_grade, description) VALUES(?, ?, ?)"""

    db_cursor.execute(QUERY, (title, max_grade, description))
    db_connection.commit()

    print "Successfully added project: %s" % (title)

def get_all_grades(github):
    """Gets all grades for a student"""

    QUERY = """SELECT grade, project_title FROM Grades WHERE student_github = ?"""

    db_cursor.execute(QUERY, (github, ))
    results = db_cursor.fetchall()

    if results == []:
        print "This github doesn't exist!"
    else:
        for result in results:
            grade, title = result
            print "Here are the grades for %s: %s, %s" % (github, title, grade)

def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(args) != 1:
                print "Please enter the github handle of a student."
            else:
                github = args[0]
                get_student_by_github(github)

        elif command == "new_student":
            if len(args) != 3:
                print "Please enter first_name, last_name, and github."
            else: 
                first_name, last_name, github = args   # unpack!
                make_new_student(first_name, last_name, github)

        elif command == "project_title":
            if len(args) != 1:
                print "Please enter a project title."
            else: 
                title = args[0]
                get_project_by_title(title)

        elif command == "get_grade":
            if len(args) != 2:
                print "Please enter github and project title."
            else:
                github = args[0]
                title = args[1]
                get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            if len(args) != 3:
                print "Please enter GitHub, project title, and grade."
            else: 
                github = args[0]
                title = args[1]
                grade = args[2]
                assign_grade(github, title, grade)

        elif command == "assign_project":
            if len(args) < 3:
                print "Please enter title, max grade and description."
            else:
                title = args[0]
                max_grade = args[1]
                description = " ".join(args[2:])
                assign_project(title, max_grade, description)

        elif command == "get_grades":
            if len(args) != 1:
                print "Please enter a student github handle."
            else:
                github = args[0]
                get_all_grades(github)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close()
