from flask import Blueprint, render_template, url_for, session,redirect
from .__init__ import db

information = Blueprint('information', __name__)

@information.route('/information')
def infobay():
    if not session:
        return redirect(url_for('auth.login'))

    cur = db.connection.cursor()
    cur.execute('call getRole(%s)', [session['id']])
    role = cur.fetchone()[0]

    if not role in ['Médico', 'Enfermero', 'Paciente']:
        return redirect(url_for('main.index'))

    return render_template('infobay.html',role=role)