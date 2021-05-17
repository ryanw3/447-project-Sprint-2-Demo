import sqlalchemy
import db_config
import pymysql.cursors


# db_connect - Logs in with the main user
def db_connect(ret_engine=False):
    engine_string = 'mysql+pymysql://' + db_config.user + ":" + db_config.password + "@" + db_config.ip_endpoint + "/" + db_config.db_name
    engine = sqlalchemy.create_engine(engine_string)
    dbConnection = engine.connect()
    if not ret_engine:
        return dbConnection
    else:
        return dbConnection, engine

# load_table - Loads proper into var
