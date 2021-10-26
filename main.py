from logging import error
import mysql.connector
import os
from dotenv import load_dotenv

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError

load_dotenv()


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
            error(e)

    def __del__(self) -> None:
        try:
            self.conn.close()
        except ProgrammingError as e:
            error(e)


class PublisherQuery:
    @staticmethod
    def _load_query_from_file(path: str):
        try:
            with open(path, 'r') as f:
                query = f.read()
        except IOError as e:
            error(e)
        return query

    @classmethod
    def create_database(cls) -> str:
        path = './sql/create/database.sql'
        return cls._load_query_from_file(path)

    @classmethod
    def create_table_bars_1min(cls) -> str:
        path = './sql/create/bars_1min.sql'
        return cls._load_query_from_file(path)

    @classmethod
    def create_table_bars_1day(cls) -> str:
        path = './sql/create/bars_1day.sql'
        return cls._load_query_from_file(path)


class AgentDB:
    def __init__(
        self,
        user: str = os.getenv('DB_USER'),
        passwd: str = os.getenv('DB_PASSWORD'),
        host: str = os.getenv('DB_HOST'),
        database: str = os.getenv('DB_NAME')
    ) -> None:
        # db accesor
        self.acr_db = AccesorDB(
            user=user,
            passwd=passwd,
            host=host
        )
        # create database & use
        self.acr_db.cur.execute(f'CREATE DATABASE IF NOT EXISTS {database};')
        self.acr_db.cur.execute(f'USE {database};')
        # create tables
        q_bars_1min = PublisherQuery.create_table_bars_1min()
        q_bars_1day = PublisherQuery.create_table_bars_1day()
        self.acr_db.cur.execute(q_bars_1min)
        self.acr_db.cur.execute(q_bars_1day)


if __name__ == '__main__':
    agent_db = AgentDB(database='foo')
