# importing libraries

import pandas as pd
import numpy as np
import scripts.helper_functions as hlp

pd.pandas.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)

bureau_df = pd.read_csv("data/bureau.csv")

hlp.check_dataframe(bureau_df)

for col in bureau_df.columns:
    print(col, " : ", bureau_df[col].nunique())

bureau_df.head()
bureau_df.tail()

categorical_columns = ["CREDIT_ACTIVE", "CREDIT_CURRENCY", "CNT_CREDIT_PROLONG", "CREDIT_TYPE"]

ids = ["SK_ID_CURR", "SK_ID_BUREAU"]

numerical_columns = [col for col in bureau_df.columns if col not in categorical_columns and col not in ids]

len(categorical_columns)
len(numerical_columns)

for col in numerical_columns:
    hlp.cat_summary(bureau_df, categorical_columns, col)

hlp.hist_for_numeric_columns(bureau_df, numerical_columns)

for col in numerical_columns:
    print(bureau_df[col].describe([0.009, 0.01, 0.05, 0.95, 0.98, 0.99, 0.995]))

hlp.aykırı_gozlem_baskıla(bureau_df)