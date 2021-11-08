import pandas as pd


def make_df_bars_bars_relative(df_bars: pd.DataFrame) -> pd.DataFrame:
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
        x = []
        for r in df_bars[:-1].itertuples():
            high_bp = ((r.high - r.open) / r.open) * 10000
            low_bp = ((r.low - r.open) / r.open) * 10000
            close_bp = ((r.close - r.open) / r.open) * 10000
            if df_bars.loc[r.Index + 1, 'close'] > df_bars.loc[r.Index + 1, 'open']:
                next_price_movement = 1
            elif df_bars.loc[r.Index + 1, 'close'] < df_bars.loc[r.Index + 1, 'open']:
                next_price_movement = 0
            else:
                next_price_movement = 2
            x.append([high_bp, low_bp, close_bp, r.volume, next_price_movement])
        return pd.DataFrame(
            x,
            columns=['high_bp', 'low_bp', 'close_bp', 'volume', 'next_price_movement'],
            index=df_bars[:-1].time
        )
