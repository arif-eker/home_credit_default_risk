# ***************************************************************#
#                                                                #
#   Bureau tablosunun eda işlemleri burada yapılacaktır.         #
#                                                                #
# ***************************************************************#


# Gerekli kütüphaneler ekleniyor.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scripts.helper_functions as hlp

# ******************************************************************************************** #

# Değişkenleri göstermesi için gerekli ayarlar yapılıyor.

pd.pandas.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)

# ******************************************************************************************** #

# Veri okunuyor.

bureau_df = pd.read_csv("data/bureau.csv")

# ******************************************************************************************** #

# head ile ilk 5, tail ile son 5 gözleme bakılıyor.
# Verinin düzgün okunup okunmadığı anlaşılıyor.

bureau_df.head()
bureau_df.tail()

# ******************************************************************************************** #

# Verimize genel hatları ile bakıyoruz.

hlp.check_dataframe(bureau_df)

# ******************************************************************************************** #

# Verimizdeki değişkenlerin, kaçar adet sınıfı var buna bakıyoruz.

for col in bureau_df.columns:
    print(col, " : ", bureau_df[col].nunique())

# ******************************************************************************************** #

# Kategorik, sayısal ve ID' lerden oluşan değişkenlerimizi ayrı ayrı seçiyoruz.

categorical_columns = ["CREDIT_ACTIVE", "CREDIT_CURRENCY", "CNT_CREDIT_PROLONG", "CREDIT_TYPE"]

ids = ["SK_ID_CURR", "SK_ID_BUREAU"]

numerical_columns = [col for col in bureau_df.columns if col not in categorical_columns and col not in ids]

# ******************************************************************************************** #

# Kategorik değişkenlerimizin, her bir sayısal değişkenle ilgili incelemesini yapıyoruz.

for col in numerical_columns:
    hlp.cat_summary(bureau_df, categorical_columns, col, True)

# ******************************************************************************************** #

# Sayısal değişkenlerimizin histogramını incelemek için çizdiriyoruz.
hlp.hist_for_numeric_columns(bureau_df, numerical_columns)
for col in numerical_columns:
    sns.boxplot(x=bureau_df[col])
    plt.show()
# ******************************************************************************************** #

# Sayısal değişkenlerimizin quantile değerlerine bakalım.
for col in numerical_columns:
    print(bureau_df[col].describe([0.009, 0.01, 0.05, 0.95, 0.98, 0.99, 0.995]))

# ******************************************************************************************** #

# Nadir sınıflara sahip değişkenlerimizi bulup, bu sınıfları inceliyoruz.
rare_perc = 0.02
rare_columns = [col for col in categorical_columns
                if (bureau_df[col].value_counts() / len(bureau_df) < rare_perc).any(axis=None)]

for var in rare_columns:
    print(var, " : ", len(bureau_df[var].value_counts()))

    print(pd.DataFrame({"COUNT": bureau_df[var].value_counts(),
                        "RATIO (%)": 100 * bureau_df[var].value_counts() / len(bureau_df)}),
          end="\n\n\n")

    print(len(rare_columns), " adet rare sınıfa sahip değişken var.")

# ******************************************************************************************** #

# Eksik gözlemlere bakıyoruz.

na_variables = hlp.missing_values_table(bureau_df)

# ******************************************************************************************** #
