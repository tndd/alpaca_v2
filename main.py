from RepositoryBars import RepositoryBars
from datatypes import TimeFrame


def main():
    rp_bar = RepositoryBars()
    rp_bar.store_bars_all(
        timeframe=TimeFrame.DAY_1,
        time_start='2016-01-01',
        time_end='2021-10-12'
    )


if __name__ == '__main__':
    main()
