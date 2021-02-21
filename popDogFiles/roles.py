from re import search
from flask import Blueprint, redirect, render_template, url_for, flash, session, request
from .__init__ import db

roles = Blueprint('roles', __name__, template_folder='templates', static_folder='static')

@roles.route('/roles/edit')
def editRoles():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()

    if profileInfo[5] != "Administrativo":
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('call getRoleless')
    roleless = cur.fetchall()
    cur.close()
    return render_template('rolesEdit.html',roleless=roleless, search='')
    

@roles.route('/roles/edit', methods=['POST'])
def editRolesPost():
    cedula = request.form['cedula']

    cur = db.connection.cursor()
    cur.execute('call getRolelessSearch(%s)', [cedula])
    roleless = cur.fetchall()
    cur.close()

    print(type(roleless[0][0]))
    print(roleless[0][0] == int(session['id']))
    print(type(int(cedula)))

    return render_template('rolesEdit.html',roleless=roleless, search=session['id'])

@roles.route('/roles/giveRole')
def giveRole():
    if not session:
        return redirect(url_for('auth.login'))

    cedula = request.args.get('cedula')

    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [cedula])
    profileInfo = cur.fetchone()

    return render_template('giveRole.html', profileInfo=profileInfo)

@roles.route('/roles/giveRole', methods=['POST'])
def giveRolePost():

    cedula = request.args.get('cedula')
    rol = request.form['rol']
    cur = db.connection.cursor()
    cur.execute('call giveRole(%s,%s)', [cedula,rol])


    db.connection.commit()

    return redirect(url_for('roles.editRoles'))

@roles.route('/roles/roleFiller', methods=[''])
def roleFiller():
    
    

    tableSelector = {
        'Administrativo': 'administrativos',
        'Médico': 'medico',
        'Paciente': 'pacientes',
        'Enfermero': 'enfermeras',
        'Ingeniero': 'ingenieros',
        'Servicios': 'serviciosGenerales'
    }