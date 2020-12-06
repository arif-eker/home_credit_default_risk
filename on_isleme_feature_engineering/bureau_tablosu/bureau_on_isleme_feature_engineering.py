#
# Ön İşleme ve Feature Engineering işlemleri burada yapılacaktır.
#

# Gerekli kütüphaneler eklendi.

import pandas as pd
import numpy as np
import scripts.helper_functions as hlp


# Veri okunuyor.
bureau_df = pd.read_csv("data/bureau.csv")

# Aykırı gözlemler baskılanıyor.
hlp.aykırı_gozlem_baskıla(bureau_df)