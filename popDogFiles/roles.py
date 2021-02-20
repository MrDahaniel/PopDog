from flask import Blueprint, session, redirect, url_for, render_template
from flask.helpers import flash
from werkzeug.security import check_password_hash, generate_password_hash
from .__init__ import db 

roles = Blueprint('roles', __name__, template_folder='templates', static_folder='static')

@roles.route('/admin') 
def admin():
    #If not logged in, redirect to login page.
    if not session:
        return redirect(url_for('auth.login', session=session))

    #First thing to do, get a cursor and call the user info from perfiles
    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()
    cur.close()

    return render_template('admin.html', profileInfo=profileInfo)

#@roles.route()
#def medico():

#@roles.route() 
#def engie():

#@roles.route() 
#def sergen():

#@roles.route() 
#def enfermeras():

#@roles.route() 
#def pacientes():
