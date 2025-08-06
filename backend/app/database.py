import pymysql
from pymysql.cursors import DictCursor

def get_connection():
    connection = pymysql.connect(
        host="switchback.proxy.rlwy.net",
        port=46119,
        user="root",
        password="TMUNvjuUBiNTpmPjdRuWQcWUYFIcrLRA",
        database="railway",
        cursorclass=DictCursor
    )
    return connection
