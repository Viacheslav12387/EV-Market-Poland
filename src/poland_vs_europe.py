import pandas as pd

df = pd.read_csv("data/electric_car_sales.csv")

countries = ["Poland", "Europe", "EU27"]

comparison = df[
    (df["region"].isin(countries))
    & (df["parameter"] == "EV sales share")
    & (df["powertrain"] == "EV")
]

print(
    comparison[
        ["region", "year", "value"]
    ].sort_values(
        ["region", "year"]
    )
)