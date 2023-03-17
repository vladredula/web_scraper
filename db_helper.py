def create_database(dbname):
    sql = f'CREATE DATABASE {dbname}'

    return sql

    
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

    return sql


def table_exists(tname):
    sql = f"SELECT EXISTS (SELECT FROM pg_catalog.pg_tables WHERE tablename = '{tname}')"
    
    return sql

def truncate_table(tname):
    sql = f"TRUNCATE {tname}"

    return sql
    

