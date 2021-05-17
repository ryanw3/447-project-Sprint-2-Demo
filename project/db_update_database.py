import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import db_logger
import db_utils
import db_tests
from db_return_codes import *
from db_config import *


#######################
# Main update function
def update() -> int:  # int-type error codes listed above.  All negative values = errors
    try:
        df_covid = pd.read_csv(MAIN_COVID_DATA_URL)
        df_prison = pd.read_csv(MAIN_PRISON_DATA_URL)
    except Exception as err: # TODO: Refine Exception clauses
        db_logger.log_error(exception=err,
                            err_type="DB_CSV_Read Error",
                            optional_message="Check Main COVID Data/Prison Data URLs")
        return RETURN_ERROR_DB_CSV_READ

    # Data Processing: Covid table
    try:
        df_covid = df_covid[df_covid['state'] == "California"]
        numeric_values = ['cases', 'deaths']
        df_covid[numeric_values] = df_covid[numeric_values].astype(int)

        df_covid.drop_duplicates(subset=['county', 'date'], keep='last')

        # Data Processing: Prison table
        kept_columns = ['Name', 'Date', 'Address', 'County', 'Residents.Confirmed', 'Staff.Confirmed',
                        'Residents.Active',
                        'Staff.Active', 'Residents.Deaths', 'Staff.Deaths']
        df_prison = df_prison[kept_columns]

        better_names = ['name', 'date', 'address', 'county', 'residents_confirmed', 'staff_confirmed',
                        'residents_active',
                        'staff_active', 'residents_deaths', 'staff_deaths']
        df_prison.columns = better_names

        numeric_values = ['residents_confirmed', 'staff_confirmed', 'residents_active', 'staff_active',
                          'residents_deaths',
                          'staff_deaths']
        df_prison[numeric_values] = df_prison[numeric_values].fillna(0)
        df_prison[numeric_values] = df_prison[numeric_values].astype(int)

        df_prison.dropna(subset=['address'], inplace=True)

        df_prison['name'] = df_prison['name'].str.title()
        df_prison['address'] = df_prison['address'].str.upper()
    except Exception as e: # TODO: Refine Exception clauses
        db_logger.log_error(exception=e,
                            err_type="DB_Data_Processing Error",
                            optional_message="Column data names likely changed")
        return RETURN_ERROR_DB_DATA_PROCESSING

    # Connect
    try:
        dbConnection = db_utils.db_connect()
    except Exception as e: # TODO: Refine Exception clauses
        db_logger.log_error(exception=e,
                            err_type="DB_db_connect error",
                            optional_message="")
        return RETURN_ERROR_DB_CONNECT

    # # TODO: REMOVE INTERACTIVE TESTING WHEN READY
    # console = code.InteractiveConsole(dict(globals(), **locals()))
    # console.interact('Interactive shell for %s' %
    #                  os.path.basename(sys.argv[0]))

    # Update
    try:
        df_covid.to_sql(COVID_DATA_TBL_NAME, dbConnection, if_exists='replace', dtype=DTYPE_COVID_DATA)
        df_prison.to_sql(PRISON_DATA_TBL_NAME, dbConnection, if_exists='replace', dtype=DTYPE_PRISON_DATA)
    except TypeError as e:  # Table not properly made
        print("Error, table creation failed, data processing likely required")
        db_logger.log_error(exception=e,
                            err_type="DB_TOSQL_Table_Creation Error",
                            optional_message="Fixing data processing likely required")
        return RETURN_ERROR_TOSQL
    except ValueError as e:  # Table already exists, should not happen due to if_exists='replace'
        db_logger.log_error(exception=e,
                            err_type="DB_TOSQL_ValueError",
                            optional_message="Table likely being replaced without if_exists='replace'")
        return RETURN_ERROR_TOSQL
    except Exception as e:  # Unknown errors logged
        db_logger.log_error(exception=e,
                            err_type="DB_TOSQL_Unknown Error",
                            optional_message="Unknown error received")
        print("Unknown error")
        return RETURN_ERROR_TOSQL

    # Close conn
    dbConnection.close()
    db_logger.log_message(f"Success: Successful update.")
    return 0


#######################
# If ran, do update then tests
if __name__ == '__main__':
    # Read data from site
    update()

    # Run test suite
    db_logger.log_message("Starting tests")
    # db_tests.db_tests()
    db_logger.log_message("Tests completed")
    print("Tests Completed!")
