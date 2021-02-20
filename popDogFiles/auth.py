from typing import final
from flask import Flask, Blueprint, render_template, url_for, redirect, request, session
from flask.helpers import flash
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
from .__init__ import db
from datetime import date
import re

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    #If logged in, redirect to main page
    if session:
        return redirect(url_for('main.index', session=session))

    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def loginPost():
    #Getting form inputs
    cedula = request.form['cedula']
    password = request.form['password']

    #Making a conn with cur to make quesries at app level
    cur = db.connection.cursor()

    #Gets passhash from the database
    cur.execute('select nombre, passhash from perfiles where cedula=%s', [cedula])
    data = cur.fetchone()

    #If passwords are the same, logs the user in. To avoid nullpo, uses try block
    if len(data) != 0:
        if check_password_hash(data[1], password):
            session['loggedin'] = True 
            session['id'] = cedula
            session['username'] = data[0] #username = nombre
            flash('¡Bienvenido!', 'ok')
            return redirect(url_for('main.index', session=session))

    cur.close();
    
    flash('Los datos ingresados son incorrectos. ¿Quizás ingresó algo incorrectamente o no está registrado?', 'alert')
    return redirect(url_for('auth.login'))

@auth.route('/signup')
def signup():
    #If logged in, redirect to main page
    if session:
        return redirect(url_for('main.index', session=session))
    return render_template('signup.html', date=date.today())

@auth.route('/signup', methods=['POST'])
def signupPost():
    #Getting form inputs
    name = request.form['name']
    fecha = request.form['fecha']
    sexo = request.form['sexo']
    phone = request.form['phone']
    cedula = request.form['id']
    password = request.form['password']

    #Making a conn with cur to make quesries at app level
    cur = db.connection.cursor()

    #Checks if there is a profile already
    cur.execute('select * from perfiles where cedula=%s limit 1', [cedula])
    data = cur.fetchall()

    #Checks for an existing id, if so, redirects and flashes into auth.login
    if len(data) != 0:
        flash('Cédula ya registrada, ¿Intentaste hacer Login?', 'alert')
        return redirect(url_for('auth.login'))

    passhash = generate_password_hash(password, method='sha256')
    cur.execute('call createProfile(%s,%s,%s,%s,%s,%s)', (cedula, name, fecha, sexo, phone, passhash))   
    db.connection.commit()
    cur.close();
    
    flash('Cuenta creada satisfactoriamente', 'ok')
    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))