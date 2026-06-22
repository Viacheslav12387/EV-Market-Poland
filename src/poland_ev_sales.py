import pandas as pd

df = pd.read_csv("data/electric_car_sales.csv")

poland = df[df["region"] == "Poland"]

sales = poland[poland["parameter"] == "EV sales"]

print(sales[["year", "powertrain", "value"]])
