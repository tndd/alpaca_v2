import requests
import time
from dotenv import load_dotenv
from typing import List, Optional
from datetime import datetime

from datatypes import TimeFrame

load_dotenv()


class ClientAlpacaAPI:
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        endpoint_market_data: str
    ) -> None:
        self.endpoint_market_data = endpoint_market_data
        self.auth_header = {
            "APCA-API-KEY-ID": api_key,
            "APCA-API-SECRET-KEY": secret_key
        }
        self.request_limit_per_sec = 3.4

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
        print(f"symbol: {symbol}, timeframe: {timeframe.value}")
        while True:
            # scice there is a limit to the number of api request.
            # so time measurement is necessary to limit the number of times sent request.
            time_start_request = datetime.now()
            bars = self.request_bars_part(
                timeframe,
                symbol,
                time_start,
                time_end,
                next_page_token
            )
            elasped_time_request = datetime.now() - time_start_request
            # wait for escape api request limit
            time_too_early = self.request_limit_per_sec - elasped_time_request.total_seconds()
            if time_too_early > 0:
                time.sleep(time_too_early)
            # temporary solution to the problem the return value of bars may be None.
            if bars['bars'] is not None:
                bars_all.extend(bars['bars'])
            next_page_token = bars['next_page_token']
            if next_page_token is None:
                print('request is completed.')
                break
            print('.', end='', flush=True)
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
            datetime.strptime(bar['t'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S'),
            bar['o'],
            bar['h'],
            bar['l'],
            bar['c'],
            bar['v']
        )), bars))
