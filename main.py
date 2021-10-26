from logging import error
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class AgentDB:
    def __init__(
        self,
        user: str = os.getenv('DB_USER'),
        passwd: str = os.getenv('DB_PASSWORD'),
        host: str = os.getenv('DB_HOST')
    ) -> None:
        try:
            # create connection
            self.conn = mysql.connector.connect(
                user=user,
                password=passwd,
                host=host
            )
            self.cur = self.conn.cursor()
            self.conn.autocommit = False
        except (mysql.connector.errors.ProgrammingError) as e:
            error(e)

    def __del__(self) -> None:
        try:
            self.conn.close()
        except (mysql.connector.errors.ProgrammingError) as e:
            error(e)

    def insert_lines(self, query: str, lines: list) -> None:
        # split lines every 500,000 because of restriction memory limit.
        chunk = 500000
        lines_len = len(lines)
        lines_parts = [lines[i:i + chunk] for i in range(0, lines_len, chunk)]
        try:
            for l_part in lines_parts:
                self.cur.executemany(query, l_part)
            self.conn.commit()
        except (mysql.connector.errors.ProgrammingError) as e:
            self.conn.rollback()
            error(e)

class AgentQuery:
    @staticmethod
    def _load_query_from_file(path: str):
        try:
            with open(path, 'r') as f:
                query = f.read()
        except IOError as e:
            error(e)
        return query

    @classmethod
    def create_database(cls):
        path = './sql/create/database.sql'
        return cls._load_query_from_file(path)

if __name__ == '__main__':
    q = AgentQuery.create_database()
    print(q)
    # agent_db = AgentDB()
    # print(agent_db.conn.is_connected())
