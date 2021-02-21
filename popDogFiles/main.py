from flask import Flask, Blueprint, render_template, url_for, redirect, session
from flask.helpers import flash
from .__init__ import db

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    if session and not 'id' in session:
        print(session)
        session.clear()
        flash('Error al iniciar sesión, error de cookies. De seguir sucediendo, limpie las cookies de su navegador', 'alert')
        return redirect(url_for('auth.login'))

    if session:
        cur = db.connection.cursor()
        cur.execute('call getRole(%s)', [session['id']])
        role = cur.fetchone()

    if session and role[0] == None:
        return render_template('index.html')

    if session:
        return redirect(url_for('dashboard.dash'))

    return render_template('index.html')

@main.route('/profile')
def profile():
    #If not logged in, redirect to login page.
    if not session:
        return redirect(url_for('auth.login'))

    #First thing to do, get a cursor and call the user info from perfiles
    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()
    cur.close()

    return render_template('profile.html', profileInfo=profileInfo)

@main.route('/tester')
def asd():
    print(session)
    return "owo"

