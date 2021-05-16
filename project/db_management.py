import db_utils
import json
import db_config
import pandas as pd


# Drops all tables given a list (WARNING: WILL DROP ANY TABLE, ADMIN ONLY)
def admin_drop_all_tables_in_list(list_of_table_names: list) -> None:
    dbConnection = db_utils.db_connect()
    for item in list_of_table_names:
        item_parsed = json.dumps(item)
        result = dbConnection.execute(f"DROP TABLE IF EXISTS {item}")
        result = dbConnection.execute(f"DELETE FROM {db_config.USER_DB_UPLOADS_TBL_NAME} WHERE table_name={item_parsed}")
    dbConnection.close()


# Get all user added tables created by username "username"
def admin_get_user_tables_by_un(username: str) -> list:
    dbConnection = db_utils.db_connect()
    username_parsed = json.dumps(username)
    # Check if table is in used_tables
    result = pd.read_sql(f"SELECT table_name FROM {db_config.USER_DB_UPLOADS_TBL_NAME} where username={username_parsed};",
                         dbConnection)
    dbConnection.close()
    return result['table_name'].tolist()


# Lists all user added tables
def admin_get_all_user_tables() -> list:
    dbConnection = db_utils.db_connect()
    # Check if table is in used_tables
    result = pd.read_sql(f"SELECT table_name FROM {db_config.USER_DB_UPLOADS_TBL_NAME};", dbConnection)
    dbConnection.close()
    return result['table_name'].tolist()


# Drops every user added table
def admin_drop_all_user_tables() -> None:
    list_of_user_tables = admin_get_all_user_tables()
    admin_drop_all_tables_in_list(list_of_user_tables)


# Drops all user tables created by "username"
def admin_drop_all_user_tables_by_un(username: str) -> None:
    tables_to_drop = admin_get_user_tables_by_un(username=username)
    admin_drop_all_tables_in_list(list_of_table_names=tables_to_drop)


# WARNING: THIS ATTEMPTS TO DELETE ALL USER ACCOUNTS
def admin_drop_all_user_accounts() -> None:
    dbConnection = db_utils.db_connect()
    dbConnection.execute(f"delete from {db_config.USER_ACCOUNTS_TBL_NAME}")


if __name__ == "__main__":
    tables = ["delme_1", "delme_2", "delme_3"]
    admin_drop_all_user_tables()
    print(admin_get_all_user_tables())