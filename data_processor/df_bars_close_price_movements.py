import pandas as pd
from collections import deque


def get_df_bars_close_price_movements(
        df_bars: pd.DataFrame,
        back_range: int = 3
    ) -> pd.DataFrame:
        """
        Params
            back_range: int
                how many previous close price to look back on.
        ------------------------------------------------------

        Scheme of 'df_bars_close_price_movements'
            today: int
                today's price movement compared to 1 days ago.
                [0: down, 1: eq, 2: up]
            ago_{back_range}: int
                {back_range} days ago's price movement compared to {back_range + 1} days ago.
                [0: down, 1: eq, 2: up]

            ...

            tomorrow: int
                tomorrow's price movement compared to today.
                [0: down, 1: eq, 2: up]
        """
        rows = []
        movements = deque(maxlen=(back_range + 1))
        # create column names of df_bars_close_price_movements
        columns_agos = [f"ago_{i}" for i in range(1, (back_range + 1))]
        columns = ['today'] + columns_agos + ['tomorrow']
        # make rows from df_bars
        for r in df_bars[1:-1].itertuples():
            # explanatory variables
            if df_bars.loc[r.Index, 'close'] > df_bars.loc[r.Index - 1, 'close']:
                # up
                movements.append(2)
            elif df_bars.loc[r.Index, 'close'] < df_bars.loc[r.Index - 1, 'close']:
                # down
                movements.append(0)
            else:
                # eq
                movements.append(1)
            # wait completion of pattern
            if len(movements) < (back_range + 1):
                continue
            # objective variables
            if df_bars.loc[r.Index + 1, 'close'] > df_bars.loc[r.Index, 'close']:
                # up
                movement_tomorrow = 2
            elif df_bars.loc[r.Index + 1, 'close'] < df_bars.loc[r.Index, 'close']:
                # down
                movement_tomorrow = 0
            else:
                # eq
                movement_tomorrow = 1
            # append movements to rows
            row = [movements[i] for i in reversed(range((back_range + 1)))]
            row.append(movement_tomorrow)
            rows.append(row)
        return pd.DataFrame(
            rows,
            columns=columns,
            index=df_bars[(back_range + 1):-1].time
        )
