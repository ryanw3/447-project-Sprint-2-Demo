from flask_login import login_required, current_user
from flask import Blueprint, render_template,request
from . import db
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
sys.path.append("/home/ryan/Desktop/tracker/447-project-Sprint-2-Demo/project/")
import secrets_ignore

main = Blueprint('main', __name__)

def query_state(return_type,date):
    '''user = 'db_user'
    password = 'test_db_pw'
    pool_recycle = '3600'
    db_name = 'covid_data'
    ip_endpoint = '127.0.0.1'''
    
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
    return return_this

@main.route('/')
def index():
    test=query_state("dataframe","'2020-01-28'")
    print(test, file=sys.stdout)
    return render_template('index.html')

@main.route('/',methods=['POST'])
def index_post():
    date= request.form.get('date')
    #test=query_state("dataframe","'2020-01-28'")
    datestr="'"+date+"'"
    #print(datestr, file=sys.stdout)
    theData=query_state("datafame",datestr)
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