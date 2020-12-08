# Kütüphaneler eklendi.

import numpy as np
import pandas as pd
import gc
import scripts.helper_functions as hlp


pd.pandas.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)

bb = pd.read_csv("data/bureau_balance.csv")

bb, new_cols = hlp.one_hot_encoder(bb, ["STATUS"], nan_as_category=False)

bb_processed = bb.groupby('SK_ID_BUREAU')[new_cols].mean().reset_index()

bb["MONTHS_BALANCE"] = -(bb["MONTHS_BALANCE"])

agg = {'MONTHS_BALANCE': ['max']}

bb_processed = hlp.group_and_merge(bb, bb_processed, '', agg, 'SK_ID_BUREAU')

del bb
gc.collect()

# return bb_processed
