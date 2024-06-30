from flask import Flask, render_template, g, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.path.join('db', 'db', 'database.db')

# DataBase establish
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('db/sql/init.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
# database creation ends here

# crud operations
@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        class_name = request.form['class']
        roll_no = request.form['roll']

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO student (name, dob, email, phone, class, roll) VALUES (?, ?, ?, ?, ?, ?)',
                (name, dob, email, phone, class_name, roll_no)
            )
            db.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error: {e}")
            return redirect(url_for('error_page'))
    
    # display student table
@app.route('/students')
def student_list():
    db = get_db()
    cursor = db.execute('SELECT * FROM student')
    students = cursor.fetchall()
    return render_template('student.html', students=students)








# app templates and all other
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    return render_template('student.html')



# error page
@app.route('/error')
def error_page():
    return "An error occurred. Please try again."

# start app
if __name__ == '__main__':
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    init_db()
    app.run(debug=True)