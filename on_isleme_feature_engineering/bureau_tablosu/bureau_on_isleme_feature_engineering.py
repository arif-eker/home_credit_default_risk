#
# Ön İşleme ve Feature Engineering işlemleri burada yapılacaktır.
#

# Gerekli kütüphaneler eklendi.
import gc
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
                                                                 "Mobile operator loan"], 'Others')

    dataframe['CREDIT_ACTIVE'] = dataframe['CREDIT_ACTIVE'].replace(['Bad debt', 'Sold'], 'Closed')

    dataframe['CREDIT_CURRENCY'] = dataframe['CREDIT_CURRENCY'].replace(['currency 2', 'currency 3', 'currency 4'],
                                                                        'currency others')
    dataframe['CNT_CREDIT_PROLONG'] = dataframe['CNT_CREDIT_PROLONG'].replace([2, 3, 4, 5, 6, 7, 8, 9],
                                                                              1)


# Bu kod alıntıdır. : https://github.com/ahmetcankaraoglan/Home-Credit-Default-Risk/blob/main/models/Home%20Credit%20Default%20Risk/Home%20Credit%20Default%20Risk.ipynb

# Alıntı başlangıç
def feature_early_shutdown(row):
    if row.CREDIT_ACTIVE == "Closed" and row.DAYS_ENDDATE_FACT < row.DAYS_CREDIT_ENDDATE:
        return 1
    elif row.CREDIT_ACTIVE == "Closed" and row.DAYS_CREDIT_ENDDATE <= row.DAYS_ENDDATE_FACT:
        return 0
    else:
        return np.nan


# Alıntı bitiş

def degisken_ekle(dataframe):
    # Açık kredilerin erken kapanması yoktur. Bu yüzden süreleri, kredinin başlangıç günü + biteceği günden hesaplanır.

    dataframe.loc[dataframe["CREDIT_ACTIVE"] == "Active", "KREDI_SURESI"] = \
        -(dataframe.loc[dataframe["CREDIT_ACTIVE"] == "Active", "DAYS_CREDIT"]) + dataframe.loc[
            dataframe["CREDIT_ACTIVE"] == "Active", "DAYS_CREDIT_ENDDATE"]

    # Kapalı krediler erken kapanmış olabilir. Bu yüzden süreleri, kredinin başlangıç günü + kapatıldığı gündür.
    dataframe.loc[dataframe["CREDIT_ACTIVE"] == "Closed", "KREDI_SURESI"] = \
        -(dataframe.loc[dataframe["CREDIT_ACTIVE"] == "Closed", "DAYS_CREDIT"]) + dataframe.loc[
            dataframe["CREDIT_ACTIVE"] == "Closed", "DAYS_ENDDATE_FACT"]

    # Kredinin kapatılma tarihleri arasındaki fark. Erken kapanırsa +, geç kapatılırsa - değer alır. Zamanındakiler için 0 olur.
    dataframe['ENDDATE_FARK'] = dataframe['DAYS_CREDIT_ENDDATE'] - dataframe['DAYS_ENDDATE_FACT']

    # Anlık kredinin yıllık krediye oranı
    dataframe['KREDI/YILLIK_ORAN'] = dataframe['AMT_CREDIT_SUM'] / dataframe['AMT_ANNUITY']

    # Açık kredilerin borçları krediden yüksekse, ödenmesi gereken kredi tutarı bu borç olarak değiştirilmelidir.
    # Kapalı krediler için 0 değeri atanmalıdır.
    dataframe["ODENMESI_GEREKEN_TUTAR"] = np.nan

    dataframe.loc[dataframe["AMT_CREDIT_SUM_DEBT"] > dataframe["AMT_CREDIT_SUM"], "ODENMESI_GEREKEN_TUTAR"] = \
        dataframe.loc[dataframe["AMT_CREDIT_SUM_DEBT"] > dataframe["AMT_CREDIT_SUM"], "AMT_CREDIT_SUM_DEBT"]

    dataframe.loc[dataframe["CREDIT_ACTIVE"] == "Closed", "ODENMESI_GEREKEN_TUTAR"] = 0.0

    # Kredinin erken ödenip ödenmemesi. erken ödeme = 1, ödememe 0. Aktif krediler için ise nan

    dataframe["ERKEN_KAPAMA"] = dataframe.apply(lambda x: feature_early_shutdown(x), axis=1)


# ************************************************ #

def get_bureau_and_balance():
    bureau_df = pd.read_csv("data/bureau.csv")
    bb = balance.get_bureau_balance()

    aykiri_gozlem_baskila(bureau_df)

    rare_encode(bureau_df)

    bureau__balance = bureau_df.merge(bb, how='left', on='SK_ID_BUREAU')

    degisken_ekle(bureau__balance)

    del bb, bureau_df

    gc.collect()

    return bureau__balance
