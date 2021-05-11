import pandas as pd
from sqlalchemy import create_engine
import secrets_ignore
import datetime
import sqlalchemy

blacklist = []

used_tables = ["main_prison_data", "main_covid_data"]

# Test csv
vaccine_data_csv = "https://data.chhs.ca.gov/dataset/e283ee5a-cf18-4f20-a92c-ee94a2866ccd/resource/130d7ba2-b6eb-438d-a412-741bde207e1c/download/covid19vaccinesbycounty.csv"
vaccine_tbl_name = "main_vaccine_by_cty"

def remove_from_blacklist(blacklist_url: str):
    if blacklist_url not in blacklist:
        blacklist.remove(blacklist_url)
        return f"Successfully removed {blacklist_url} from blacklist"
    else:
        return f"{blacklist_url} does not exist in blacklist"

def add_to_blacklist(blacklist_url: str):
    if blacklist_url not in blacklist:
        blacklist.append(blacklist_url)
        return f"Successfully added {blacklist_url} to blacklist"
    else:
        return f" Table {blacklist_url} already exists in  blacklist"

def remove_table_restriction(table_name: str):
    if table_name in used_tables:
        used_tables.remove(table_name)
        return f"Successfully removed table {table_name}"
    else:
        return f"Table {table_name} does not exist in blacklist."

def update_vaccine_data(csv_url:str, table_name: str):
    # Perhaps check if the url is bad here:
    if csv_url in blacklist:
        return "Error, this URL is not allowed"
    df_new_table = pd.read_csv(csv_url)

    if table_name in used_tables:
        return "Error, the table is in use"

    # Connect
    engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    send_new_df = df_new_table.to_sql(table_name, dbConnection, if_exists='replace')
    # print(f"ALTER TABLE {vaccine_tbl_name} DROP COLUMN index;")
    # dbConnection.execute(f"ALTER TABLE {vaccine_tbl_name} DROP COLUMN index;")
    dbConnection.close()


# def join_vaccine_covid():
#     engine_string = 'mysql+pymysql://' + secrets_ignore.user + ":" + secrets_ignore.password + "@" + secrets_ignore.ip_endpoint + "/" + secrets_ignore.db_name
#     engine = create_engine(engine_string)
#     dbConnection = engine.connect()
#     dbConnection.execute("CREATE VIEW joint_vaccine_covid AS SELECT 'index' id1 FROM main_vaccine_by_cty A "
#                          "LEFT JOIN main_covid_data B "
#                          "ON A.county = B.county and A.administered_date = B.date;")
#     dbConnection.close()

# def drop_indx():


if __name__ == "__main__":
    update_vaccine_data()

    # join_vaccine_covid()