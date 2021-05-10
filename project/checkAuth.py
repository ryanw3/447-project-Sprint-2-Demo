from sqlalchemy import create_engine
import pymysql
import pandas as pd
import secrets_ignore
# Set UN/PW

# Global error codes
# Insert PW
ERRNO_PW_EXISTS = -1
# Query User
ERROR_USER_DNE = -2

def initialize_user_table(): # Run as admin please
    engine_string = 'mysql+pymysql://' + \
                    secrets_ignore.user + ":" + \
                    secrets_ignore.password + "@" + \
                    secrets_ignore.ip_endpoint + "/" + \
                    secrets_ignore.db_name
    engine = create_engine(engine_string)
    dbConnection = engine.connect()
    result = dbConnection.execute("CREATE TABLE covid_user_accounts ("
                                  "username varchar(255),"
                                  "password varchar(64)"
                                  ");")
    dbConnection.close()
    return 0

def insert_user(username, password):
    # Error message
    ERROR_MESSAGE = "Sorry, this username has been taken"

    # Query
    engine_string = 'mysql+pymysql://' + \
                    secrets_ignore.user + ":" + \
                    secrets_ignore.password + "@" + \
                    secrets_ignore.ip_endpoint + "/" + \
                    secrets_ignore.db_name
    print(engine_string)
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # Setup
    stmt = "SET @a = \'" + username + "\';"
    print(stmt)
    result = dbConnection.execute(stmt)
    stmt = "SET @b = \'" + password + "\';"
    result = dbConnection.execute(stmt)
    print(stmt)
    # Query if UN exists
    #result = dbConnection.execute(f"SELECT * from covid_user_accounts where username=\"{username}\";")
    #print(f"The result: {result}")
    #
    result = dbConnection.execute("PREPARE cov_att_login from 'SELECT * from covid_user_accounts where username=?;';")
    result = pd.read_sql("EXECUTE cov_att_login using @a;", dbConnection)
    # If the UN exists, fail
    fail = True
    if result.empty:
        fail = False
    if fail:
        print(ERROR_MESSAGE)
        dbConnection.close()
        return ERRNO_PW_EXISTS

    # If UN DNE, set UN/PW
    print("Here")
    result = dbConnection.execute("INSERT INTO covid_user_accounts(username, password) VALUES (@a,@b)")
    # dbConnection.execute(
    #     "PREPARE cov_insert_user from 'INSERT INTO covid_user_accounts (username, password) VALUES (?,?);';")
    # result = dbConnection.execute("EXECUTE cov_insert_user using @a, @b;")
    dbConnection.close()
    return 1


# Get UN/PW
def query_user(username, password):
    engine_string = 'mysql+pymysql://' + \
                    secrets_ignore.user + ":" + \
                    secrets_ignore.password + "@" + \
                    secrets_ignore.ip_endpoint + "/" + \
                    secrets_ignore.db_name
    print(engine_string)
    engine = create_engine(engine_string)
    dbConnection = engine.connect()

    # Query
    stmt = "SET @a = \'" + username + "\';"
    result = dbConnection.execute(stmt)
    stmt = "SET @b = \'" + password + "\';"
    result = dbConnection.execute(stmt)

    # Query for username and password match
    result = dbConnection.execute(
        "PREPARE cov_att_login from 'SELECT * from covid_user_accounts where username=? AND password=?;';")
    result = pd.read_sql("EXECUTE cov_att_login using @a, @b;", dbConnection)
    print("Uhh T1")
    if result.empty:
        # Failed login, return error
        print("Uhh T2")
        dbConnection.close()
        return ERROR_USER_DNE
    else:
        # Successful login, return token perhaps?  (SESS_ID token?)
        print("Uhh T3")
        print("Remove me when this is completed")  # TODO: Do login work here
    print("T4")
    dbConnection.close()
    return 1

if __name__ == "__main__":
    print("RC: " + str(insert_user("AA", "AA")))