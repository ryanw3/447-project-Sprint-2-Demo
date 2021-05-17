import requests
import db_config
import db_utils
import db_logger
import db_table_initializers
import db_update_database
import db_update_more_databases
import database_queries_covid
import database_queries_users as database_queries_users
import random
import string

#######################
# Test URLs
vaccine_data_csv = "https://data.chhs.ca.gov/dataset/e283ee5a-cf18-4f20-a92c-ee94a2866ccd/resource/130d7ba2-b6eb-438d-a412-741bde207e1c/download/covid19vaccinesbycounty.csv"
vaccine_tbl_name = "main_vaccine_by_cty"


#######################
# Testing
def generate_user():
    test_user_un = ''.join(random.choice(string.printable) for i in range(100))
    test_user_pw = ''.join(random.choice(string.printable) for i in range(60))
    return test_user_un, test_user_pw


def perform_user_tests():
    # Generate random unique username & passwords
    test_user_1_un, test_user_1_pw = generate_user()
    test_user_2_un, test_user_2_pw = generate_user()

    while test_user_1_un == test_user_2_un or test_user_1_pw == test_user_2_pw:
        test_user_1_un, test_user_1_pw = generate_user()
        test_user_2_un, test_user_2_pw = generate_user()

    # Test valid
    res = database_queries_users.insert_user(username=test_user_1_un, password=test_user_1_pw)
    if res !=
    res = database_queries_users.insert_user(username=test_user_2_un, password=test_user_2_pw)

    # Test invalid
    database_queries_users.query_user(username=test_user_1_un, password=test_user_2_pw)
    database_queries_users.query_user(username=test_user_2_un, password=test_user_1_pw)

    # Test delete (Failed deletes - invalid username, invalid password)
    test_fail_un, _ = generate_user()
    database_queries_users.delete_user(username=test_fail_un, password=test_user_1_pw)
    database_queries_users.delete_user(username=test_user_1_un, password=test_user_2_pw)

    # Test delete (Successful deletes - user 1 & user 2
    database_queries_users.delete_user(username=test_user_1_un, password=test_user_1_pw)
    database_queries_users.delete_user(username=test_user_2_un, password=test_user_2_pw)


def db_main_url_tests():
    test_1 = requests.get(db_config.MAIN_COVID_DATA_URL)
    if test_1.status_code != 200:
        db_logger.log_message("Test 1 Failed: Could not reach Main COVID County Data URL")
    test_2 = requests.get(db_config.MAIN_PRISON_DATA_URL)
    if test_2.status_code != 200:
        db_logger.log_message("Test 2 Failed: Could not reach Main COVID Prison Data URL")



if __name__ == "__main__":
    # print(query_user_tests())
    perform_user_tests()
    # create_user_test()
    #  db_main_url_tests()
