import os
from datetime import datetime
from dotenv import load_dotenv

from services import ClientDB, ClientAlpacaAPI, PublisherQuery
from datatypes import TimeFrame, Symbol

load_dotenv()


class RepositoryBars:
    def __init__(
        self,
        user: str = os.getenv('DB_USER'),
        passwd: str = os.getenv('DB_PASSWORD'),
        host: str = os.getenv('DB_HOST'),
        database: str = os.getenv('DB_NAME'),
        api_key: str = os.getenv('ALPACA_API_KEY'),
        secret_key: str = os.getenv('ALPACA_SECRET_KEY'),
        endpoint_market_data: str = os.getenv('ALPACA_ENDPOINT_MARKET_DATA')
    ) -> None:
        self.cli_db = ClientDB(
            user=user,
            passwd=passwd,
            host=host
        )
        self.cli_alpaca = ClientAlpacaAPI(
            api_key=api_key,
            secret_key=secret_key,
            endpoint_market_data=endpoint_market_data
        )
        # create database & use
        self.cli_db.cur.execute(f'CREATE DATABASE IF NOT EXISTS {database};')
        self.cli_db.cur.execute(f'USE {database};')
        # create tables
        q_bars = PublisherQuery.create_bars()
        self.cli_db.cur.execute(q_bars)

    def store_bars(
        self,
        timeframe: TimeFrame,
        symbol: Symbol,
        time_start: str,
        time_end: str
    ) -> None:
        payload = self.cli_alpaca.request_bars_payload(
            timeframe=timeframe.value,
            symbol=symbol.value,
            time_start=time_start,
            time_end=time_end
        )
        query = PublisherQuery.insert_bars()
        self.cli_db.insert_payload(query, payload)

    def get_latest_time(self, symbol: Symbol, timeframe: TimeFrame) -> datetime:
        query = PublisherQuery.select_bars_latest_time()
        return self.cli_db.fetch_all(query, (timeframe.value, symbol.value))[0][0]
