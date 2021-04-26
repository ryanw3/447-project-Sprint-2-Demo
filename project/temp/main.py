import pandas as pd
from sqlalchemy import create_engine
import secrets_ignore


def update():
    main_covid_data = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
    main_prison_data = "https://raw.githubusercontent.com/uclalawcovid19behindbars/historical-data/main/data/CA-historical-data.csv"
    df_covid = pd.read_csv(main_covid_data)
    df_prison = pd.read_csv(main_prison_data)

    covid_table_name = "main_covid_data"
    prison_table_name = "main_prison_data"
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    send_frame_covid = df_covid.to_sql(covid_table_name, dbConnection, if_exists='replace')
    send_frame_prison = df_prison.to_sql(prison_table_name, dbConnection, if_exists='replace')

    # Close conn
    dbConnection.close()
    return


if __name__ == '__main__':
    # Read data from site
    update()
    print("Hello world")
