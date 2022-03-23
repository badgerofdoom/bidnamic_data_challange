import psycopg2
import sqlalchemy


class Database:
    def __init__(self, db_name: str, db_host: str, db_port: int) -> None:
        self.name: str = db_name
        self.host: str = db_host
        self.port: int = db_port
        self.connection = None

    def connect(self, db_user: str, db_password: str) -> bool:
        try:
            self.connection = psycopg2.connect(
                database=self.name, user=db_user, password=db_password, host=self.host, port=self.port)
            return True
        except:
            return False

    def disconnect(self) -> None:
        self.connection.close()
        self.connection = None

    def get_connection_string(self, db_user: str, db_password: str) -> str:
        conn_string: str = f'postgresql://{db_user}:{db_password}@{self.host}:{self.port}/{self.name}'
        return conn_string

    def create_db_enigine(self, db_user: str, db_password: str):
        engine = sqlalchemy.create_engine(
            self.get_connection_string(db_user, db_password))
        return engine
