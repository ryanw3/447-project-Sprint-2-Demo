import sqlalchemy # For the proper sqlalchemy types
from db_gen_secret import *  # Add in the secrets (user, password, ip endpoint)

#######################
# Connection - Main DB user
pool_recycle = '3600'
db_name = 'covid_data'

#######################
# Logging
LOG_LOCATION = "./db.log"
LOG_LOCATION_DB_TESTS = "./db_test.log"

#######################
# Table names
COVID_DATA_TBL_NAME = "main_covid_data"
PRISON_DATA_TBL_NAME = "main_prison_data"
USER_DB_UPLOADS_TBL_NAME = "user_db_uploads"
USER_ACCOUNTS_TBL_NAME = "covid_user_accounts"

#######################
# Source Data URLs
MAIN_COVID_DATA_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
MAIN_PRISON_DATA_URL = "https://raw.githubusercontent.com/uclalawcovid19behindbars/historical-data/main/data/CA-historical-data.csv"

#######################
# Defined Data Types for Managed Tables
DTYPE_COVID_DATA = {
    "date": sqlalchemy.types.DATE,
    "county": sqlalchemy.types.VARCHAR(length=50),
    "state": sqlalchemy.types.VARCHAR(length=50),
    "fips": sqlalchemy.types.INT,
    "cases": sqlalchemy.types.INT,
    "death": sqlalchemy.types.INT
}

DTYPE_PRISON_DATA = {
    "name": sqlalchemy.types.VARCHAR(length=50),
    "date": sqlalchemy.types.DATE,
    "address": sqlalchemy.types.VARCHAR(length=100),
    "county": sqlalchemy.types.VARCHAR(length=100),
    "residents_confirmed": sqlalchemy.types.INT,
    "staff_confirmed": sqlalchemy.types.INT,
    "residents_active": sqlalchemy.types.INT,
    "staff_active": sqlalchemy.types.INT,
    "residents_death": sqlalchemy.types.INT,
    "staff_deaths": sqlalchemy.types.INT,
}