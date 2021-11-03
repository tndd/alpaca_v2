from RepositoryBars import RepositoryBars
from datatypes import TimeFrame
from datatypes.Symbol import Symbol
from sklearn.tree import DecisionTreeClassifier


def test_decision_tree():
    pass


def main():
    rp_bar = RepositoryBars()
    df = rp_bar.get_df_bars(Symbol.AAPL, TimeFrame.DAY_1)
    print(df)


if __name__ == '__main__':
    main()
