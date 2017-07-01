import psycopg2
from database_connection_data import db_con_data
from werkzeug.security import generate_password_hash, check_password_hash


def connect_database():
    try:
        connect_str = "dbname={} user={} host='localhost'".format(
            db_con_data()['dbname'], db_con_data()['user'])
        conn = psycopg2.connect(connect_str)
        conn.autocommit = True
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
    """Add the given username and 
       password to the database"""
    query_result("""INSERT INTO user_table (user_name, password)
                    VALUES (%s, %s);""", (username, password))


def user_in_db(username, password):
    """Returns True if the given username exists
       and has the same password as in the argument"""
    users = query_result("""SELECT user_name, password FROM user_table;""")
    for user in users:
        if user[0] == username:
            if check_password_hash(user[1], password):
                return True
    return False
