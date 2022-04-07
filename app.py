from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = psycopg2.connect("host=database user=postgres password=mysecretpassword ")
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM cars ORDER BY ID ASC;')
    cars = cur.fetchall()
    conn.close()
    return render_template('index.html', posts=cars)
    
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        plate = request.form['plate']
        password = request.form['password']
        
        if not plate:
            flash('License plate is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.autocommit = True
            cur = conn.cursor()
            #cur.execute("INSERT INTO cars (plate, password) VALUES ('{}', '{}');".format(plate,password))
            cur.execute("UPDATE cars SET plate = '{}',password = '{}',is_free = FALSE WHERE id = (SELECT ID from cars WHERE is_free = TRUE LIMIT 1);".format(plate,password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/unpark/', methods=('GET', 'POST'))
def unpark():
    if request.method == 'POST':
        plate = request.form['plate']
        password = request.form['password']

        if not plate:
            flash('License plate is required!')
        elif not password:
            flash('Password is required!')
        else:
            conn = get_db_connection()
            conn.autocommit = True
            cur = conn.cursor()
            #cur.execute("INSERT INTO cars (plate, password) VALUES ('{}', '{}');".format(plate,password))
            cur.execute("UPDATE cars SET plate = '',password = '',is_free = TRUE WHERE plate = '{}' AND password = '{}' ;".format(plate,password))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('unpark.html')

    