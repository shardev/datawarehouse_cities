import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

# [database]
DB_HOST =  parser.get('database', 'db_host')
DB_USER =  parser.get('database', 'db_user')
DB_PASSWORD =  parser.get('database', 'db_password')
DB_PORT =  parser.get('database', 'db_port')
DB_NAME =  parser.get('database', 'db_name')

# [env]
URL =  parser.get('env', 'url')
