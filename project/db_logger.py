import os
import db_config
import uuid

#######################
# Log write location
LOG_LOCATION = db_config.LOG_LOCATION
LOG_LOCATION_TESTS = db_config.LOG_LOCATION_DB_TESTS


# Error logging function, DEP: uuid
def log_error(exception, err_type, optional_message="", output_location=LOG_LOCATION) -> None:
    with open(output_location, 'a') as f:
        err_uuid = uuid.uuid1()  # Device + Timestamp in one
        f.write(f"ERROR: {err_uuid} :"
                f"{err_type}: {optional_message}. :\n"
                f"Exception: {exception}\n"
                f"END_ERROR: {err_uuid}\n")


def log_message(message, output_location=LOG_LOCATION) -> None:
    with open(output_location, 'a') as f:
        msg_uuid = uuid.uuid1()
        f.write(f"MESSAGE: {msg_uuid} {message} END_MESSAGE: {msg_uuid}\n")