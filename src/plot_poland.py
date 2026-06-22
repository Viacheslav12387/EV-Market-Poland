import pandas as pd
import plotly.express as px

df = pd.read_csv("data/electric_car_sales.csv")

poland = df[
    (df["region"] == "Poland")
    & (df["parameter"] == "EV sales")
    & (df["powertrain"].isin(["BEV", "PHEV"]))
]

fig = px.line(
    poland,
    x="year",
    y="value",
    color="powertrain",
    markers=True,
    title="Poland EV Market: BEV vs PHEV"
)

fig.show()