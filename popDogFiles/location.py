from flask import Blueprint, flash, redirect, render_template, url_for, request, session
from .__init__ import db

location = Blueprint('location', __name__)

@location.route('/location')
def searchLocation():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()

    cur.execute('call getSectors()')
    sectors = cur.fetchall()
    return render_template('location.html',sectors=sectors)

@location.route('/location', methods=['POST'])
def searchLocationPost():

    profileInfo=None
    showProfile=False
    ubicacion=None

    cedula = request.form['cedula']
    sector = request.form['sector']

    cur = db.connection.cursor()
    cur.execute('call getSectors()')
    sectors = cur.fetchall()
    cur.execute('call getRole(%s)', [cedula])

    if cur.fetchone()[0] in ['Enfermero', 'Paciente']:
        showProfile = True
        cur.execute('call getProfile(%s)',[cedula])
        profileInfo = cur.fetchone()
        cur.execute('call getLocationSector(%s)', [sector])
        ubicacion = cur.fetchall()
    
    else:
        flash('La persona ingresada no existe o no tiene ubicación asignable', 'alert')
        redirect(url_for('location.searchLocation'))

    return render_template('location.html',cedula=cedula,showProfile=showProfile,profileInfo=profileInfo, search=cedula, ubicaciones=ubicacion, sectors=sectors)

@location.route('/location/ubicator')
def ubicatorGet():
    return redirect(url_for('location.searchLocation'))

@location.route('/location/ubicator', methods=['POST'])
def ubicator():

    cedula = request.args.get('cedula')
    role = request.args.get('role')
    idUbi = request.form['ubicacion']

    cur = db.connection.cursor()

    if role == 'Enfermero':
        cur.execute('update enfermeras set idUbicacion = %s where cedula = %s', [idUbi, cedula])

    else:
        cur.execute('update pacientes set idUbicacion = %s where cedula = %s', [idUbi, cedula])

    db.connection.commit()

    flash('Ubicación asignada correctamente', 'ok')
    return redirect(url_for('location.searchLocation'))