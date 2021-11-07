from datatypes import TimeFrame, Symbol
from data_processor import get_df_bars_close_price_movements
from RepositoryBars import RepositoryBars
from analyzer import classification_tree


def test_classification_tree():
    rp_bar = RepositoryBars()
    df_bars = rp_bar.get_df_bars(
        Symbol.AAPL,
        TimeFrame.DAY_1
    )
    df = get_df_bars_close_price_movements(df_bars, back_range=3)
    result = classification_tree(
        df=df,
        objective_var_name='tomorrow',
        class_names=['down', 'eq', 'up'],
        depth=10
    )
    print(result)


def test_store_bars():
    rp_bar = RepositoryBars()
    rp_bar.store_bars(
        timeframe=TimeFrame.MIN_1,
        symbol=Symbol.AAPL,
        time_start='2016-01-01',
        time_end='2021-10-12'
    )


def main():
    test_classification_tree()


if __name__ == '__main__':
    main()
