import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from collections import deque

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

    def store_bars_all(
        self,
        timeframe: TimeFrame,
        time_start: str,
        time_end: str
    ) -> None:
        symbols_num = len(Symbol)
        for i, symbol in enumerate(Symbol):
            print(f"Progress: [{i + 1} / {symbols_num}]")
            self.store_bars(
                timeframe=timeframe,
                symbol=symbol,
                time_start=time_start,
                time_end=time_end
            )

    def get_latest_time(self, symbol: Symbol, timeframe: TimeFrame) -> datetime:
        query = PublisherQuery.select_bars_latest_time()
        return self.cli_db.fetch_all(query, (timeframe.value, symbol.value))[0][0]

    def get_df_bars(self, symbol: Symbol, timeframe: TimeFrame) -> pd.DataFrame:
        query = PublisherQuery.select_bars()
        return pd.read_sql(
            query,
            self.cli_db.conn,
            params=(symbol.value, timeframe.value)
        )

    def get_df_bars_relative(self, symbol: Symbol, timeframe: TimeFrame) -> pd.DataFrame:
        """
        Scheme of 'df_bars_relative'
        ---------------------------
        high_bp: float
            basis point of price increase from opening price to high price.
        low_bp: float
            basis point of price decrease from opening price to low price.
        close_bp: float
            basis point of price change from opening price to close price.
        volume: int
            trading volume.
        next_price_movement: int
            relationship between NEXT time's closing price and opening price.
            0: down, 1: up, 2: eq
        """
        df = self.get_df_bars(symbol, timeframe)
        x = []
        for r in df[:-1].itertuples():
            high_bp = ((r.high - r.open) / r.open) * 10000
            low_bp = ((r.low - r.open) / r.open) * 10000
            close_bp = ((r.close - r.open) / r.open) * 10000
            if df.loc[r.Index + 1, 'close'] > df.loc[r.Index + 1, 'open']:
                next_price_movement = 1
            elif df.loc[r.Index + 1, 'close'] < df.loc[r.Index + 1, 'open']:
                next_price_movement = 0
            else:
                next_price_movement = 2
            x.append([high_bp, low_bp, close_bp, r.volume, next_price_movement])
        return pd.DataFrame(
            x,
            columns=['high_bp', 'low_bp', 'close_bp', 'volume', 'next_price_movement'],
            index=df[:-1].time
        )

    def get_df_bars_close_price_movements(self, symbol: Symbol, timeframe: TimeFrame) -> pd.DataFrame:
        """
        Scheme of 'df_bars_close_price_movements'
        --------------------------------
        today: int
            today's price movement compared to 1 days ago.
            [0: down, 1: up, 2: eq]
        ago_1: int
            1 days ago's price movement compared to 2 days ago.
            [0: down, 1: up, 2: eq]
        ago_2: int
            SAME PATTERN AS ABOVE.
        ago_3: int
            SAME PATTERN AS ABOVE.
        tomorrow: int
            tomorrow's price movement compared to today.
            [0: down, 1: up, 2: eq]
        """
        df = self.get_df_bars(symbol, timeframe)
        rows = []
        movements = deque(maxlen=4)
        for r in df[1:-1].itertuples():
            # explanatory variables
            if df.loc[r.Index, 'close'] > df.loc[r.Index - 1, 'close']:
                # up
                movements.append(1)
            elif df.loc[r.Index, 'close'] < df.loc[r.Index - 1, 'close']:
                # down
                movements.append(0)
            else:
                # eq
                movements.append(2)
            # wait completion of pattern
            if len(movements) < 4:
                continue
            # objective variables
            if df.loc[r.Index + 1, 'close'] > df.loc[r.Index, 'close']:
                # up
                movement_tomorrow = 1
            elif df.loc[r.Index + 1, 'close'] < df.loc[r.Index, 'close']:
                # down
                movement_tomorrow = 0
            else:
                # eq
                movement_tomorrow = 2
            rows.append([movements[3], movements[2], movements[1], movements[0], movement_tomorrow])
        return pd.DataFrame(
            rows,
            columns=['today', 'ago_1', 'ago_2', 'ago_3', 'tomorrow'],
            index=df[4:-1].time
        )
