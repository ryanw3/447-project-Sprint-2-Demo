import pandas as pd
from sqlalchemy import create_engine
import db_config
import datetime
import sqlalchemy
import db_utils
import json

reserved_tables = [{db_config.COVID_DATA_TBL_NAME},
                   {db_config.PRISON_DATA_TBL_NAME},
                   {db_config.USER_DB_UPLOADS_TBL_NAME},
                   {db_config.USER_ACCOUNTS_TBL_NAME}]

# Test csv
vaccine_data_csv = "https://data.chhs.ca.gov/dataset/e283ee5a-cf18-4f20-a92c-ee94a2866ccd/resource/130d7ba2-b6eb-438d-a412-741bde207e1c/download/covid19vaccinesbycounty.csv"
vaccine_tbl_name = "main_vaccine_by_cty"
test_user = "TEST_USER_1"

def remove_user_table(rm_table_name: str, requesting_user: str= "NO_USER_SPECIFIED"):
    dbConnection = db_utils.db_connect()
    tn = json.dumps(rm_table_name)
    un = json.dumps(requesting_user)
    result = pd.read_sql(f"SELECT table_name FROM {db_config.USER_DB_UPLOADS_TBL_NAME} where table_name={tn} and username={un};", dbConnection)
    if not result.empty:
        delete_this_table = result['table_name'].tolist()[0]
        dbConnection.execute(f"DROP TABLE IF EXISTS {delete_this_table}")
        dbConnection.execute(f"DELETE FROM {db_config.USER_DB_UPLOADS_TBL_NAME} WHERE table_name={tn}")
        print(f"Success: Deleted Table {delete_this_table}")
        return f"Success: Deleted Table {delete_this_table}"
    else:
        print(f"Invalid delete")
        return f"Invalid delete."

def create_new_table(csv_url: str, new_table_name: str, requesting_user: str="NO_USER_SPECIFIED"):
    # Perhaps check if the url is bad here:
    if new_table_name in reserved_tables:
        print("This table is reserved")
        return "This table is reserved"

    # Connect
    dbConnection = db_utils.db_connect()

    # Check if table is in used_tables
    result = pd.read_sql(f"SELECT table_name FROM {db_config.USER_DB_UPLOADS_TBL_NAME};", dbConnection)
    list_of_used_tables = result['table_name'].tolist()
    if new_table_name in list_of_used_tables:
        # Fail
        print("Error, the table is in use")
        return "Error, the table is in use"
    else:
        # Successful login, return token perhaps?  (SESS_ID token?)
        pass
        # Continue

    try:
        df_new_table = pd.read_csv(csv_url)
    except Exception as e:  # TODO: Actually split the errors, currently it just fails
        return "Error, URL could not be read"

    # Connect
    df_new_table.to_sql(new_table_name, dbConnection, if_exists='replace')

    tn = json.dumps(new_table_name)
    du = json.dumps(csv_url)
    un = json.dumps(requesting_user)

    try:
        result = dbConnection.execute(f"INSERT INTO {db_config.USER_DB_UPLOADS_TBL_NAME}(table_name, data_url, username) "
                                      f"VALUES ({tn}, {du}, {un});")
    except Exception as e: # On fail, rollback
        result = dbConnection.execute(f"DROP TABLE IF EXISTS {new_table_name}")
    dbConnection.close()
    print(f"Success: Table Created: {new_table_name}")  # TODO: Do login work here
    return f"Success, Table Created: {new_table_name}"


if __name__ == "__main__":
    # update_vaccine_data()
    create_new_table(vaccine_data_csv, vaccine_tbl_name, "TEST_USER_1")
    # remove_user_table(vaccine_tbl_name, test_user)
    pass
