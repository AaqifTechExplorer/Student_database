from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite database for local use
app.config['SECRET_KEY'] = 'your_secret_key'  # Secret key for session management
db = SQLAlchemy(app)

# Database Model for Students
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(10), nullable=False, unique=True)
    student_class = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(5), nullable=False)
    parent_phone = db.Column(db.String(15), nullable=False)

# Routes

@app.route('/')
def index():
    """Route to display all students."""
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    """Route to add a new student."""
    if request.method == 'POST':
        # Get data from form
        name = request.form['name']
        roll_number = request.form['roll_number']
        student_class = request.form['class']
        section = request.form['section']
        parent_phone = request.form['parent_phone']

        # Create a new student record
        new_student = Student(name=name, roll_number=roll_number,
                              student_class=student_class, section=section, 
                              parent_phone=parent_phone)
        db.session.add(new_student)  # Add the record to the session
        db.session.commit()  # Commit the session to save the record to the database
        
        return redirect(url_for('index'))  # Redirect to the main page after adding

    return render_template('add_student.html')  # Render form if method is GET

@app.route('/delete/<int:id>')
def delete_student(id):
    """Route to delete a student by ID."""
    student = Student.query.get_or_404(id)  # Get the student by ID
    db.session.delete(student)  # Delete the student record
    db.session.commit()  # Commit the session
    return redirect(url_for('index'))  # Redirect back to the main page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables (only needs to be run once)
    app.run(debug=True)  # Run the Flask app in debug mode
