# config.py

import pymysql

username = 'mike'
password = '5454160s'
hostname = 'localhost'
db_name = 'books_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}/{db_name}"
