# init_db.py

import pymysql

# Initialize connection with server
conn = pymysql.connect(
    host="localhost",
    user="mike",
    password="5454160s"
)

# Database cursor
curs = conn.cursor()

curs.execute("DROP DATABASE IF EXISTS my_db")
curs.execute("CREATE DATABASE IF NOT EXISTS my_db")
curs.execute("use my_db")

curs.execute("DROP TABLE IF EXISTS posts")
curs.execute('''
                CREATE TABLE IF NOT EXISTS posts (
                    post_id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)''')

curs.execute("DROP TABLE IF EXISTS comments")
curs.execute('''CREATE TABLE IF NOT EXISTS comments(
             comment_id INT PRIMARY KEY AUTO_INCREMENT,
             comment TEXT NOT NULL,
             created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
             post_id INT NOT NULL,
             FOREIGN KEY (post_id) REFERENCES posts(post_id))''')

# Commit and close the database connection
conn.commit()
conn.close()
