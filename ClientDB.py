from dotenv import load_dotenv
from typing import List, Any, Union
import mysql.connector

from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector.errors import ProgrammingError

load_dotenv()


class ClientDB:
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

    def insert_payload(self, query: str, payload: List[tuple]) -> None:
        # split lines every 500,000 because of restriction memory limit.
        chunk = 500000
        lines_len = len(payload)
        print(f"insert lines num: {lines_len}")
        payloads_separated = [payload[i:i + chunk] for i in range(0, lines_len, chunk)]
        for payload in payloads_separated:
            self.cur.executemany(query, payload)
        self.conn.commit()

    def fetch_all(self, query: str, params: tuple) -> Union[Any, list]:
        self.cur.execute(query, params)
        return self.cur.fetchall()
