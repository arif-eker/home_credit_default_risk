import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing

class_freq_num = 25  # Kategorik değişkenleri seçmek için frekans sınır değeri

low_q1 = 0.01  # Aykırı değer bulurken kullanılacak alt quantile sınırı

upper_q3 = 0.98  # Aykırı değer bulurken kullanılacak üst quantile sınırı

correlation_limit = 0.60  # Korelasyon incelenirken kullanılacak olan sınır değer


def check_dataframe(dataframe):
    """
    -> Veriye genel bakış sağlar.

    :param dataframe: Genel bakış yapılacak dataframe

    """

    print("Data Frame Raws Lenght : ", dataframe.shape[0],
          "\nData Frame Columns Lenght : ", dataframe.shape[1])

    print("\nData Frame Columns Names : \n", list(dataframe.columns))

    print("\nIs data frame has null value? : \n", dataframe.isnull().any())

    print("\nHow many missing values are in which columns? :\n", dataframe.isnull().sum())

    cat_names = [col for col in dataframe.columns if dataframe[col].dtype == "O"]
    num_names = [col for col in dataframe.columns if dataframe[col].dtype != "O"]

    print("\nHow many columns are in the object type? : ", len(cat_names), "\n", cat_names)

    print("\nHow many columns are in the numerical type? : ", len(num_names), "\n", num_names)


def get_categorical_and_numeric_columns(dataframe, exit_columns, number_of_unique_classes=class_freq_num):
    """
    -> Kategorik ve sayısal değişkenleri belirler.

    :param dataframe: İşlem yapılacak dataframe
    :param exit_columns: Dikkate alınmayacak değişken ismi
    :param number_of_unique_classes: Değişkenlerin sınıflarının frekans sınırı
    :return: İlk değer olarak kategorik sınıfların adını, ikinci değer olarak sayısal değişkenlerin adını döndürür.

    """

    categorical_columns = [col for col in dataframe.columns
                           if len(dataframe[col].unique()) <= number_of_unique_classes]

    numeric_columns = [col for col in dataframe.columns if len(dataframe[col].unique()) > number_of_unique_classes
                       and dataframe[col].dtype != "O"
                       and col not in exit_columns]

    return categorical_columns, numeric_columns


def cat_summary(dataframe, categorical_columns, target, plot=False):
    """
    -> Kategorik değişkenlerin sınıflarının oranını ve targettaki medyanı gösterir.

    :param dataframe: İşlem yapılacak dataframe
    :param categorical_columns: Kategorik değişkenlerin adları
    :param target: Dataframe'de ilgilendiğimiz değişken.
    :param plot: Grafik çizdirmek için argüman : True/False

    """
    for col in categorical_columns:
        print(col, " : ", dataframe[col].nunique(), " unique classes.\n")

        print(col, " : ", dataframe[col].value_counts().sum(), "\n")

        print("TARGET : ", target, "\n")

        print(pd.DataFrame({"COUNT": dataframe[col].value_counts(),
                            "RATIO ( % )": 100 * dataframe[col].value_counts() / len(dataframe),
                            "TARGET_MEAN": dataframe.groupby(col)[target].mean(),
                            "TARGET_MEDIAN": dataframe.groupby(col)[target].median()}), end="\n\n\n")

        if plot:
            sns.countplot(x=col, data=dataframe)

            plt.show()


def hist_for_numeric_columns(dataframe, numeric_columns):
    """
    -> Sayısal değişkenlerin histogramını çizdirir.

    :param dataframe: İşlem yapılacak dataframe.
    :param numeric_columns: Sayısal değişkenlerin adları

    """
    col_counter = 0

    data = dataframe.copy()

    for col in numeric_columns:
        data[col].hist(bins=20)

        plt.xlabel(col)

        plt.title(col)

        plt.show()

        col_counter += 1

    print(col_counter, "variables have been plotted!")


def outlier_thresholds(dataframe, variable, low_quantile=low_q1, up_quantile=upper_q3):
    """
    -> Verilen değerin alt ve üst aykırı değerlerini hesaplar ve döndürür.

    :param dataframe: İşlem yapılacak dataframe
    :param variable: Aykırı değeri yakalanacak değişkenin adı
    :param low_quantile: Alt eşik değerin hesaplanması için bakılan quantile değeri
    :param up_quantile: Üst eşik değerin hesaplanması için bakılan quantile değeri
    :return: İlk değer olarak verilen değişkenin alt sınır değerini, ikinci değer olarak üst sınır değerini döndürür
    """
    quantile_one = dataframe[variable].quantile(low_quantile)

    quantile_three = dataframe[variable].quantile(up_quantile)

    interquantile_range = quantile_three - quantile_one

    up_limit = quantile_three + 1.5 * interquantile_range

    low_limit = quantile_one - 1.5 * interquantile_range

    return low_limit, up_limit


def has_outliers(dataframe, numeric_columns, plot=False):
    """
    -> Sayısal değişkenlerde aykırı gözlem var mı?

    -> Varsa isteğe göre box plot çizdirme görevini yapar.

    -> Ayrıca aykırı gözleme sahip değişkenlerin ismini göndürür.

    :param dataframe:  İşlem yapılacak dataframe
    :param numeric_columns: Aykırı değerleri bakılacak sayısal değişken adları
    :param plot: Boxplot grafiğini çizdirmek için bool değer alır. True/False
    :return: Aykırı değerlere sahip değişkenlerin adlarını döner
    """
    variable_names = []

    for col in numeric_columns:
        low_limit, up_limit = outlier_thresholds(dataframe, col)

        if dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].any(axis=None):
            number_of_outliers = dataframe[(dataframe[col] > up_limit) | (dataframe[col] < low_limit)].shape[0]

            print(col, " : ", number_of_outliers, " aykırı gözlem.")

            variable_names.append(col)

            if plot:
                sns.boxplot(x=dataframe[col])
                plt.show()

    return variable_names


def remove_outliers(dataframe, numeric_columns):
    """
     Dataframede, verilen sayısal değişkenlerin aykırı gözlemlerini siler ve dataframe döner.

    :param dataframe: İşlem yapılacak dataframe
    :param numeric_columns: Aykırı gözlemleri silinecek sayısal değişken adları
    :return: Aykırı gözlemleri silinmiş dataframe döner
    """

    for variable in numeric_columns:
        low_limit, up_limit = outlier_thresholds(dataframe, variable)

        dataframe_without_outliers = dataframe[~((dataframe[variable] < low_limit) | (dataframe[variable] > up_limit))]

    return dataframe_without_outliers


def replace_with_thresholds(dataframe, numeric_columns):
    """
    Baskılama yöntemi

    Silmemenin en iyi alternatifidir.

    Loc kullanıldığından dataframe içinde işlemi uygular.

    :param dataframe: İşlem yapılacak dataframe
    :param numeric_columns: Aykırı değerleri baskılanacak sayısal değişkenlerin adları
    """
    for variable in numeric_columns:
        low_limit, up_limit = outlier_thresholds(dataframe, variable)

        dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit

        dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


def missing_values_table(dataframe):
    """
     Eksik değerlere sahip değişkenleri gösterir ve bu değerleri döndürür.

    :param dataframe: İşlem yapılacak dataframe
    :return: Eksik değerlere sahip değişkenlerin adlarını döndürür.
    """
    variables_with_na = [col for col in dataframe.columns
                         if dataframe[col].isnull().sum() > 0]

    n_miss = dataframe[variables_with_na].isnull().sum().sort_values(ascending=False)

    ratio = (dataframe[variables_with_na].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)

    # ratio = (100 * dataframe[variables_with_na].isnull().sum() / dataframe.shape[0]).sort_values(ascending=False)

    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=["n_miss", "ratio"])

    print(missing_df)

    return variables_with_na


def label_encoder(dataframe, categorical_columns):
    """
    2 sınıflı kategorik değişkeni 0-1 yapma

    :param dataframe: İşlem yapılacak dataframe
    :param categorical_columns: Label encode yapılacak kategorik değişken adları
    :return:
    """
    labelencoder = preprocessing.LabelEncoder()

    for col in categorical_columns:

        if dataframe[col].nunique() == 2:
            dataframe[col] = labelencoder.fit_transform(dataframe[col])

    return dataframe


def one_hot_encoder(dataframe, categorical_columns, nan_as_category=False):
    """
    Drop_first doğrusal modellerde yapılması gerekli

    Ağaç modellerde gerekli değil ama yapılabilir.

    dummy_na eksik değerlerden değişken türettirir.

    :param dataframe: İşlem yapılacak dataframe
    :param categorical_columns: One-Hot Encode uygulanacak kategorik değişken adları
    :param nan_as_category: NaN değişken oluştursun mu? True/False
    :return: One-Hot Encode yapılmış dataframe ve bu işlem sonrası oluşan yeni değişken adlarını döndürür.
    """
    original_columns = list(dataframe.columns)

    dataframe = pd.get_dummies(dataframe, columns=categorical_columns,
                               dummy_na=nan_as_category, drop_first=False)

    new_columns = [col for col in dataframe.columns if col not in original_columns]

    return dataframe, new_columns


def rare_analyser(dataframe, categorical_columns, target, rare_perc):
    """
     Data frame değişkenlerinin herhangi bir sınıfı, verilen eşik değerden düşük frekansa sahipse bu değişkenleri gösterir.

    :param dataframe: İşlem yapılacak dataframe
    :param categorical_columns: Rare analizi yapılacak kategorik değişken adları
    :param target: Analizi yapılacak hedef değişken adı
    :param rare_perc: Rare için sınır değer. Altında olanlar rare kategorisine girer.
    :return:
    """
    rare_columns = [col for col in categorical_columns
                    if (dataframe[col].value_counts() / len(dataframe) < rare_perc).any(axis=None)]

    print("TARGET : ", target, "\n")
    for var in rare_columns:
        print(var, " : ", len(dataframe[var].value_counts()))

        print(pd.DataFrame({"COUNT": dataframe[var].value_counts(),
                            "RATIO": dataframe[var].value_counts() / len(dataframe),
                            "TARGET_MEAN": dataframe.groupby(var)[target].mean(),
                            "TARGET_MEDIAN": dataframe.groupby(var)[target].median()}),
              end="\n\n\n")

    print(len(rare_columns), " adet rare sınıfa sahip değişken var.")


def aykırı_gozlem_baskıla(dataframe):
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

# Alıntı Başlangıç
# Bu kısım : https://www.kaggle.com/jsaguiar/lightgbm-7th-place-solution  adresinden alınmıştır.
def group(df_to_agg, prefix, aggregations, aggregate_by='SK_ID_CURR'):
    agg_df = df_to_agg.groupby(aggregate_by).agg(aggregations)
    agg_df.columns = pd.Index(['{}{}_{}'.format(prefix, e[0], e[1].upper())
                               for e in agg_df.columns.tolist()])
    return agg_df.reset_index()


def group_and_merge(df_to_agg, df_to_merge, prefix, aggregations, aggregate_by='SK_ID_CURR'):
    agg_df = group(df_to_agg, prefix, aggregations, aggregate_by=aggregate_by)
    return df_to_merge.merge(agg_df, how='left', on=aggregate_by)


# AGGREGATIONS
BUREAU_AGG = {
    'SK_ID_BUREAU': ['nunique'],
    'DAYS_CREDIT': ['min', 'max', 'mean'],
    'DAYS_CREDIT_ENDDATE': ['min', 'max'],
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_OVERDUE': ['max', 'mean', 'sum'],
    'AMT_ANNUITY': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean', 'sum'],
    'MONTHS_BALANCE_MEAN': ['mean', 'var'],
    'MONTHS_BALANCE_SIZE': ['mean', 'sum'],
    # Categorical
    'STATUS_0': ['mean'],
    'STATUS_1': ['mean'],
    'STATUS_12345': ['mean'],
    'STATUS_C': ['mean'],
    'STATUS_X': ['mean'],
    'CREDIT_ACTIVE_Active': ['mean'],
    'CREDIT_ACTIVE_Closed': ['mean'],
    'CREDIT_ACTIVE_Sold': ['mean'],
    'CREDIT_TYPE_Consumer credit': ['mean'],
    'CREDIT_TYPE_Credit card': ['mean'],
    'CREDIT_TYPE_Car loan': ['mean'],
    'CREDIT_TYPE_Mortgage': ['mean'],
    'CREDIT_TYPE_Microloan': ['mean'],
    # Group by loan duration features (months)
    'LL_AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'LL_DEBT_CREDIT_DIFF': ['mean'],
    'LL_STATUS_12345': ['mean'],
}

BUREAU_ACTIVE_AGG = {
    'DAYS_CREDIT': ['max', 'mean'],
    'DAYS_CREDIT_ENDDATE': ['min', 'max'],
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM': ['max', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'sum'],
    'AMT_CREDIT_SUM_OVERDUE': ['max', 'mean'],
    'DAYS_CREDIT_UPDATE': ['min', 'mean'],
    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],
    'CREDIT_TO_ANNUITY_RATIO': ['mean'],
    'MONTHS_BALANCE_MEAN': ['mean', 'var'],
    'MONTHS_BALANCE_SIZE': ['mean', 'sum'],
}

BUREAU_CLOSED_AGG = {
    'DAYS_CREDIT': ['max', 'var'],
    'DAYS_CREDIT_ENDDATE': ['max'],
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'AMT_CREDIT_SUM': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['max', 'sum'],
    'DAYS_CREDIT_UPDATE': ['max'],
    'ENDDATE_DIF': ['mean'],
    'STATUS_12345': ['mean'],
}

BUREAU_LOAN_TYPE_AGG = {
    'DAYS_CREDIT': ['mean', 'max'],
    'AMT_CREDIT_MAX_OVERDUE': ['mean', 'max'],
    'AMT_CREDIT_SUM': ['mean', 'max'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'max'],
    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],
    'DAYS_CREDIT_ENDDATE': ['max'],
}

BUREAU_TIME_AGG = {
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'AMT_CREDIT_SUM': ['max', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'sum'],
    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],
    'STATUS_0': ['mean'],
    'STATUS_12345': ['mean'],
}

# Alıntı Bitiş