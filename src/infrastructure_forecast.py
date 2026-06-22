import pandas as pd

ev_scenarios = [500000, 750000, 1000000]

current_ratio = 20.3

results = []

for ev_count in ev_scenarios:

    chargers_needed = round(ev_count / current_ratio)

    results.append([
        ev_count,
        chargers_needed
    ])

forecast = pd.DataFrame(
    results,
    columns=[
        "EV_Count",
        "Chargers_Needed"
    ]
)

print(forecast)