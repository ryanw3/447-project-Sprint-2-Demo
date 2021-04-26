from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required
import sys
sys.path.append("/home/ryan/Desktop/tracker/447-project-Sprint-2-Demo/project/")
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
    print("Test")
    if checkAuth.query_user(username, password):
        user = User(username=username, name="Temp", password=password) #generate_password_hash(password, method='sha256'))
        login_user(user.get_id())
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    '''
    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=false)
    '''
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username= request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if checkAuth.insert_user(username, password):
        new_user = User(username=username, name=name, password=password)#generate_password_hash(password, method='sha256'))
    else:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))
    #user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database
    '''if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    '''
    return redirect(url_for('auth.login'))
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))