import db_config
import db_utils


#########################
# Table initializations


def initialize_user_table() -> None:
    dbConnection = db_utils.db_connect()
    result = dbConnection.execute(f"DROP TABLE IF EXISTS {db_config.USER_ACCOUNTS_TBL_NAME};")
    result = dbConnection.execute(f"CREATE TABLE {db_config.USER_ACCOUNTS_TBL_NAME} ("
                                  f"username varchar(255) NOT NULL,"
                                  f"password varchar(255),"
                                  f"PRIMARY KEY(username)"
                                  f");")
    dbConnection.close()


# covid_user_accounts(username) -> user_db_uploads(username)
# Deleting a username from the accounts table will remove all user tables by a user
def initialize_user_db_uploads() -> None:
    dbConnection = db_utils.db_connect()
    result = dbConnection.execute(f"DROP TABLE IF EXISTS {db_config.USER_DB_UPLOADS_TBL_NAME}")
    result = dbConnection.execute(f"CREATE TABLE {db_config.USER_DB_UPLOADS_TBL_NAME} ("
                                  f"table_name varchar(255) NOT NULL,"
                                  f"data_url varchar(500) NOT NULL,"
                                  f"username varchar(255) NOT NULL,"
                                  f"FOREIGN KEY(username) REFERENCES {db_config.USER_ACCOUNTS_TBL_NAME}(username) ON DELETE RESTRICT"
                                  f");")
    dbConnection.close()


if __name__ == "__main__":
    initialize_user_table()
    initialize_user_db_uploads()