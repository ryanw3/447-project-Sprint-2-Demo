import os
import db_installation_script
os.system(f"apt install python3-pip")
os.system(f"python3 -m pip install sqlalchemy")
os.system(f"python3 -m pip install pandas")
os.system(f"python3 -m pip install flask")
os.system(f"python3 -m pip install Werkzeug")
os.system(f"python3 -m pip install datetime")
os.system(f"python3 -m pip install pymysql")

db_installation_script.full_install()