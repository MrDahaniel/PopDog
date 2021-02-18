from flask import Flask, Blueprint, render_template, url_for, redirect

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def loginPost():
    return "owo"

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signupPost():
    return "uwu"

@auth.route('/logout')
def logout():
    return redirect(url_for('main.index'))