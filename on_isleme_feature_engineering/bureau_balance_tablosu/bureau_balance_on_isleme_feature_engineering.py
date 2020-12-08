# Kütüphaneler eklendi.

import numpy as np
import pandas as pd
import gc
import scripts.helper_functions as hlp

pd.pandas.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)


def get_bureau_balance():
    """

    :return: bureau_balance ön işlemden geçirilmiş hali döndürür.

    """
    df = pd.read_csv("data/bureau_balance.csv")

    df, new_cols = hlp.one_hot_encoder(df, ["STATUS"], nan_as_category=False)

    df_processed = df.groupby('SK_ID_BUREAU')[new_cols].mean().reset_index()

    df["MONTHS_BALANCE"] = -(df["MONTHS_BALANCE"])

    agg = {'MONTHS_BALANCE': ['max']}

    for col in new_cols:
        agg[col] = ['mean']

    df_processed = hlp.group_and_merge(df, df_processed, '', agg, 'SK_ID_BUREAU')
    df_processed.drop(new_cols, axis=1, inplace=True)

    del df
    gc.collect()

    return df_processed
