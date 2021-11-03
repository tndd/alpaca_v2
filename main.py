import pandas as pd
from RepositoryBars import RepositoryBars
from datatypes import TimeFrame
from datatypes.Symbol import Symbol
from sklearn.tree import DecisionTreeClassifier


def test_convert_df():
    rp_bar = RepositoryBars()
    df = rp_bar.get_df_bars(Symbol.AAPL, TimeFrame.DAY_1)
    x = []
    state_count = {
        'eq': 0,
        'up': 0,
        'down': 0
    }
    for r in df[:-1].itertuples():
        high_bp = ((r.high - r.open) / r.open) * 10000
        low_bp = ((r.low - r.open) / r.open) * 10000
        close_bp = ((r.close - r.open) / r.open) * 10000
        is_price_up_next = df.loc[r.Index + 1, 'close'] > df.loc[r.Index + 1, 'open']
        if df.loc[r.Index + 1, 'close'] > df.loc[r.Index + 1, 'open']:
            state_count['up'] += 1
        elif df.loc[r.Index + 1, 'close'] < df.loc[r.Index + 1, 'open']:
            state_count['down'] += 1
        else:
            state_count['eq'] += 1
        x.append([high_bp, low_bp, close_bp, r.volume, is_price_up_next])
    print(state_count)
    return pd.DataFrame(
        x,
        columns=['high_bp', 'low_bp', 'close_bp', 'volume', 'is_price_up_next'],
        index=df[:-1].time
    )


def main():
    df = test_convert_df()
    print(df)


if __name__ == '__main__':
    main()
