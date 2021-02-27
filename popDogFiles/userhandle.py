from flask import Flask, Blueprint, render_template, url_for, redirect, session, request
from flask.helpers import flash
from werkzeug.security import check_password_hash, generate_password_hash
from .__init__ import db

userhandle = Blueprint('userhandle', __name__, template_folder='templates', static_folder='static')

@userhandle.route('/profile/edit')
def editProfile():
    if not session:
        return redirect(url_for('auth.login', session=session))

    cur = db.connection.cursor()
    cur.execute('call getProfile(%s)', [session['id']])

    profileInfo = cur.fetchone()

    cur.close()

    return render_template('selfedit.html', profileInfo=profileInfo)

@userhandle.route('/profile/edit',methods=['POST'])
def editProfilePost():

    name = request.form['name']
    fecha = request.form['fecha']
    sexo = request.form['sexo']
    phone = request.form['phone']
    password = request.form['password']
    
    cur = db.connection.cursor()
    cur.execute('call getHashPass(%s)', [session['id']])

    profileInfo = cur.fetchone()[0]

    if check_password_hash(profileInfo,password): #If true, means passwords good. update fields in database
        cur.execute('call updateProfile(%s,%s,%s,%s,%s)', [session['id'], name, fecha, sexo, phone])
        db.connection.commit()
        flash('Perfil ha sido actualizado correctamente', 'ok')
        cur.close()
        session['username'] = name
        return redirect(url_for('main.profile'))

    flash('La contraseña no es correcta, intente nuevamente', 'alert')
    cur.close()

    return redirect(url_for('userhandle.editProfile'))