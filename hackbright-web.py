from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    results = hackbright.get_all_grades(github)

    html = render_template("student_info.html",
                            first = first,
                            last = last,
                            github = github,
                            results = results)
    return html

@app.route("/create-student")
def add_new_student():
    """Show form for creating a new student."""

    return render_template("new_student.html") 

@app.route("/display-new-student", methods=['POST'])
def display_new_student():
    """display new student info"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("access_new_student.html", 
                            github = github)


if __name__ == "__main__":
    app.run(debug=True)