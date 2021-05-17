from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
#import sys
#sys.path.append("/home/ryan/Desktop/tracker/447-project-Sprint-2-Demo/project/")
import db_return_codes
import checkAuth
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    print("Login")
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    #email = request.form.get('email')
    username= request.form.get('User')
    password = request.form.get('password')
    #remember = True if we are able to login
    #password=generate_password_hash(password, method='sha256')
    #password=
    print(password)
    retcode, db_pass = get_user_hash(username)
    if retcode == db_return_codes.UA_QUERY_SUCCESS:
        if check_password_hash(db_pass,password)==True:
            session['loggedin'] = True
            session['username'] = username
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username= request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password = password=generate_password_hash(password, method='sha256')
    print(password)
    if checkAuth.insert_user(username, password)==db_return_codes.UA_INSERT_SUCCESS:
        #new_user = User(username=username, name=name, password=password)#generate_password_hash(password, method='sha256'))
        redirect(url_for('auth.login'))
    else:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    return redirect(url_for('auth.login'))
    
@auth.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('main.index'))