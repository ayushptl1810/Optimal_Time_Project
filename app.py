from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SECRET_KEY'] = "SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///timetable.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    tag = db.Column(db.String(16), nullable=False)
    dept = db.Column(db.String(16), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/add_student', methods = ['POST'])
def add_student_post():
    name = request.form.get('name')
    tag = request.form.get('year_tag')
    dept = request.form.get('dept')

    if not name or not tag or not dept:
        flash('Fill all fields')
        return redirect(url_for('add_student'))
    
    new_student = Student(name=name, tag=tag, dept=dept)
    db.session.add(new_student)
    db.session.commit()

    flash('Student successfully added')
    return redirect(url_for('add_student'))
