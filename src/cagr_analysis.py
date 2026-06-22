import pandas as pd

df = pd.read_csv("data/electric_car_sales.csv")

bev = df[
    (df["region"] == "Poland")
    & (df["parameter"] == "EV sales")
    & (df["powertrain"] == "BEV")
]

bev = bev.sort_values("year")

start = bev[bev["year"] == 2020]["value"].iloc[0]
end = bev[bev["year"] == 2023]["value"].iloc[0]

years = 3

cagr = ((end / start) ** (1 / years) - 1) * 100

print(f"Start: {start}")
print(f"End: {end}")
print(f"CAGR: {cagr:.2f}%")