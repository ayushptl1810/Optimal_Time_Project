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
    selected_flag = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    results = Student.query.filter_by(selected_flag = True).all()
    return render_template('home.html', results=results)

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/add_student', methods = ['POST'])
def add_student_post():
    name = request.form.get('name')
    tag = request.form.get('year_tag')
    dept = request.form.get('dept')

    if not name or not tag or not dept:
        return redirect(url_for('add_student'))
    
    new_student = Student(name=name, tag=tag, dept=dept)
    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('add_student'))

@app.route('/filter')
def filter():
    return render_template('filter.html')

@app.route('/filter', methods=['POST'])
def filter_post():
    query = Student.query
    filters = []
    
    name = request.form.get('name')
    tags = request.form.getlist('year_tag')
    depts = request.form.getlist('dept')

    if name:
        filters.append(Student.name.like(f"%{name}%"))
    if tags:
        filters.append(Student.tag.in_(tags)) 
    if depts:
        filters.append(Student.dept.in_(depts))

    filters.append(Student.selected_flag == False)
    query = query.filter(*filters)

    results = query.all()
    return render_template('filter.html', results=results, name=name, tag=tags, dept=depts)

@app.route('/add_filter', methods=['POST'])
def add_filter():
    student_id = request.form.get('id')
    student = Student.query.get(student_id)
    student.selected_flag = True
    db.session.commit()

    name = request.form.get('name')
    tag = request.form.get('year_tag')
    dept = request.form.get('dept')

    query = Student.query
    filters = []

    if name:
        filters.append(Student.name.like(f"%{name}%"))
    if tag:
        tags = tag.split(',')
        filters.append(Student.tag.in_(tags))
    if dept:
        depts = dept.split(',')
        filters.append(Student.dept.in_(depts))

    filters.append(Student.selected_flag == False)
    query = query.filter(*filters)

    results = query.all()

    return render_template('filter.html', results=results, name=name, tag=tag, dept=dept)


@app.route('/remove', methods = ['POST'])
def remove():
    student_id = request.form.get('id')
    student = Student.query.get(student_id)
    student.selected_flag = False
    db.session.commit()

    return redirect(url_for('home'))