import sys,os
os.system(f"apt install python3-pip")
os.system(f"python3 -m pip install sqlalchemy")
os.system(f"python3 -m pip install pandas")
os.system(f"python3 -m pip install flask")
os.system(f"python3 -m pip install Werkzeug")
os.system(f"python3 -m pip install datetime")
os.system(f"python3 -m pip install pymysql")
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path) 
import db_installation_script
db_installation_script.full_install()