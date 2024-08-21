from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from main_image_detector import process_image
from algo import find_best_time_from_csv


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SECRET_KEY'] = "SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///timetable.db'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = 'image'


db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    tag = db.Column(db.String(16), nullable=False)
    dept = db.Column(db.String(16), nullable=False)
    selected_flag = db.Column(db.Boolean, default = False)
    image = db.Column(db.String(64))

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    results = Student.query.filter_by(selected_flag = True).all()
    return render_template('home.html', results=results)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/add_student')
def add_student():
    return render_template('add_student.html')

@app.route('/add_student', methods=['POST'])
def add_student_post():
    name = request.form.get('name')
    tag = request.form.get('year_tag')
    dept = request.form.get('dept')

    if not name or not tag or not dept:
        return redirect(url_for('add_student'))
    
    new_student = Student(name=name, tag=tag, dept=dept)
    db.session.add(new_student)
    db.session.flush()  

    if 'timetable' in request.files:
        file = request.files['timetable']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f"timetable_{new_student.id}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            new_student.image = new_filename  

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

@app.route('/find_optimal', methods = ['POST'])
def find_optimal():
    student_ids = request.form.getlist('student_ids')
    csv_files = []
    for id in student_ids:
        student = Student.query.get(id)
        image_filename = student.image
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        student.selected_flag = False

        csv_file_name = process_image(image_path)
        csv_file_path = os.path.join(csv_file_name)
        csv_files.append(csv_file_path)

    optimal_time = find_best_time_from_csv(*csv_files)
    
    return render_template('home.html', optimal_time=optimal_time)


