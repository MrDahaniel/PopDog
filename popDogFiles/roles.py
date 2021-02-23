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
    print(session)

    cedula = request.form['cedula']

    cur = db.connection.cursor()
    cur.execute('call getRolelessSearch(%s)', [cedula])
    roleless = cur.fetchall()
    cur.close()

    return render_template('rolesEdit.html',roleless=roleless, search=cedula, session=session)

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
    cur.close()

    return redirect(url_for('roles.roleFiller',cedula=cedula, rol=rol))

@roles.route('/roles/roleFiller')
def roleFiller():
    if not session:
        return redirect(url_for('auth.login'))

    cedula = request.args.get('cedula')
    rol = request.args.get('rol')

    cur = db.connection.cursor()
    cur.execute('select nombre from perfiles where cedula = %s', [cedula])
    nombre = cur.fetchone()

    # Queries para el médico Especialidades y Horarios
    if rol == 'Médico':
        cur.execute('call getEspec()')
        especialidades = cur.fetchall()
        cur.execute('call getSchedule()')
        horarios = cur.fetchall()
        cur.close()
        return render_template('roleFiller.html', cedula=cedula, nombre=nombre, rol=rol, especialidades=especialidades, horarios=horarios)

    elif rol == 'Enfermero' or rol == 'Ingeniero' or rol == 'Servicios' or rol == 'Administrativo':
        cur.execute('call getSchedule()')
        horarios = cur.fetchall()
        cur.close()
        return render_template('roleFiller.html', cedula=cedula, nombre=nombre, rol=rol, horarios=horarios)

    elif rol == 'Paciente':
        cur.execute('select * from EPS')
        eps = cur.fetchall()
        cur.close()
        return render_template('roleFiller.html', cedula=cedula, nombre=nombre, rol=rol, eps=eps)

    # This literally, should never happen, if so, be scared.
    return render_template('roleFiller.html', cedula=cedula, rol=rol)

@roles.route('/roles/roleFiller', methods=['POST'])
def roleFillerPost():
    cedula = request.args.get('cedula')
    print(cedula)
    cur = db.connection.cursor()

    if request.args.get('rol') == 'Médico':
        especialidad = request.form['especialidad']
        horario = request.form['horario']

        cur.execute('call getMedicProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            cur.execute('update medico set idEspecialidad=%s, idHorario=%s where cedula==%s', [especialidad,horario,cedula])
            flash('Médico actualizado correctamente', 'ok')
        else:    
            cur.execute('insert into medico (cedula,idEspecialidad,idHorario) values (%s,%s,%s)',[cedula,especialidad,horario])
            flash('Médico creado correctamente', 'ok')

        db.connection.commit()

    elif request.args.get('rol') == 'Enfermero':
        horario = request.form['horario']

        cur.execute('call getNurseProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            cur.execute('update enfermeras set idHorario = %s where cedula = %s', [horario,cedula])
            flash('Enfermero actualizado correctamente', 'ok')
        else:
            cur.execute('insert into enfermeras (cedula, idHorario) values (%s,%s)', [cedula,horario])
            flash('Enfermero creado correctamente', 'ok')

        db.connection.commit()

        
    elif request.args.get('rol') == 'Ingeniero':
        horario = request.form['horario']

        cur.execute('call getEngieProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            flash('Ingeniero actualizado correctamente', 'ok')
            cur.execute('update ingenieros set idHorario = %s where cedula = %s', [horario,cedula])
        else:
            flash('Ingeniero creado correctamente', 'ok')
            cur.execute('insert into ingenieros (cedula, idHorario) values (%s,%s)', [cedula,horario])

        db.connection.commit()


    elif request.args.get('rol') == 'Servicios':
        horario = request.form['horario']

        
        cur.execute('call getSerGenProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            cur.execute('update serviciosGenerales set idHorario = %s where cedula = %s', [horario,cedula])
            flash('Personal de servicios generales actualizado correctamente', 'ok')
        else:
            cur.execute('insert into serviciosGenerales (cedula, idHorario) values (%s,%s)', [cedula,horario])
            flash('Personal de servicios generales creado correctamente', 'ok')
        db.connection.commit()

    elif request.args.get('rol') == 'Administrativo':
        horario = request.form['horario']
        area = request.form['area']
        
        cur.execute('call getAdminProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            cur.execute('update administrativos set idHorario = %s where cedula = %s', [horario,cedula])
            flash('Administrativo actualizado correctamente', 'ok')
        else:
            cur.execute('insert into administrativos (cedula, idHorario,areaAsig) values (%s,%s,%s)', [cedula,horario,area])
            flash('Administrativo creado correctamente', 'ok')
        db.connection.commit()

    elif request.args.get('rol') == 'Paciente':
        eps = request.form['eps']
        peso = request.form['peso']
        
        cur.execute('call getPatientProfile(%s)',[cedula])
        doubleChecker = cur.fetchall()

        if len(doubleChecker) != 0:
            cur.execute('update pacientes set idEPS = %s, peso = %s where cedula = %s', [eps,peso,cedula])
            flash('Paciente actualizado correctamente', 'ok')
        else:
            cur.execute('insert into pacientes (cedula,idEPS,peso) values (%s,%s,%s)', [cedula,eps,peso])
            flash('Paciente creado correctamente', 'ok')
        db.connection.commit()

        cur.execute('select * from historialMedico where idHistorial = %s', [cedula])
        historialMedico = cur.fetchone()

        if historialMedico == None:
            cur.execute('insert into historialMedico (idHistorial,fechaSubida) values (%s, curdate())',[cedula])
            cur.execute('update pacientes set idHistorial = %s where cedula = %s', [cedula, cedula])
            
        db.connection.commit()

    return redirect(url_for('roles.editRoles'))