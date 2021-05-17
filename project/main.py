from flask import Blueprint, render_template,request,url_for, session, redirect, flash
import pandas as pd
import os
import db_update_more_databases
import database_queries_covid
from datetime import datetime , timedelta  
main = Blueprint('main', __name__)
from werkzeug.utils import secure_filename

@main.route('/')
def index():
    date=datetime.today()
    date=date.strftime('%Y-%m-%d')
    countyData=database_queries_covid.get_latest_update_covid(date)
    prisonData=database_queries_covid.get_latest_update_prison(date)
    countyData=countyData.to_json(orient="split")
    prisonData=prisonData.to_json(orient="split")
    return render_template('index.html', data=countyData,prisonData=prisonData, date=date, loggedin=checkLogin())

@main.route('/',methods=['POST'])
def index_post():
    date= request.form.get('date')
    countyData=database_queries_covid.get_latest_update_covid(date)
    prisonData=database_queries_covid.get_latest_update_prison(date)
    prisonData=prisonData.to_json(orient="split")
    countyData=countyData.to_json(orient="split")
    return render_template('index.html', data=countyData, prisonData=prisonData, date=date, loggedin=checkLogin())

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/help')
def help():
    return render_template('about.html')

@main.route('/send_California_County_Boundaries')
def send_California_County_Boundaries():
    return "<a href=%s>file</a>" % url_for('static', filename='json/California_County_Boundaries.geojson')

@main.route('/send_CA_Prison_Boundaries')
def send_CA_Prison_Boundaries():
    return "<a href=%s>file</a>" % url_for('static', filename='json/CA_Prison_Boundaries.geojson')

@main.route('/send_bg.png')
def send_bg():
    return "<a href=%s>file</a>" % url_for('templates', filename='images/bg.png')

@main.route('/send_criminal_justice_facility.png')
def send_criminal_justice_facility():
    return "<a href=%s>file</a>" % url_for('templates', filename='images/criminal_justice_facility.png')

@main.route('/send_colors.png')
def send_colors():
    return "<a href=%s>file</a>" % url_for('templates', filename='images/colors.png')

@main.route('/send_home_button.png')
def send_home_button():
    return "<a href=%s>file</a>" % url_for('templates', filename='images/home_button.png')

@main.route('/send_question_mark.png')
def send_question_mark():
    return "<a href=%s>file</a>" % url_for('templates', filename='images/question_mark.png')

@main.route('/database')
def database():
    if(session['loggedin'] == True):
        return render_template('database.html')
    else:
        return render_template('index.html')

@main.route('/database',methods=['POST'])
def database_post():
    name = request.form.get('name')
    file = request.files['file']
    filename = secure_filename(file.filename)
    if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
    path = os.path.join('project/uploads', filename)
    file.save(path)
    db_update_more_databases.create_new_table(path, name)
    flash('File added to database')
    return redirect(url_for('main.index'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'

def checkLogin():
    return session["loggedin"]