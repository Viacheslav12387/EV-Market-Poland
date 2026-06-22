import pandas as pd

current_sales = 17000
start_year = 2023
end_year = 2030

scenarios = {
    "Conservative": 0.15,
    "Base": 0.25,
    "Optimistic": 0.35
}

results = []

for scenario, growth in scenarios.items():

    sales = current_sales

    for year in range(start_year + 1, end_year + 1):

        sales = sales * (1 + growth)

        results.append([
            scenario,
            year,
            round(sales)
        ])

forecast = pd.DataFrame(
    results,
    columns=["Scenario", "Year", "Sales"]
)

print(forecast)