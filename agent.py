import os
import requests
from dotenv import load_dotenv
from typing import List, Optional
from enum import Enum

from assistant import AccesorDB, PublisherQuery

load_dotenv()


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
        q_bars = PublisherQuery.create_table_bars()
        self.acr_db.cur.execute(q_bars)


class TimeFrame(Enum):
    MIN_1 = '1Min'
    MIN_15 = '15Min'
    HOUR_1 = '1Hour'
    DAY_1 = '1Day'


class AgentAlpacaApi:
    def __init__(
        self,
        api_key: str = os.getenv('ALPACA_API_KEY'),
        secret_key: str = os.getenv('ALPACA_SECRET_KEY'),
        endpoint_market_data: str = os.getenv('ALPACA_ENDPOINT_MARKET_DATA')
    ) -> None:
        self.endpoint_market_data = endpoint_market_data
        self.auth_header = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }

    def request_bars_part(
        self,
        timeframe: TimeFrame,
        symbol: str,
        time_start: str,
        time_end: str,
        page_token: Optional[str] = None
    ) -> dict:
        url = f"{self.endpoint_market_data}/stocks/{symbol}/bars"
        query = {
            'start': time_start,
            'end': time_end,
            'timeframe': timeframe.value,
            'limit': 10000
        }
        if page_token is not None:
            query['page_token'] = page_token
        r = requests.get(
            url,
            headers=self.auth_header,
            params=query
        )
        return r.json()

    def request_bars(
        self,
        timeframe: TimeFrame,
        symbol: str,
        time_start: str,
        time_end: str,
    ) -> List[dict]:
        next_page_token = None
        bars_all = []
        while True:
            bars = self.request_bars_part(
                timeframe,
                symbol,
                time_start,
                time_end,
                next_page_token
            )
            # temporary solution to the problem the return value of bars may be None.
            if bars['bars'] is not None:
                bars_all.extend(bars['bars'])
            next_page_token = bars['next_page_token']
            if next_page_token is None:
                break
        return bars_all

    def request_bars_payload(
        self,
        timeframe: TimeFrame,
        symbol: str,
        time_start: str,
        time_end: str,
    ) -> List[tuple]:
        bars = self.request_bars(
            timeframe,
            symbol,
            time_start,
            time_end
        )
        return list(map(lambda bar: ((
            timeframe.value,
            symbol,
            bar['t'],
            bar['o'],
            bar['h'],
            bar['l'],
            bar['c'],
            bar['v']
        )), bars))
