from RepositoryBars import RepositoryBars
from datatypes import TimeFrame, Symbol


def main():
    rp_bar = RepositoryBars()
    # print(rp_bar.get_latest_time(symbol='GLD', timeframe=TimeFrame.DAY_1))
    rp_bar.store_bars(
        timeframe=TimeFrame.DAY_1,
        symbol=Symbol.BRK_B,
        time_start='2016-01-01',
        time_end='2021-10-12'
    )


if __name__ == '__main__':
    main()
