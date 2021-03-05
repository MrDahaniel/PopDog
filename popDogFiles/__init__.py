from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

db = MySQL()

def createApp():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'thisisaverysecurekeylmaoplsdontstealthisthx'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'popdogdb'

    db.init_app(app)

    app.static_folder = 'static'

    from .auth import auth as authBlueprint
    app.register_blueprint(authBlueprint)

    from .main import main as mainBlueprint
    app.register_blueprint(mainBlueprint)

    from .userhandle import userhandle as userhandleBlueprint
    app.register_blueprint(userhandleBlueprint)

    from .dashboard import dashboard as dashboardBlueprint
    app.register_blueprint(dashboardBlueprint)

    from .roles import roles as rolesBlueprint
    app.register_blueprint(rolesBlueprint)

    from .search import search as searchBlueprint
    app.register_blueprint(searchBlueprint)

    from .location import location as locationBlueprint
    app.register_blueprint(locationBlueprint)

    from .inventory import inventory as inventoryBlueprint
    app.register_blueprint(inventoryBlueprint)

    from .maintenance import maintenance as maintenanceBlueprint
    app.register_blueprint(maintenanceBlueprint)

    from .patients import patients as patientsBlueprint
    app.register_blueprint(patientsBlueprint)

    return app
