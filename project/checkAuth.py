from sqlalchemy import create_engine
import sqlalchemy
import pymysql
import pandas as pd
import db_config
import db_utils
import db_return_codes
import db_logger


def insert_user(username: str, password: str):
    meta = sqlalchemy.MetaData()
    dbConnection, engine = db_utils.db_connect(ret_engine=True)
    user_accounts = sqlalchemy.Table(db_config.USER_ACCOUNTS_TBL_NAME, meta, autoload_with=engine)
    ins = user_accounts.insert().values(username=username, password=password)
    try:
        result = dbConnection.execute(ins)
        if not result:
            return db_return_codes.UNHANDLED_ERROR
    except sqlalchemy.exc.IntegrityError as e:
        print(f"Attempted DB Creation of Duplicate username {username}")
        db_logger.log_error(e, "Warning: Attempted DB Creation of Duplicate User Name")
        return db_return_codes.UA_INSERT_FAILED_DUPLICATE
    print(f"User Accounts: Creation of username {username} successful.")
    db_logger.log_message(f"User Accounts: Creation of username {username} successful.")
    return db_return_codes.UA_INSERT_SUCCESS


def delete_user(username: str, password: str):
    # Check if the password is valid
    result = query_user(username=username, password=password)
    if result == db_return_codes.UA_LOGIN_SUCCESS:
        # Delete
        meta = sqlalchemy.MetaData()
        dbConnection, engine = db_utils.db_connect(ret_engine=True)
        user_accounts = sqlalchemy.Table(db_config.USER_ACCOUNTS_TBL_NAME, meta, autoload_with=engine)
        try:
            dbConnection.execute(user_accounts.delete().where(user_accounts.c.username == username))
            if not result:
                print("Error: Unhandled DB Exception -- delete_user (No Result)")
                return db_return_codes.UNHANDLED_ERROR
        except Exception as e:
            print("Error: Unhandled DB Exception -- delete_user")
            db_logger.log_error(e, "Error: Unhandled DB Exception -- delete_user")
            return db_return_codes.UNHANDLED_ERROR
        db_logger.log_message(f"User Accounts: Deletion of username {username} successful")
        print(f"Deletion of user {username} successful")
        return db_return_codes.UA_DELETE_USER_SUCCESS
    else:
        print("Delete User: Login Failed, cannot delete without valid un/pw")
        return db_return_codes.UA_DELETE_USER_FAILED


def query_user(username: str, password: str):
    meta = sqlalchemy.MetaData()
    dbConnection, engine = db_utils.db_connect(ret_engine=True)
    user_accounts = sqlalchemy.Table(db_config.USER_ACCOUNTS_TBL_NAME, meta, autoload_with=engine)
    s = sqlalchemy.select(user_accounts.c.username).where(
        sqlalchemy.and_(user_accounts.c.username == username, user_accounts.c.password == password))
    try:
        result = dbConnection.execute(s)
        if not result:
            return db_return_codes.UNHANDLED_ERROR
    except sqlalchemy.exc.IntegrityError as e:
        db_logger.log_error(e, "Error: DB SELECT Failed")
        return db_return_codes.UA_ERROR_SELECT_FAILED

    if result.rowcount == 0:  # If it doesn't match, it doesn't exist
        # Return false
        print(f"Login Failed, returning {db_return_codes.UA_LOGIN_FAILED}")
        return db_return_codes.UA_LOGIN_FAILED
    else:
        print(f"login Success, returning {db_return_codes.UA_LOGIN_SUCCESS}")
        return db_return_codes.UA_LOGIN_SUCCESS

def get_user_hash(username: str) -> tuple:
    meta = sqlalchemy.MetaData()
    dbConnection, engine = db_utils.db_connect(ret_engine=True)
    user_accounts = sqlalchemy.Table(db_config.USER_ACCOUNTS_TBL_NAME, meta, autoload_with=engine)
    s = sqlalchemy.select(user_accounts).where(user_accounts.c.username == username)
    try:
        result = dbConnection.execute(s)
        if not result:
            return db_return_codes.UNHANDLED_ERROR, 0
    except sqlalchemy.exc.IntegrityError as e:
        db_logger.log_error(e, "Error: DB SELECT Failed")
        return db_return_codes.UA_ERROR_SELECT_FAILED, 0
    if result.rowcount == 0:  # If it doesn't match, it doesn't exist
        # Return false
        #  print(f"Login Failed, returning {db_return_codes.UA_LOGIN_FAILED}")
        return db_return_codes.UA_LOGIN_FAILED, 0
    elif result.rowcount == 1:  # Execute
        username, password = result.fetchone()
    else:
        #  print(f"login Success, returning {db_return_codes.UA_LOGIN_SUCCESS}")
        return db_return_codes.UNHANDLED_ERROR
    return db_return_codes.UA_QUERY_SUCCESS, password

if __name__ == "__main__":
    pass
