# **Bureau Tablosu Keşifçi Veri Analizi İşlemleri**

### :small_red_triangle_down: 1. *Veriye Genel Bakış* :point_left:

###### Bu adımda verimizi okuduktan sonra veriye genel bir bakış yapıyoruz.
###### Verimizi doğru okuduğumuzu kontrol etmek için baştan ve sondan 5 gözleme bakıyoruz.
###### Daha sonra verinin uzunluğuna ve değişken adedine bakıyoruz.
###### Değişkenlerimizin adlarına bakıyoruz.
###### Sonrasında eksik gözlem var mı bu bilgiye bakıyoruz. Bu bilgiden sonra hangi değişkende kaçar adet var buna bakıyoruz.
###### Bu adımlar bittikten sonra değişkenlerimizin kaçı "**object**" tipte ve kaçı "**sayısal**" tipte bu bilgilere bakıyoruz.



### :small_red_triangle_down: 2. *Kategorik Değişkenlerin İncelenmesi* :point_left:

###### Bu adımda kategorik değişkenlerimizi incelemeye geçiyoruz.
###### Öncelikle verimizdeki *kategorik, sayısal ve gereksiz* değişkenlerimizi belirliyoruz.
###### Belirlediğimiz kategorik değişkenlerimizin sayısal değişkenlerle ilişkisine bakıyoruz.
###### Bu işlemi yaparken "*countplot*" yardımı ile kategorik değişkenlerimize görsel olarak bakıyoruz.
###### Aynı zamanda kategorik değişkenlerimizin sınıflarının adedine ve verimizdeki %' sine bakıyoruz.


### :small_red_triangle_down: 3. *Sayısal Değişkenlerin İncelenmesi* :point_left:

###### Bu adımda yukarıda belirlediğimiz sayısal değişkenlerimizin dağılımına bakıyoruz.
###### Bunun için "*histogram*" çizdiriyoruz. Aykırı gözlemleri görebilmek içinse "*boxplot*" çizdiriyoruz.
###### Aykırı gözlemleri seçmek için bir fonksiyon tanımlanabilir -*helper_functions* içinde böyle bir fonksiyon var- fakat bu verimiz için aykırı gözlemleri otomatik yakalamak sorunlu oluyor. 
###### Bu yüzden manuel olarak aykırılıkları yakalıyoruz.
###### Bunun içinse sayısal değişkenlerimiz için kartillere elle bakıyoruz. Böylece hangi değişkende aykırılık var görebiliyoruz.


### :small_red_triangle_down: 4. *Nadirlik İncelemesi* :point_left:

###### Bu adımda kategorik değişkenlerimizdeki nadir sınıfları inceliyoruz.
###### Nadir sınıflar normal şartlarda karşımıza çok zor çıkan durumlardır ve bizlere yük olur.
###### Bunun için bir *sınır* değer belirliyoruz. Örneğin "*%1*".
###### Daha sonra kategorik değişkenlerimizin sınıf adedi veri setimizde bu sınır değişkenden küçükse, bu değişkenleri yakalıyoruz.



### :small_red_triangle_down: 5. *Eksik Gözlem Analizi* :point_left:

###### Bu adımda eksik gözlem analizi yapıyoruz.
###### Değişkenlerde eksik gözleme sahip değişkenleri yakalıyoruz.
###### Yakalanan değişkenlerdeki eksiklik sayısına ve bu eksikliğin verimizde % kaç olduğuna bakıyoruz.


# **Bureau Tablosu - Keşifçi Veri Analizi Sonuçları** :point_down:

### :orange_circle:  *Aykırı Gözlemler*  :orange_circle:


##### :small_orange_diamond: *CREDIT_DAY_OVERDUE*

###### *Başvuru esnasında, önceki kredilerin vadesi geçen gün sayısı* bilgisidir.
###### 1 tane gözlemde *2792* değeri bulunmaktadır. Bu değer *0.99* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *DAYS_CREDIT_ENDDATE*

###### *Başvuru esnasında, önceki kredinin kapanmasına kaç gün kaldığı gün sayısı* bilgisidir.
###### Min değeri *-42.060* gün ve Max değeri *31.199* gündür. Alt aykırı değerler *0.01* kartiller ile ve üst aykırı değerler de *0.97* kartiller değeri ile baskılanmalıdır.

##### :small_orange_diamond: *DAYS_ENDDATE_FACT*

###### *Başvuru esnasında, kapanmmış kredilerin üstünden geçen gün sayısı* bilgisidir.
###### Min değeri *-42.023* gündür. Alt aykırı değerler *0.01* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *AMT_CREDIT_MAX_OVERDUE*

###### *Kredinin bugüne kadar ödenmemiş maks tutarı* bilgisidir.
###### Üst aykırı değerler *0.99* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *AMT_CREDIT_SUM*

###### *Anlık kredi miktarı* bilgisidir.
###### Üst aykırı değerler *0.99* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *AMT_CREDIT_SUM_DEBT*

###### *Kredi için anlık borç* bilgisidir.
###### Mantıksız olarak eksi değerler bulunmaktadır. Alt aykırı değerler *0.01* kartiller ile ve üst aykırı değerler ise *0.99* kartillerle baskılanmalıdır.

##### :small_orange_diamond: *AMT_CREDIT_SUM_LIMIT*

###### *Kredi kartının kredi limiti* bilgisidir.
###### Mantıksız olarak eksi değerler bulunmaktadır. Alt aykırı değerler *0.01* kartiller ile ve üst aykırı değerler ise *0.99* kartillerle baskılanmalıdır.

##### :small_orange_diamond: *AMT_CREDIT_SUM_OVERDUE*

###### *Kredinin ödemesi gelmiş cari tutar* bilgisidir.
###### Üst aykırı değerler *0.99* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *DAYS_CREDIT_UPDATE*

###### *Başvurudan itibaren son bilgiler kaç gün önce geldi* bilgisidir.
###### Min değeri *-41.947* gün ve Max değeri *372* gündür. Alt aykırı değerler *0.01* kartiller ile ve üst aykırı değerler *0.99* kartiller ile baskılanmalıdır.

##### :small_orange_diamond: *AMT_ANNUITY*

###### *Kredi rantı* bilgisidir.
###### Üst aykırı değerler *0.99* kartiller ile baskılanmalıdır.


### :green_circle:  *Nadir Sınıflar*  :green_circle:

##### :small_orange_diamond: *CREDIT_ACTIVE*

###### *Önceki kredinin anlık durum* bilgisidir.
###### Sold ve Bad debt sınıfları Closed sınıfına eklenmelidir.

##### :small_orange_diamond: *CREDIT_CURRENCY*

###### *Kredinin yeniden kodlanmış para birimi* bilgisidir.
###### Bu değişken esasında tamamen düşürülebilir. Currency 1 hariç diğer sınıflar birleştirilebilir.

##### :small_orange_diamond: *CNT_CREDIT_PROLONG*

###### *Kredinin kaç kere uzatıldığı* bilgisidir.
###### Bu değişken esasında tamamen düşürülebilir. 0 hariç diğerleri tek bir çatıda toplanmalıdır.

##### :small_orange_diamond: *CREDIT_TYPE*

###### *Kredinin türü* bilgisidir.
###### Consumer credit ve Credit card sınıfları hariç diğer sınıflar birleştirilmelidir.


### :yellow_circle:  *Eksik Gözlemler*  :yellow_circle:

##### Şu aşamada eksik gözlemleri doldurmak sıkıntı doğuracaktır. Bu yüzden bu işlemler en sonda yapılabilir.