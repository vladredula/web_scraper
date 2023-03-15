from psycopg2 import connect
from psycopg2 import OperationalError

def print_psycopg2_exception(err):
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    

def create_database(dbname):
    sql = f'CREATE DATABASE {dbname}'
    
def create_table(tname, fields, pkey):
    sql = f'CREATE TABLE {tname} ('

    # check if the table already exist
    if table_exists(tname):
        return

    for count, (column, attribute) in enumerate(fields.items()):
        sql += column+' '+attribute.upper()

        if attribute == pkey:
            sql += ' PRIMARY KEY'

        if count+1 < len(fields):
            sql += ', '
    
    sql += ') '


    try:
        cursor.execute(sql)
    except Exception as err:
        # pass exception to function
        print(err)

    conn.commit()

    # check if the table was successfully created
    if not table_exists(tname):
        print('Error: unable to create table')


def table_exists(tname):
    sql = f"SELECT EXISTS (SELECT FROM pg_catalog.pg_tables WHERE tablename = '{tname}')"
    cursor.execute(sql)
    return cursor.fetchone()[0]

try:
    conn = connect(
        dbname = "postgres",
        user = "postgres",
        host = "localhost",
        password = "password",
        port = '5432'
    )
except OperationalError as err:
    # pass exception to function
    print_psycopg2_exception(err)

    # set the connection to 'None' in case of error
    conn = None

# if the connection was successful
if conn != None:
    # declare a cursor object from the connection
    cursor = conn.cursor()

    # execute a PostgreSQL command to get all rows in a table
    # returns 'psycopg2.errors.InFailedSqlTransaction' if rollback() not called
    try:
        cursor.execute('SELECT current_database()')
    except Exception as err:
        # pass exception to function
        print(err)

    table = 'sample'
    columns = {
        'id':'int',
        'name':'varchar'
    }
    pkey = 'id'

    create_table(table, columns,pkey)

    # close the cursor object to avoid memory leaks
    cursor.close()
    

