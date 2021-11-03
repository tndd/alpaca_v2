import pandas as pd
from RepositoryBars import RepositoryBars
from datatypes import TimeFrame
from datatypes.Symbol import Symbol
from sklearn.tree import DecisionTreeClassifier


def test_convert_df():
    rp_bar = RepositoryBars()
    df = rp_bar.get_df_bars(Symbol.AAPL, TimeFrame.DAY_1)
    x = []
    for r in df.itertuples():
        high_bp = ((r.high - r.open) / r.open) * 10000
        low_bp = ((r.low - r.open) / r.open) * 10000
        close_bp = ((r.close - r.open) / r.open) * 10000
        x.append([high_bp, low_bp, close_bp, r.volume])
    return pd.DataFrame(
        x,
        columns=['high_bp', 'low_bp', 'close_bp', 'volume'],
        index=df.time
    )


def main():
    df = test_convert_df()
    print(df)


if __name__ == '__main__':
    main()
