from datatypes import TimeFrame, Symbol
from data_processor import make_df_bars_close_price_movement, make_df_bars_discrete
from RepositoryBars import RepositoryBars
from analyzer import classification_tree


def test_clf_df_bars_close_price_movement():
    rp_bar = RepositoryBars()
    df_bars = rp_bar.get_df_bars(
        Symbol.AAPL,
        TimeFrame.DAY_1
    )
    df = make_df_bars_close_price_movement(df_bars, back_range=3)
    result = classification_tree(
        df=df,
        objective_var_name='tomorrow',
        class_names=['down', 'eq', 'up'],
        depth=10
    )
    print(result)


def test_clf_df_bars_discrete():
    rp_bar = RepositoryBars()
    df_bars = rp_bar.get_df_bars(
        Symbol.AAPL,
        TimeFrame.DAY_1
    )
    df = make_df_bars_discrete(df_bars)
    result = classification_tree(
        df=df,
        objective_var_name='r_co',
        class_names=['big_down', 'down', 'up', 'big_up'],
        depth=6
    )
    print(result)


def test_make_df_bars_discrete():
    rp_bar = RepositoryBars()
    df_bars = rp_bar.get_df_bars(
        Symbol.AAPL,
        TimeFrame.DAY_1
    )
    df = make_df_bars_discrete(df_bars)
    print(df)


def test_store_bars():
    rp_bar = RepositoryBars()
    rp_bar.store_bars(
        timeframe=TimeFrame.MIN_1,
        symbol=Symbol.AAPL,
        time_start='2016-01-01',
        time_end='2021-10-12'
    )


def main():
    test_clf_df_bars_discrete()


if __name__ == '__main__':
    main()
