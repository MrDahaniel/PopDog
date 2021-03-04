from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask.globals import request
from .__init__ import db

maintenance = Blueprint('maintenance', __name__)

@maintenance.route('/maintenance/main')
def maintenanceMain():
    if not session:
        return redirect(url_for('auth.login'))
    
    cur = db.connection.cursor()

    cur.execute('call getRole(%s)', [session['id']])
    
    if not cur.fetchone()[0] in ['Administrativo', 'Ingeniero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('call getMOByStatus(%s)',[False])
    pendientes = cur.fetchall()

    cur.execute('call getMOByStatus(%s)',[True])
    completados = cur.fetchall()

    cur.execute('select p.nombre, i.idIngeniero from perfiles as p inner join ingenieros as i on p.cedula = i.cedula')
    ingenieros = cur.fetchall()

    cur.execute('call getAllEquipment()')
    equipos = cur.fetchall()

    return render_template('mantenimientoBase.html',pendientes=pendientes,completados=completados,ingenieros=ingenieros,equipos=equipos)

@maintenance.route('/maintenance/create', methods=['POST'])
def maintenanceCreate():
    ingeniero = request.form['ingeniero']
    equipo = request.form['equipo']

    cur = db.connection.cursor()
    cur.execute('insert into ordenMantenimiento (idEquipo,idIngeniero) values (%s,%s)', [equipo,ingeniero])
    cur.connection.commit()

    flash('Orden creada satisfactoriamente', 'ok')
    
    return redirect(url_for('maintenance.maintenanceMain'))
    
@maintenance.route('/maintenance/complete')
def maintenanceComplete():
    if not session:
        return redirect(url_for('auth.login'))
    
    cur = db.connection.cursor()

    cur.execute('call getRole(%s)', [session['id']])
    
    if not cur.fetchone()[0] in ['Administrativo', 'Ingeniero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('update ordenMantenimiento set ordenCompletada = true where idOrdenMantenimiento = %s', [request.args.get('orden')])

    cur.connection.commit()

    return redirect(url_for('maintenance.maintenanceMain'))