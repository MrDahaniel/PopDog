from flask import Flask, Blueprint, render_template, url_for, redirect, session
from .__init__ import db

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    return render_template('index.html', session=session)

@main.route('/profile')
def profile():
    #If not logged in, redirect to login page.
    if not session:
        return redirect(url_for('auth.login', session=session))

    #First thing to do, get a cursor and call the user info from perfiles
    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()
    cur.close()

    return render_template('profile.html', session=session, profileInfo=profileInfo)
