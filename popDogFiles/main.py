from flask import Flask, Blueprint, render_template, url_for, redirect, session

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    return render_template('index.html', session=session)

@main.route('/profile')
def profile():
    return render_template('profile.html')
