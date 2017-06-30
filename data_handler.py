import psycopg2
from database_connection_data import db_con_data
from werkzeug.security import generate_password_hash, check_password_hash
import os
import urllib


def connect_database():
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        # setup connection string
        # connect_str = "dbname={} user={} host='localhost'".format(
        #     db_con_data()['dbname'], db_con_data()['user'])
        # use our connection values to establish a connection
        # conn = psycopg2.connect(connect_str)
        # set autocommit option, to do every query when we call it
        conn.autocommit = True
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        print("Uh oh, can't connect. Invalid dbname, user or password?")
        print(e)

    return cursor, conn


def query_result(*query):
    """Execute SQL query and return the result if it exists.
    Close the connection after execution.
    """
    try:
        cursor, conn = connect_database()
        cursor.execute(*query)
        rows = cursor.fetchall()
        rows = [list(row) for row in rows]
    except psycopg2.OperationalError as e:
        print('OperationalError')
        print(e)
    except psycopg2.ProgrammingError as e:
        print(e)
        print("Nothing to print")
        rows = ""
    except psycopg2.IntegrityError as e:
        print('IntegrityError')
        print(e)
        rows = ""
        raise e from query_result()
    finally:
        if conn:
            conn.close()

    return rows


def add_user_to_db(username, password):
    query_result("""INSERT INTO user_table (user_name, password)
                    VALUES (%s, %s);""", (username, password))


def user_in_db(username, password):
    users = query_result("""SELECT user_name, password FROM user_table;""")
    for user in users:
        if user[0] == username:
            if check_password_hash(user[1], password):
                return True
    return False
