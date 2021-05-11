from flask_login import login_required, current_user
from flask import Blueprint, render_template,request,url_for
from . import db
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
sys.path.append("/home/ryan/Desktop/tracker/447-project-Sprint-2-Demo/project/")
import secrets_ignore
import database_queries_covid

@main.route('/')
def index():
    searchedDate = "'2021-01-28'"
    data=database_queries_covid.prepare_two(return_type="dataframe",
                prepname="cov_read",
                tbl_name="main_covid_data",
                where_clause="where state=? AND date=?",
                var_a='"California"',
                var_b=searchedDate)
    theData=data.to_json(orient="split")
    prisonData=database_queries_covid.prepare_one(return_type="dataframe",
                prepname="prison_data",
                tbl_name="main_prison_data",
                where_clause="where date=?",
                var_a=searchedDate)
    print(prisonData)
    prisonData=prisonData.to_json(orient="split")
    #print(data, file=sys.stdout)
    return render_template('index.html', data=theData,prisonData=prisonData)

@main.route('/',methods=['POST'])
def index_post():
    date= request.form.get('date')
    datestr="'"+date+"'"
    print(datestr)
    countyData=database_queries_covid.prepare_two(return_type="dataframe",
                prepname="cov_read",
                tbl_name="main_covid_data",
                where_clause="where state=? AND date=?",
                var_a='"California"',
                var_b=datestr)
    prisonData=database_queries_covid.prepare_one(return_type="dataframe",
                prepname="prison_data",
                tbl_name="main_prison_data",
                where_clause="where date=?",
                var_a=datestr)
    prisonData=prisonData.to_json(orient="split")
    #theData=query_state("datafame",datestr)
    #print(theData, file=sys.stdout)
    theData=theData.to_json(orient="split")
    print(prisonData, file=sys.stdout)
    return render_template('index.html', data=countyData, prisonData=prisonData)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/data')
@login_required
def showData(date):
    return render_template()

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