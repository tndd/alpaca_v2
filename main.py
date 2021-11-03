import subprocess
import pandas as pd
from RepositoryBars import RepositoryBars
from datatypes import TimeFrame
from datatypes.Symbol import Symbol
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn.metrics import (roc_curve, auc, accuracy_score)


def test_convert_df():
    rp_bar = RepositoryBars()
    df = rp_bar.get_df_bars(Symbol.AAPL, TimeFrame.DAY_1)
    x = []
    for r in df[:-1].itertuples():
        high_bp = ((r.high - r.open) / r.open) * 10000
        low_bp = ((r.low - r.open) / r.open) * 10000
        close_bp = ((r.close - r.open) / r.open) * 10000
        # 0: up, 1: down, 2: eq
        if df.loc[r.Index + 1, 'close'] > df.loc[r.Index + 1, 'open']:
            is_price_up_next = 0
        elif df.loc[r.Index + 1, 'close'] < df.loc[r.Index + 1, 'open']:
            is_price_up_next = 1
        else:
            is_price_up_next = 2
        x.append([high_bp, low_bp, close_bp, r.volume, is_price_up_next])
    return pd.DataFrame(
        x,
        columns=['high_bp', 'low_bp', 'close_bp', 'volume', 'is_price_up_next'],
        index=df[:-1].time
    )


def test_decision_tree():
    df = test_convert_df()
    df_x = df.drop('is_price_up_next', axis=1)
    df_y = df.is_price_up_next
    (train_x, test_x, train_y, test_y) = train_test_split(df_x, df_y, test_size=0.3, random_state=666)
    clf = DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(train_x, train_y)
    pred = clf.predict(test_x)
    fpr, tpr, thresholds = roc_curve(test_y, pred, pos_label=1)
    print(auc(fpr, tpr))
    print(accuracy_score(pred, test_y))
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

def main():
    test_decision_tree()


if __name__ == '__main__':
    main()
