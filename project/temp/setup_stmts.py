import pandas as pd
from sqlalchemy import create_engine
import pymysql
import secrets_ignore

def setup_stmt():
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    result = dbConnection.execute("SET @a = 'California';")
    result = dbConnection.execute("PREPARE cov_read from 'SELECT * from main_covid_data where state=? limit 0,10;';")
    result2 = dbConnection.execute("EXECUTE cov_read USING @a;")

    for v in result2:
        for column, value in v.items():
            print(f"{column}: {value}")

    print(result)
    # Close conn
    dbConnection.close()
    return

# Setup
if __name__ == "__main__":
    setup_stmt()
