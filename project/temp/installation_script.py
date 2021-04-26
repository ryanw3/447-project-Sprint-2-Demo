import os
os.system("sudo apt install mariadb-server")
os.system("sudo mysql_install_db --user=mysql")
os.system("sudo systemctl start mariadb.service")
