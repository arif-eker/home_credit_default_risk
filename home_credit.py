# importing libraries

import pandas as pd
import numpy as np


pd.pandas.set_option("display.max_columns", None)



# reading data

df = pd.read_csv("datasets/bureau.csv")

df.head()

df.groupby("SK_ID_CURR")["SK_ID_BUREAU"].count().head()

df["AMT_ANNUITY"].quantile(0.995)
df["AMT_ANNUITY"].mean()
df["AMT_ANNUITY"].median()

df["AMT_ANNUITY"].describe()

df.shape

df["CREDIT_TYPE"].unique()