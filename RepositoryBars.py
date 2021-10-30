import os
from datetime import datetime
from dotenv import load_dotenv

from ClientDB import ClientDB
from PublisherQuery import PublisherQuery
from ClientAlpacaAPI import TimeFrame, ClientAlpacaAPI

load_dotenv()


class RepositoryBars:
    def __init__(
        self,
        user: str = os.getenv('DB_USER'),
        passwd: str = os.getenv('DB_PASSWORD'),
        host: str = os.getenv('DB_HOST'),
        database: str = os.getenv('DB_NAME')
    ) -> None:
        self.cli_db = ClientDB(
            user=user,
            passwd=passwd,
            host=host
        )
        self.cli_alpaca = ClientAlpacaAPI()
        # create database & use
        self.cli_db.cur.execute(f'CREATE DATABASE IF NOT EXISTS {database};')
        self.cli_db.cur.execute(f'USE {database};')
        # create tables
        q_bars = PublisherQuery.create_bars()
        self.cli_db.cur.execute(q_bars)

    def store_bars(
        self,
        timeframe: TimeFrame,
        symbol :str,
        time_start: str,
        time_end: str
    ) -> None:
        payload = self.cli_alpaca.request_bars_payload(
            timeframe=timeframe,
            symbol=symbol,
            time_start=time_start,
            time_end=time_end
        )
        query = PublisherQuery.insert_bars()
        self.cli_db.insert_payload(query, payload)

    def get_latest_time(self, symbol: str, timeframe: TimeFrame) -> datetime:
        query = PublisherQuery.select_bars_latest_time()
        return self.cli_db.fetch_all(query, (timeframe.value, symbol))[0][0]
