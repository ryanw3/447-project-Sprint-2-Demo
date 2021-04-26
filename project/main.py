from flask_login import login_required, current_user
from flask import Blueprint, render_template,request,url_for
from . import db
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
sys.path.append("/home/ryan/Desktop/tracker/447-project-Sprint-2-Demo/project/")
import secrets_ignore

main = Blueprint('main', __name__)

def query_state(return_type,date):    
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    #engine_string = 'mysql+pymysql://' + user + ":" + password + "@" + ip_endpoint + "/" + db_name
    print(engine_string)
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    searchedDate = date
    result = dbConnection.execute("SET @a = 'California';")
    setup = "SET @b = " + searchedDate + ";"
    print(setup)
    result = dbConnection.execute(setup)
    result = dbConnection.execute("PREPARE cov_read from 'SELECT * from main_covid_data where state=? AND date=? limit 0,10;';")
    covid_data_df = pd.read_sql("EXECUTE cov_read using @a, @b;", dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    if return_type == "csv":
        return_this = covid_data_df.to_csv()
    elif return_type == "print":
        print(covid_data_df.to_csv())
        print(covid_data_df)
        return 0
    else:
        return_this = covid_data_df
    #print(return_this)
    return return_this

@main.route('/')
def index():
    searchedDate = "'2021-01-28'"
    data=query_state("dataframe",searchedDate)
    theData=data.to_json(orient="split")
    print(data, file=sys.stdout)
    return render_template('index.html', data=theData)

@main.route('/',methods=['POST'])
def index_post():
    date= request.form.get('date')
    #test=query_state("dataframe","'2020-01-28'")
    datestr="'"+date+"'"
    print(datestr)
    theData=query_state("datafame",datestr)
    print(theData, file=sys.stdout)
    theData=theData.to_json(orient="split")
    print(theData, file=sys.stdout)
    return render_template('index.html', data=theData)

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