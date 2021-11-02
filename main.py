from RepositoryBars import RepositoryBars
from datatypes import TimeFrame
from datatypes.Symbol import Symbol


def main():
    rp_bar = RepositoryBars()
    # rp_bar.store_bars_all(
    #     timeframe=TimeFrame.DAY_1,
    #     time_start='2016-01-01',
    #     time_end='2021-10-12'
    # )
    df = rp_bar.get_df_bars(Symbol.AAPL, TimeFrame.DAY_1)
    print(df)


if __name__ == '__main__':
    main()
