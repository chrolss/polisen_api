from sqlalchemy import create_engine


class postgresql():
    def __init__(self, database, credentials_path):
        self.database = database
        self.credentials_path = credentials_path
        self.username, self.password, self.ip = self.get_credentials()

    def get_credentials(self):
        key_file_path = self.credentials_path
        keys = []
        with open(key_file_path) as file:
            keys = file.read().splitlines()

        sql_username = keys[0]
        sql_password = keys[1]
        ip = keys[2]

        return sql_username, sql_password, ip

    def create_connection(self):
        engine_path = 'mssql+pyodbc://' + self.username + ':' + self.password + '@' + self.ip + '\\SQLEXPRESS/' + self.database + '?driver=SQL+Server'
        engine = create_engine(engine_path)
        connection = engine.connect()

        return engine
