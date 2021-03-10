from flask import Blueprint, session, redirect, url_for, render_template
from flask.helpers import flash
from werkzeug.security import check_password_hash, generate_password_hash
from .__init__ import db 

dashboard = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')

@dashboard.route('/dashboard')
def dash():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()

    if session and role[0] == None:
        return redirect('main.index')

    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()
    cur.close()

    templateSelector = {
        'Administrativo': 'dashboard.admin',
        'Médico': 'dashboard.medic',
        'Paciente': 'dashboard.patient',
        'Enfermero': 'dashboard.nurse',
        'Ingeniero': 'dashboard.engie',
        'Servicios': 'dashboard.sergen'
    }   

    return redirect(url_for(templateSelector[profileInfo[5]]))

@dashboard.route('/dashboard/admin') 
def admin():
    #If not logged in, redirect to login page.
    if not session:
        return redirect(url_for('auth.login'))

    #First thing to do, get a cursor and call the user info from perfiles
    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]
    cur.close()

    if role != 'Administrativo':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    return render_template('dashboard.html', role=role)

@dashboard.route('/dashboard/medic')
def medic():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]
    cur.close()
    
    if role != 'Médico':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))
    
    return render_template('dashboard.html', role=role)

@dashboard.route('/dashboard/engie') 
def engie():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]
    cur.close()
    
    if role != 'Ingeniero':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))
    
    return render_template('dashboard.html', role=role)

#@dashboard.route('/dashboard/sergen') 
#def sergen():

@dashboard.route('/dashboard/nurse') 
def nurse():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]
    cur.close()
    
    if role != 'Enfermero':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))
    
    return render_template('dashboard.html', role=role)

@dashboard.route('/dashboard/patient') 
def patient():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]
    cur.close()
    
    if role != 'Paciente':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    return render_template('dashboard.html', role=role)