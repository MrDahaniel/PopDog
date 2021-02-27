from flask import Flask, Blueprint, render_template, url_for, redirect, session
from flask.helpers import flash
from .__init__ import db

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    if session and not 'id' in session:
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
    cedula = session['id']
    
    cur = db.connection.cursor()
    cur.execute('call getRole(%s)',[cedula])
    role = cur.fetchone()[0]

    horario = None
    especialidad = None
    ubicacion = None
    eps = None

    #Pain, time to make a if giberish 
    if role == 'Administrativo':
        cur.execute('call getAdminProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getSingleSchedule(%s)', [profileInfo[9]])
        horario = cur.fetchone()
        
    elif role == 'Médico':
        cur.execute('call getMedicProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getSingleSchedule(%s)', [profileInfo[10]])
        horario = cur.fetchone()
        cur.execute('call getSingleEspecial(%s)', [profileInfo[9]])
        especialidad = cur.fetchone()[0]
        
    elif role == 'Paciente':
        cur.execute('call getPatientProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getEPS(%s)', [profileInfo[10]])
        eps = cur.fetchone()[0]
        cur.execute('call getLocation(%s)', [profileInfo[9]])
        ubicacion = cur.fetchone()
        
    elif role == 'Enfermero':
        cur.execute('call getNurseProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getLocation(%s)', [profileInfo[10]])
        ubicacion = cur.fetchone()
        print(ubicacion)
        cur.execute('call getSingleSchedule(%s)', [profileInfo[10]])
        horario = cur.fetchone()
        
    elif role == 'Ingeniero':
        cur.execute('call getEngieProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getSingleSchedule(%s)', [profileInfo[9]])
        horario = cur.fetchone()
        
    elif role == 'Servicios':
        cur.execute('call getSerGenProfile(%s)', [cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getSingleSchedule(%s)', [profileInfo[9]])
        horario = cur.fetchone()

    else:
        cur.execute('call getProfile(%s)', [cedula])
        profileInfo = cur.fetchone()

    return render_template('profile.html', profileInfo=profileInfo, horario=horario, role=role, especialidad=especialidad, ubicacion=ubicacion, eps=eps)

@main.route('/tester')
def asd():
    print(session)
    return "owo"

