from sqlalchemy import create_engine
import pymysql
import pandas as pd
import secrets_ignore

def prepare_one(return_type: str, prepname: str, tbl_name: str, where_clause: str, var_a: str):
    engine_string = 'mysql+pymysql://' + \
                    secrets_ignore.user + ":" + \
                    secrets_ignore.password + "@" + \
                    secrets_ignore.ip_endpoint + "/" + \
                    secrets_ignore.db_name
    print(engine_string)
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # Set variable :: Ex: varA = "'2020-04-07'"
    setup = "SET @a = " + str(var_a) + ";"
    print(setup)
    result = dbConnection.execute(setup)

    # Do query
    result = dbConnection.execute(
        "PREPARE " + str(prepname) + " from 'SELECT * from " + str(tbl_name) + " where date=?;';"
    )
    covid_data_df = pd.read_sql("EXECUTE " + str(prepname) + " using @a;", dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    if return_type == "csv":
        return_this = covid_data_df.to_csv()
    elif return_type == "print":
        print(covid_data_df.to_csv())
        print(covid_data_df)
        return 0
    else:
        return_this = covid_data_df
    dbConnection.close()
    return return_this

def prepare_two(return_type: str, prepname: str, tbl_name: str, where_clause: str, var_a: str, var_b):
    engine_string = 'mysql+pymysql://' + \
                    secrets_ignore.user + ":" + \
                    secrets_ignore.password + "@" + \
                    secrets_ignore.ip_endpoint + "/" + \
                    secrets_ignore.db_name
    print(engine_string)
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # Set variable :: Ex: varA = "'2020-04-07'"
    setup = "SET @a = " + str(var_a) + ";"
    print(setup)
    result = dbConnection.execute(setup)

    # Set variable :: Ex: var_b =
    setup = "SET @b = " + str(var_b) + ";"
    print(setup)
    result = dbConnection.execute(setup)

    # Do query
    result = dbConnection.execute(
        "PREPARE " + str(prepname) + " from 'SELECT * from " + str(tbl_name) + " " + str(where_clause) + ";';"
    )
    covid_data_df = pd.read_sql("EXECUTE " + str(prepname) + " using @a, @b;", dbConnection)
    pd.set_option('display.expand_frame_repr', False)
    if return_type == "csv":
        return_this = covid_data_df.to_csv()
    elif return_type == "print":
        print(covid_data_df.to_csv())
        print(covid_data_df)
        return 0
    else:
        return_this = covid_data_df
    dbConnection.close()
    return return_this

def deduplicate():
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    dbConnection.execute("")
# Setup
if __name__ == "__main__":
    prepare_two(return_type="print",
                prepname="prison_data",
                tbl_name="main_vaccine_by_cty",
                where_clause="where county=? and administered_date=? limit 10",
                var_a='"Alameda"',
                var_b="'2020-12-15'")  # Note, dates must be like "'2020-04-07'"


