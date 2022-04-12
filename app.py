from flask import Flask, render_template, request, url_for, flash, redirect
import psycopg2
from datetime import datetime
import time

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
            cur.execute("SELECT count(ID) from cars WHERE is_free = TRUE")
            places = cur.fetchall()
            if places[0][0] == 0:
                flash("Parking place is full please wait until place frees!")
                return redirect(url_for('create'))
            cur.execute("UPDATE cars SET plate = '{}',password = '{}',is_free = FALSE,time = '{}' WHERE id = (SELECT ID from cars WHERE is_free = TRUE LIMIT 1);".format(plate,password,str(datetime.now())))
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
            cur.execute("SELECT time from cars WHERE plate = '{}' AND password = '{}' ;".format(plate,password))
            time = cur.fetchall()
            date_format_str = '%Y-%m-%d %H:%M:%S.%f'
            try:
                start = datetime.strptime(time[0][0], date_format_str)
            except:
                flash("Wrong licence plate or password!")
                return redirect(url_for('unpark'))
            end = datetime.now()
            diff = end - start
            diff_in_hours = diff.total_seconds() / 3600
            money = diff_in_hours * 5
            flash("You need to pay {:.2f} euros".format(money))
            cur.execute("UPDATE cars SET plate = '',password = '',is_free = TRUE,time = '' WHERE plate = '{}' AND password = '{}' ;".format(plate,password))
            conn.commit()
            conn.close()
            return redirect(url_for('payment'))

    return render_template('unpark.html')
@app.route('/payment/',methods=('GET','POST'))
def payment():
    if request.method == 'POST':
        flash("Thanks for parking on our parking place. Payment accepted!")
        time.sleep(2)
        return redirect(url_for('index'))
    return render_template('payment.html')
    
