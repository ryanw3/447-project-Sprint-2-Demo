import pandas as pd
from sqlalchemy import create_engine
import secrets_ignore
import datetime
import sqlalchemy
import code
import os
import sys

dtype_covid_data = {
	"date": sqlalchemy.types.DATE,
        "county": sqlalchemy.types.VARCHAR(length=50),
        "state": sqlalchemy.types.VARCHAR(length=50),
        "fips": sqlalchemy.types.INT,
        "cases": sqlalchemy.types.INT,
	"death": sqlalchemy.types.INT
}

dtype_prison_data = {
	"facility_id" : sqlalchemy.types.INT,
	"jurisdiction" : sqlalchemy.types.VARCHAR(length=50),
	"prison_name" : sqlalchemy.types.VARCHAR(length=50),
	"source" : sqlalchemy.types.VARCHAR(length=500),
	"residents_confirmed" : sqlalchemy.types.INT,
	"staff_confirmed" : sqlalchemy.types.INT,
	"staff_confirmed" : sqlalchemy.types.INT,
	"residents_death" : sqlalchemy.types.INT,
    "staff_death" : sqlalchemy.types.INT,
    "residents_recovered" : sqlalchemy.types.INT,
    "staff_recovered" : sqlalchemy.types.INT,
    "residents_tadmin" : sqlalchemy.types.INT,
    "staff_tested" : sqlalchemy.types.INT,
    "residents_negative" : sqlalchemy.types.INT,
    "staff_negative" : sqlalchemy.types.INT,
    "residents_pending" : sqlalchemy.types.INT,
    "staff_pending" : sqlalchemy.types.INT,
    "residents_quarantine" : sqlalchemy.types.INT,
    "staff_quarantine" : sqlalchemy.types.INT,
    "residents_active" : sqlalchemy.types.INT,
    "population_feb20" : sqlalchemy.types.INT,
    "residents_population" : sqlalchemy.types.INT,
    "residents_tested" : sqlalchemy.types.INT,
    "residents_initiated" : sqlalchemy.types.INT,
    "residents_completed" : sqlalchemy.types.INT,
    "residents_vadmin" : sqlalchemy.types.INT,
    "staff_initiated" : sqlalchemy.types.INT,
    "staff_completed" : sqlalchemy.types.INT,
    "staff_vadmin" : sqlalchemy.types.INT,
    "address" : sqlalchemy.types.VARCHAR(length=100),
    "zipcode" : sqlalchemy.types.INT,
    "city" : sqlalchemy.types.VARCHAR(length=20),
    "county" : sqlalchemy.types.INT,
    "latitude" : sqlalchemy.types.FLOAT,
    "longitude" : sqlalchemy.types.FLOAT,
    "county_fips" : sqlalchemy.types.INT,
    "hifld_id" : sqlalchemy.types.INT,
    "jurisdiction_scraper" : sqlalchemy.types.VARCHAR(length=20),
    "description" : sqlalchemy.types.VARCHAR(length=20),
    "security" : sqlalchemy.types.VARCHAR(length=20),
    "age" : sqlalchemy.types.VARCHAR(length=10),
    "is_different_operator" : sqlalchemy.types.BOOLEAN,
    "different_operator" : sqlalchemy.types.VARCHAR(length=20),
    "capacity" : sqlalchemy.types.VARCHAR(length=50),
    "bjs_id" : sqlalchemy.types.VARCHAR(length=50),
    "source_population_feb20" : sqlalchemy.types.VARCHAR(length=50),
    "source_capacity" : sqlalchemy.types.VARCHAR(length=50),
	"website" : sqlalchemy.types.VARCHAR(length=500),
	"ice_field_office" : sqlalchemy.types.VARCHAR(length=50)
}

def update_from_link(link:str, renames: dict, table_name: str):
    df = pd.read_csv(link)
    if renames is not False:
        df.rename(columns=renames)


def update():
    main_covid_data = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    main_prison_data = "https://raw.githubusercontent.com/uclalawcovid19behindbars/historical-data/main/data/CA-historical-data.csv"

    # Extra opendata tables (json backends)
    non_prison_county_hospitalization = "https://data.ca.gov/api/3/action/datastore_search?resource_id=0d9be83b-5027-41ff-97b2-6ca70238d778"

    df_covid = pd.read_csv(main_covid_data)
    df_prison = pd.read_csv(main_prison_data)
    df_full_cty_hosp = pd.read_json(non_prison_county_hospitalization)
    df_full_cty_hosp.rename(columns={"todays_date": "date"})

    # Main tables
    covid_table_name = "main_covid_data"
    prison_table_name = "main_prison_data"

    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # TODO: REMOVE INTERACTIVE TESTING WHEN READY
    # console = code.InteractiveConsole(dict(globals(), **locals()))
    # console.interact('Interactive shell for %s' %
    #                  os.path.basename(sys.argv[0]))

    # Deduplication
    df_covid.drop_duplicates(subset=['county', 'date'], keep='last')

    # Automated update
    send_frame_covid = df_covid.to_sql(covid_table_name, dbConnection, if_exists='replace', dtype=dtype_covid_data)
    send_frame_prison = df_prison.to_sql(prison_table_name, dbConnection, if_exists='replace', dtype=dtype_prison_data)
    # Close conn
    dbConnection.close()
    pass

def update_geojson():
    prison_geojson_url = "https://opendata.arcgis.com/datasets/ee98a8bdd0994597b322220909525dd4_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D"
    df_prison_geojson = pd.read_csv(prison_geojson_url)
    tb_name_prison_geojson = "prison_geojson_ca"

    # Setup engine
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # Exec
    send_frame_covid = df_prison_geojson.to_sql(tb_name_prison_geojson, dbConnection, if_exists='replace')
    dbConnection.close()
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Read data from site
    update()
    #update_geojson()
    print("Hello world")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/