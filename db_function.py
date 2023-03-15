import psycopg2

def print_psycopg2_exception(err):
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    

def create_database(dbname):
    sql = f'CREATE DATABASE {dbname}'

    execute_query(sql)

    
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

    # execute the structured sql
    execute_query(sql)

    # check if the table was not successfully created
    if not table_exists(tname):
        print('Error: unable to create table')


def table_exists(tname):
    sql = f"SELECT EXISTS (SELECT FROM pg_catalog.pg_tables WHERE tablename = '{tname}')"
    return execute_query(sql)


def execute_query(sql):

    # return false if the passed string is empty
    if sql == '':
        return False
    
    try:
        cursor.execute(sql)
    except psycopg2.OperationalError as err:
        print_psycopg2_exception(err)

    # commit the changes to the database
    conn.commit()

    # get all the results from the query statement
    result = cursor.fetchall()

    # close the cursor object to avoid memory leaks
    cursor.close()
    conn.close()

    return result

try:
    conn = psycopg2.connect(
        dbname = "postgres",
        user = "postgres",
        host = "localhost",
        password = "password",
        port = '5432'
    )
except psycopg2.OperationalError as err:
    # pass exception to function
    print_psycopg2_exception(err)

    # set the connection to 'None' in case of error
    conn = None

# if the connection was successful
if conn != None:
    # declare a cursor object from the connection
    cursor = conn.cursor()

    # execute a simple PostgreSQL command to get the current datebase name
    try:
        cursor.execute('SELECT current_database()')
    except Exception as err:
        # pass exception to function
        print_psycopg2_exception(err)
    

