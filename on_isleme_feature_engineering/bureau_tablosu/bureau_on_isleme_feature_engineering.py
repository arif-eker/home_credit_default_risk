#
# Ön İşleme ve Feature Engineering işlemleri burada yapılacaktır.
#

# Gerekli kütüphaneler eklendi.

import pandas as pd
import numpy as np
import scripts.helper_functions as hlp

import on_isleme_feature_engineering.bureau_balance_tablosu.bureau_balance_on_isleme_feature_engineering as balance


# ************************************************ #

def aykiri_gozlem_baskila(dataframe):
    dataframe.loc[
        (dataframe["CREDIT_DAY_OVERDUE"] > dataframe["CREDIT_DAY_OVERDUE"].quantile(0.99)), "CREDIT_DAY_OVERDUE"] = \
        dataframe["CREDIT_DAY_OVERDUE"].quantile(0.99)

    dataframe.loc[
        (dataframe["DAYS_CREDIT_ENDDATE"] > dataframe["DAYS_CREDIT_ENDDATE"].quantile(0.97)), "DAYS_CREDIT_ENDDATE"] = \
        dataframe["DAYS_CREDIT_ENDDATE"].quantile(0.97)
    dataframe.loc[
        (dataframe["DAYS_CREDIT_ENDDATE"] < dataframe["DAYS_CREDIT_ENDDATE"].quantile(0.01)), "DAYS_CREDIT_ENDDATE"] = \
        dataframe["DAYS_CREDIT_ENDDATE"].quantile(0.01)

    dataframe.loc[
        (dataframe["DAYS_ENDDATE_FACT"] < dataframe["DAYS_ENDDATE_FACT"].quantile(0.01)), "DAYS_ENDDATE_FACT"] = \
        dataframe["DAYS_ENDDATE_FACT"].quantile(0.01)

    dataframe.loc[(dataframe["AMT_CREDIT_MAX_OVERDUE"] > dataframe["AMT_CREDIT_MAX_OVERDUE"].quantile(
        0.99)), "AMT_CREDIT_MAX_OVERDUE"] = dataframe["AMT_CREDIT_MAX_OVERDUE"].quantile(0.99)

    dataframe.loc[(dataframe["AMT_CREDIT_SUM"] > dataframe["AMT_CREDIT_SUM"].quantile(0.99)), "AMT_CREDIT_SUM"] = \
        dataframe[
            "AMT_CREDIT_SUM"].quantile(0.99)

    dataframe.loc[
        (dataframe["AMT_CREDIT_SUM_DEBT"] > dataframe["AMT_CREDIT_SUM_DEBT"].quantile(0.99)), "AMT_CREDIT_SUM_DEBT"] = \
        dataframe["AMT_CREDIT_SUM_DEBT"].quantile(0.99)
    dataframe.loc[
        (dataframe["AMT_CREDIT_SUM_DEBT"] < dataframe["AMT_CREDIT_SUM_DEBT"].quantile(0.01)), "AMT_CREDIT_SUM_DEBT"] = \
        dataframe["AMT_CREDIT_SUM_DEBT"].quantile(0.01)

    dataframe.loc[
        (dataframe["AMT_CREDIT_SUM_LIMIT"] > dataframe["AMT_CREDIT_SUM_LIMIT"].quantile(
            0.99)), "AMT_CREDIT_SUM_LIMIT"] = \
        dataframe["AMT_CREDIT_SUM_LIMIT"].quantile(0.99)
    dataframe.loc[
        (dataframe["AMT_CREDIT_SUM_LIMIT"] < dataframe["AMT_CREDIT_SUM_LIMIT"].quantile(
            0.01)), "AMT_CREDIT_SUM_LIMIT"] = \
        dataframe["AMT_CREDIT_SUM_LIMIT"].quantile(0.01)

    dataframe.loc[(dataframe["AMT_CREDIT_SUM_OVERDUE"] > dataframe["AMT_CREDIT_SUM_OVERDUE"].quantile(
        0.99)), "AMT_CREDIT_SUM_OVERDUE"] = dataframe["AMT_CREDIT_SUM_OVERDUE"].quantile(0.99)

    dataframe.loc[
        (dataframe["DAYS_CREDIT_UPDATE"] > dataframe["DAYS_CREDIT_UPDATE"].quantile(0.99)), "DAYS_CREDIT_UPDATE"] = \
        dataframe["DAYS_CREDIT_UPDATE"].quantile(0.99)
    dataframe.loc[
        (dataframe["DAYS_CREDIT_UPDATE"] < dataframe["DAYS_CREDIT_UPDATE"].quantile(0.01)), "DAYS_CREDIT_UPDATE"] = \
        dataframe["DAYS_CREDIT_UPDATE"].quantile(0.01)

    dataframe.loc[(dataframe["AMT_ANNUITY"] > dataframe["AMT_ANNUITY"].quantile(0.99)), "AMT_ANNUITY"] = dataframe[
        "AMT_ANNUITY"].quantile(0.99)


def rare_encode(dataframe):
    dataframe['CREDIT_TYPE'] = dataframe['CREDIT_TYPE'].replace(['Car loan',
                                                                 'Mortgage',
                                                                 'Microloan',
                                                                 'Loan for business development',
                                                                 'Another type of loan',
                                                                 'Unknown type of loan',
                                                                 'Loan for working capital replenishment',
                                                                 "Loan for purchase of shares (margin lending)",
                                                                 'Cash loan (non-earmarked)',
                                                                 'Real estate loan',
                                                                 "Loan for the purchase of equipment",
                                                                 "Interbank credit",
                                                                 "Mobile operator loan"], 'Rare')

    dataframe['CREDIT_ACTIVE'] = dataframe['CREDIT_ACTIVE'].replace(['Bad debt', 'Sold'], 'Closed')

    dataframe['CREDIT_CURRENCY'] = dataframe['CREDIT_CURRENCY'].replace(['currency 2', 'currency 3', 'currency 4'],
                                                                        'currency others')
    dataframe['CNT_CREDIT_PROLONG'] = dataframe['CNT_CREDIT_PROLONG'].replace([2, 3, 4, 5, 6, 7, 8, 9],
                                                                              1)


# ************************************************ #

def get_bureau_and_balance():
    bureau_df = pd.read_csv("data/bureau.csv")
    bb = balance.get_bureau_balance()

    aykiri_gozlem_baskila(bureau_df)

    rare_encode(bureau_df)

    bureau_df = bureau_df.merge(bb, how='left', on='SK_ID_BUREAU')

    # Açık kredilerin erken kapanması yoktur. Bu yüzden süreleri, kredinin başlangıç günü + biteceği günden hesaplanır.

    bureau_df.loc[bureau_df["CREDIT_ACTIVE"] == "Active", "CREDIT_DURATION"] = \
        -(bureau_df.loc[bureau_df["CREDIT_ACTIVE"] == "Active", "DAYS_CREDIT"]) + bureau_df.loc[
            bureau_df["CREDIT_ACTIVE"] == "Active", "DAYS_CREDIT_ENDDATE"]

    # Açık krediler erken kapanmış olabilir. Bu yüzden süreleri, kredinin başlangıç günü + kapatıldığı gündür.
    bureau_df.loc[bureau_df["CREDIT_ACTIVE"] == "Closed", "CREDIT_DURATION"] = \
        -(bureau_df.loc[bureau_df["CREDIT_ACTIVE"] == "Closed", "DAYS_CREDIT"]) + bureau_df.loc[
            bureau_df["CREDIT_ACTIVE"] == "Closed", "DAYS_ENDDATE_FACT"]

    # Kredinin kapatılma tarihleri arasındaki fark. Erken kapanırsa +, geç kapatılırsa - değer alır. Zamanındakiler için 0 olur.
    bureau_df['ENDDATE_DIF'] = bureau_df['DAYS_CREDIT_ENDDATE'] - bureau_df['DAYS_ENDDATE_FACT']

    # Anlık kredinin yıllık krediye oranı
    bureau_df['CREDIT_TO_ANNUITY_RATIO'] = bureau_df['AMT_CREDIT_SUM'] / bureau_df['AMT_ANNUITY']
