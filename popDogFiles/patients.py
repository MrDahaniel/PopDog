from flask import Blueprint, session, flash, render_template, redirect, url_for
from flask.globals import request
from flask.templating import render_template, render_template_string
from .__init__ import db

patients = Blueprint('patients', __name__)

@patients.route('/patients')
def patientsHandle():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if not role in ["Administrativo", 'Médico', 'Enfermero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('call getInPatients()')
    ingresados = cur.fetchall()

    cur.execute('call getOutPatients()')
    salidos = cur.fetchall()

    cur.execute('select * from medioEntrada')
    mediosEntrada = cur.fetchall()

    return render_template('patients.html', ingresados=ingresados, salidos=salidos, mediosEntrada=mediosEntrada, role=role)

@patients.route('/patients', methods=['POST'])
def patientsHandlePost():
    cur = db.connection.cursor()

    return render_template('patients.html')

@patients.route('/patients/in', methods=['POST'])
def patientHandleIn():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if not role in ["Administrativo", 'Médico', 'Enfermero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))
    
    cedula = request.form['cedula']
    medio = request.form['medio']

    cur.execute('select idPaciente from pacientes where cedula = %s', [cedula])
    idPaciente = cur.fetchone()[0]

    if idPaciente == None:
        flash('La persona ingresada no tiene perfil de paciente creado', 'alert')
        return redirect(url_for('patients.patientsHandle'))

    cur.execute('select * from ingresos where idPaciente = %s and estado = false', [idPaciente])
    ingresado = cur.fetchall()
    
    print(ingresado)

    if ingresado:
        flash('El paciente ya está ingresado en el sistema', 'alert')
        return redirect(url_for('patients.patientsHandle'))

    cur.execute('insert into ingresos (idPaciente,idMedio,fecha,hora) values (%s,%s,curdate(),curtime())', [idPaciente,medio])

    cur.connection.commit()

    flash('Ingreso generado', 'ok')

    return redirect(url_for('patients.patientsHandle'))

@patients.route('/patients/Out')
def patientHandleOut():
    ingreso = request.args.get('ingreso')
    paciente = request.args.get('patient')
    
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if not role in ["Administrativo", 'Médico', 'Enfermero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('call getMedicProfile(%s)', [session['id']])
    medic = cur.fetchone()[7]
    cur.execute('update ingresos set estado = true where idIngreso = %s', [ingreso])
    cur.execute('insert into salidas (idPaciente,idMedicoAut,fecha,hora) values (%s,%s, curdate(),curtime())', [paciente, medic])

    cur.connection.commit()

    return redirect(url_for('patients.patientsHandle'))