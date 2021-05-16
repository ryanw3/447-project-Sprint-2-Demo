# Please run this as the root user
import os
import json

confirms = ["Y", "y", "Yes", "yes"]
denys = ["N", "n", "No", "no"]


def setup_secret_file():
    # Defaults
    user = 'db_user'
    password = 'test_db_pw'
    ip_endpoint = '127.0.0.1:3306'

    # Generate secret file
    user_next = False
    while user_next is not True:
        user = str(input("Please set a db user name:") or user)
        password = str(input("Please set a db user password:") or password)
        ip_endpoint = str(input("Please set an IP endpoint:") or ip_endpoint)
        user = json.dumps(user)
        password = json.dumps(password)
        ip_endpoint = json.dumps(ip_endpoint)
        form = f"user = {user}\n" + \
               f"password = {password}\n" + \
               f"ip_endpoint = {ip_endpoint}\n"
        res = input(f"Looks good? (Y/N?)\n" + form)
        if res in confirms:
            with open('db_gen_secret.py', "w") as f:
                f.write(form)
            user_next = True


# Sets up database
def setup_database():
    import db_config
    un = json.dumps(db_config.user)
    pw = json.dumps(db_config.password)
    os.system(f"apt install mariadb-server")
    os.system(f"mysql_secure_installation")
    os.system(f"mariadb -u root -e 'CREATE USER {un} IDENTIFIED BY {pw}; "
              f"CREATE DATABASE covid_data; "
              f"GRANT ALL PRIVILEGES on covid_data.* to {un}; "
              f"FLUSH PRIVILEGES;'")
    pass

# Sets up prereqs
def setup_prereqs():
    os.system(f"apt install python3-pip")
    os.system(f"python3 -m pip install sqlalchemy")
    os.system(f"python3 -m pip install numpy")
    os.system(f"python3 -m pip install pandas")
    os.system(f"python3 -m pip install PyMySQL")
    os.system(f"python3 -m pip install PyMySQL[ed25519]")

# Full installation
def full_install():
    response = input(f"Do you want to generate a db_gen_secret file?")
    if response in confirms:
        setup_secret_file()
    response = input(f"Do you want to set up the prereqs?")
    if response in confirms:
        setup_prereqs()
    response = input(f"Do you want to set up the database?")
    if response in confirms:
        setup_database()


if __name__ == "__main__":
    full_install()
