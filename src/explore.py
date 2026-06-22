import pandas as pd

df = pd.read_csv("data/electric_car_sales.csv")

print("Wymiary:")
print(df.shape)

print("\nKolumny:")
print(df.columns)

print("\nBraki danych:")
print(df.isnull().sum())

print("\nParametry:")
print(df["parameter"].unique())

print("\nNapędy:")
print(df["powertrain"].unique())

print("\nLata:")
print(df["year"].min(), "-", df["year"].max())

print("\nPrzykładowe kraje:")
print(sorted(df["region"].unique())[:50])
Wymiary:
(3798, 8)

Kolumny:
Index(['region', 'category', 'parameter', 'mode', 'powertrain', 'year', 'unit',
       'value'],
      dtype='object')

Braki danych:
region        0
category      0
parameter     0
mode          0
powertrain    0
year          0
unit          0
value         0
dtype: int64

Parametry:
['EV sales' 'EV stock share' 'EV sales share' 'EV stock'
 'Electricity demand' 'Oil displacement Mbd'
 'Oil displacement, million lge']

Napędy:
['BEV' 'EV' 'PHEV' 'FCEV']

Lata:
2010 - 2023

Przykładowe kraje:
['Australia', 'Austria', 'Belgium', 'Brazil', 'Bulgaria', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'EU27', 'Estonia', 'Europe', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'India', 'Ireland', 'Israel', 'Italy', 'Japan', 'Korea', 'Latvia', 'Lithuania', 'Luxembourg', 'Mexico', 'Netherlands', 'New Zealand', 'Norway', 'Poland', 'Portugal', 'Rest of the world', 'Romania', 'Seychelles', 'Slovakia', 'Slovenia', 'South Africa', 'Spain', 'Sweden', 'Switzerland', 'Turkiye', 'USA', 'United Arab Emirates']
vycheslav2018ayfonicloud.com@MBP-Vycheslav EV_Market_Poland %