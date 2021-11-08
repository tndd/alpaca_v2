import pandas as pd


def _discretezation_pr_ho(pr_ho):
    if pr_ho == 1.0:
        return 1
    elif 1.0 <= pr_ho <= 1.005:
        return 2
    elif 1.005 < pr_ho:
        return 3
    else:
        raise Exception('Invalid input.')


def _discretezation_pr_lo(pr_lo):
    if pr_lo <= 0.995:
        return 1
    elif 0.995 < pr_lo <= 1.0:
        return 2
    else:
        raise Exception('Invalid input.')


def _discretezation(r):
    if r <= 0.995:
        return 1
    elif 0.995 < r <= 1.0:
        return 2
    elif 1.0 <= r <= 1.005:
        return 3
    elif 1.005 < r:
        return 4
    else:
        raise Exception('Invalid input.')


def make_df_bars_discrete(
    df_bars: pd.DataFrame
) -> pd.DataFrame:
    """
    Scheme "df_bars_discrete_price_movement"
        pr_ho: int
            Ratio of previous time's open price to high price.
                1: pr_ho = 1.0
                2: 1.0 <= pr_ho <= 1.005
                3: 1.005 < pr_ho
        pr_lo: int
            Ratio of previous time's open price to low price.
                1: pr_lo <= 0.995
                2: 0.995 < pr_lo <= 1.0
        pr_co: int
            Ratio of previous time's open price to close price.
                1: pr_co <= 0.995
                2: 0.995 < pr_co <= 1.0
                3: 1.0 < pr_co <= 1.005
                4: 1.005 < pr_co
        pnr_oc: int
            Ratio of previous time's now's open price to close price.
                1: pnr_oc <= 0.995
                2: 0.995 < pnr_oc <= 1.0
                3: 1.0 < pnr_oc <= 1.005
                4: 1.005 < pnr_oc
        [OBJ] r_co: int
            Ratio of now time's open price to close price.
                1: r_co <= 0.995
                2: 0.995 < r_co <= 1.0
                3: 1.0 < r_co <= 1.005
                4: 1.005 < r_co
    """
    rows = []
    for r in df_bars[1:].itertuples():
        prev_r = df_bars.loc[r.Index - 1]
        pr_ho = _discretezation_pr_ho(prev_r.high / prev_r.open)
        pr_lo = _discretezation_pr_lo(prev_r.low / prev_r.open)
        pr_co = _discretezation(prev_r.close / prev_r.open)
        pnr_oc = _discretezation(r.open / prev_r.close)
        r_co = _discretezation(r.close / r.open)
        rows.append((pr_ho, pr_lo, pr_co, pnr_oc, r_co))
    return pd.DataFrame(
        rows,
        columns=('pr_ho', 'pr_lo', 'pr_co', 'pnr_oc', 'r_co'),
        index=df_bars[1:].time
    )
