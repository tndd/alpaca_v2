import subprocess
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split

from datatypes import TimeFrame, Symbol
from data_processor import get_df_bars_close_price_movements
from RepositoryBars import RepositoryBars


def test_decision_tree():
    rp_bar = RepositoryBars()
    df_bars = rp_bar.get_df_bars(
        Symbol.AAPL,
        TimeFrame.DAY_1
    )
    df = get_df_bars_close_price_movements(df_bars, back_range=6)
    df_x = df.drop('tomorrow', axis=1)
    df_y = df.tomorrow
    (train_x, test_x, train_y, test_y) = train_test_split(df_x, df_y, test_size=0.3, random_state=666)
    for i in range(1, 11):
        clf = DecisionTreeClassifier(max_depth=i)
        clf = clf.fit(train_x, train_y)
        pred = clf.predict(test_x)
        accuracy = sum(pred == test_y) / len(test_y)
        print(f'depth: {i}')
        print(accuracy)
    # visualize
    export_graphviz(
        clf,
        out_file='tree.dot',
        class_names=['up', 'down', 'eq'],
        feature_names=df_x.columns,
        filled=True,
        rounded=True
    )
    subprocess.call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png'])


def test_store_bars():
    rp_bar = RepositoryBars()
    rp_bar.store_bars(
        timeframe=TimeFrame.MIN_1,
        symbol=Symbol.AAPL,
        time_start='2016-01-01',
        time_end='2021-10-12'
    )


def main():
    test_decision_tree()
    # rp_bar = RepositoryBars()
    # df = rp_bar.get_df_bars_close_price_movements(Symbol.AAPL, TimeFrame.DAY_1, back_range=10)
    # print(df)


if __name__ == '__main__':
    main()
