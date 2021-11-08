import pandas as pd


def make_df_bars_discrete_price_movement(
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
    pass
