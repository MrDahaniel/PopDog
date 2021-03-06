from flask import Blueprint, render_template, redirect, url_for, session, flash
from datetime import date
from flask.globals import request
from .__init__ import db

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory')
def inv():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if not role in ["Administrativo", 'Médico', 'Enfermero']:
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))

    cur.execute('call getOrders()')
    ordenes = cur.fetchall()

    cur.execute('select * from item')
    items = cur.fetchall()

    cur.close()

    return render_template('inventario.html', items=items, ordenes=ordenes, role=role)

@inventory.route('/inventory', methods=['POST'])
def invPost():
    idItem = request.form['item']
    cantidad = request.form['cantidad']

    cur = db.connection.cursor()

    cur.execute('call getAdminProfile(%s)',[session['id']])
    idAdministrativo = cur.fetchone()[7];
    
    cur.execute('insert into pedidos (idItem,idAdministrativo,cantidad,fecha) values (%s,%s,%s,%s)', [idItem, idAdministrativo,cantidad,date.today()])
    db.connection.commit()

    flash('orden creada correctamente', 'ok')

    return redirect(url_for('inventory.inv'))

    

@inventory.route('/inventory/recieved')
def recieved():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])
    profileInfo = cur.fetchone()

    if profileInfo[5] != 'Administrativo':
        flash('No se tienen los permisos suficientes para acceder a esta página', 'alert')
        return redirect(url_for('main.index'))
    
    orden = request.args.get('orden')
    item = request.args.get('item')
    cantidad = request.args.get('cantidad')

    cur.execute('delete from pedidos where idPedido = %s', [orden])
    db.connection.commit()
    
    cur.execute('update item set cantidad = cantidad + %s where idItem = %s', [cantidad,item])
    db.connection.commit()

    cur.close()

    flash('Orden completada', 'ok')

    return redirect(url_for('inventory.inv'))

@inventory.route('/inventory/remove', methods=['POST'])
def invRem():
    idItem = request.form['item']
    cantidadARetirar = request.form['cantidad']

    cur = db.connection.cursor()

    cur.execute('select * from item where idItem = %s',  [idItem])
    cantidadInventario = cur.fetchone()[3]

    if int(cantidadInventario) < int(cantidadARetirar):
        flash('La cantidad solicitada es mayor que la cantidad en stock','alert')

    else:
        cur.execute('update item set cantidad = cantidad - %s where idItem = %s', [cantidadARetirar,idItem])
        db.connection.commit()
        flash('Cantidad retirada de inventario satisfactoriamente','ok')

    cur.close()
    
    return redirect(url_for('inventory.inv'))