import re
from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from .__init__ import db

search = Blueprint('search', __name__, template_folder='templates', static_folder='static')

@search.route('/search')
def searchRedirector():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if role == 'Administrativo':
        cur.execute('call getAllProfiles()')
        perfiles = cur.fetchall()
        return render_template('search.html',role=role,perfiles=perfiles)

    return redirect(url_for('main.index'))

@search.route('/search', methods=['POST'])
def searchRedirectorPost():
    cedula = request.form['cedula']

    cur = db.connection.cursor()
    cur.execute('call getRolelessSearch(%s)', [cedula])
    roleless = cur.fetchall()
    cur.close()

    return render_template('search.html',perfiles=roleless, search=cedula,role=request.args.get('role'))

@search.route('/search/result')
def searchResult():
    cedula = request.args.get('cedula')
    role = request.args.get('rol')
    cur = db.connection.cursor()
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

    return render_template('searchResult.html', profileInfo=profileInfo, horario=horario, role=role, especialidad=especialidad, ubicacion=ubicacion, eps=eps)
