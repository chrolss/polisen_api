from sqlalchemy import create_engine


class postgresql():
    def __init__(self, database, credentials_path):
        self.database = database
        self.credentials_path = credentials_path
        self.username, self.password, self.ip, self.dbtype, self.driver = self.get_credentials()

    def get_credentials(self):
        key_file_path = self.credentials_path
        keys = []
        with open(key_file_path) as file:
            keys = file.read().splitlines()

        sql_username = keys[0]
        sql_password = keys[1]
        ip = keys[2]
        dbtype = keys[3]
        driver = keys[4]

        return sql_username, sql_password, ip, dbtype, driver

    def create_connection(self):
        if self.dbtype == 'mssql':
            engine_path = 'mssql+pyodbc://' + self.username + ':' + self.password + '@' + self.ip + '\\SQLEXPRESS/' + self.database + '?driver=SQL+Server'
        elif self.dbtype == 'postgresql':
            engine_path = 'postgresql+pg8000://' + self.username + ':' + self.password + '@' + self.ip + '/' + self.database
        else:
            print("unknown db type")
            return False

        engine = create_engine(engine_path)
        connection = engine.connect()

        return engine
