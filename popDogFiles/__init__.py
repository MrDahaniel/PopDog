from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

def createApp():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisisaverysecurekeylmaoplsdontstealthisthx'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'testo'
    mysql = MySQL(app)

    app.static_folder = 'static'

    from .auth import auth as authBlueprint
    app.register_blueprint(authBlueprint)

    from .main import main as mainBlueprint
    app.register_blueprint(mainBlueprint)

    return app
