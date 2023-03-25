import psycopg2


class DB_connector:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname, 
                user=self.user,
                password=self.password, 
                host=self.host, 
                port=self.port
            )

            self.cursor = self.conn.cursor()
            print('Successfully connected to Database')

        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def execute_query(self, query, params = []):
        try:
            self.cursor.execute(query, params)
            print("Query executed successfully")
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def close_connection(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Connection closed")