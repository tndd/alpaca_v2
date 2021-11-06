import subprocess
import pandas as pd
from typing import List
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split


def classification_tree(
    df: pd.DataFrame,
    objective_var_name: str,
    class_names: List[str],
    depth: int,
    test_size: float = 0.3,
) -> dict:
    df_x = df.drop(objective_var_name, axis=1)
    df_y = df[objective_var_name]
    (train_x, test_x, train_y, test_y) = train_test_split(
        df_x,
        df_y,
        test_size=test_size,
        random_state=666
    )
    results = {}
    for i in range(1, (depth + 1)):
        clf = DecisionTreeClassifier(max_depth=i)
        clf = clf.fit(train_x, train_y)
        pred = clf.predict(test_x)
        accuracy = sum(pred == test_y) / len(test_y)
        print(i, accuracy)
        results[i] = accuracy
    # visualize
    export_graphviz(
        clf,
        out_file='tree.dot',
        class_names=class_names,
        feature_names=df_x.columns,
        filled=True,
        rounded=True
    )
    subprocess.call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png'])
    return results
