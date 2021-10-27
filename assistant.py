import mysql.connector

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError


class AccesorDB:
    def __init__(
        self,
        user: str,
        passwd: str,
        host: str
    ) -> None:
        try:
            # create connection
            self.conn: MySQLConnection = mysql.connector.connect(
                user=user,
                password=passwd,
                host=host
            )
            self.cur: MySQLCursor = self.conn.cursor()
            self.conn.autocommit = False
        except ProgrammingError as e:
            print(e)

    def __del__(self) -> None:
        try:
            self.conn.close()
        except ProgrammingError as e:
            print(e)


class PublisherQuery:
    @staticmethod
    def _load_query_from_file(path: str) -> str:
        try:
            with open(path, 'r') as f:
                query = f.read()
        except IOError as e:
            print(e)
        return query

    @classmethod
    def create_table_bars(cls) -> str:
        path = './sql/create/bars.sql'
        return cls._load_query_from_file(path)

    @classmethod
    def insert_bars(cls) -> str:
        path = './sql/insert/bars.sql'
        return cls._load_query_from_file(path)
