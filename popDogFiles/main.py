from flask import Flask, Blueprint, render_template, url_for, redirect

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')
