import pandas as pd
from functions import data_clean

# Create an index that determine if a country is nice to live or not.
# Process files
data = "world-data-2023.csv"
read_data = pd.read_csv(data)
df = pd.DataFrame(read_data)

# Data Clean
df = data_clean(df)

"""Create average CO2 Emissions per person"""
df["CO2-Emissions/person"] = df["Population"] / df["Co2-Emissions"]
"""Create GDP per capita column"""
df["GDP per capita"] = df["GDP"] / df["Population"]


# Create index
"""This index was created specifically to calculate how good it is to live in a country.
All results are based on dataframe information:
https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023
It wasn't designed to cater to that country's military, wealth, or anything else.
Furthermore, this index is not influenced by personal opinions about a specific country or type of country."""

"""Declare points"""
points = 0


def QOLindex(country):
    """Global variable points"""
    global points

    """Check if function arguments is a string or a list of strings"""
    if (
        isinstance(country, list)
        and all(isinstance(i, str) for i in country)
        or (isinstance(country, str))
    ):
        if not isinstance(country, list):
            country = [country]
        for c in country:
            points = 0
            country_row = df[df["Country"] == c]

            if (
                not pd.isnull(
                    country_row[
                        [
                            "Gross tertiary education enrollment (%)",
                            "Physicians per thousand",
                            "Life expectancy",
                            "Unemployment rate",
                            "Forested Area (%)",
                            "Gross primary education enrollment (%)",
                            "GDP per capita",
                            "Infant mortality",
                            "Maternal mortality ratio",
                            "CO2-Emissions/person",
                            "Co2-Emissions",
                            "Tax revenue (%)",
                            "Total tax rate",
                        ]
                    ]
                )
                .any()
                .any()
            ):

                def evaluate_economics():
                    """Global variable points"""
                    global points

                    """Double conditions"""
                    if (
                        country_row.loc[:, "Total tax rate"].item() < 50
                        and country_row.loc[:, "Tax revenue (%)"].item() < 15
                    ):
                        points += 3
                    elif (
                        country_row.loc[:, "Total tax rate"].item() < 65
                        and country_row.loc[:, "Tax revenue (%)"].item() < 20
                    ):
                        points += 1
                    if (
                        country_row.loc[:, "GDP per capita"].item() >= 40000
                        and country_row.loc[:, "Unemployment rate"].item() <= 5
                    ):
                        points += 7
                    elif (
                        country_row.loc[:, "GDP per capita"].item() >= 25000
                        and country_row.loc[:, "Unemployment rate"].item() <= 10
                    ):
                        points += 3

                    """Single conditions"""
                    if country_row.loc[:, "Unemployment rate"].item() < 1:
                        points += 3
                    elif country_row.loc[:, "Unemployment rate"].item() > 25:
                        points -= 5
                    elif country_row.loc[:, "GDP per capita"].item() < 1000:
                        points -= 5
                    
                evaluate_economics()

                def evaluate_education():
                    """Global variable points"""
                    global points

                    """Double conditions"""
                    if country_row.loc[
                        :, "Gross primary education enrollment (%)"
                    ].item() >= 100 and (
                        country_row.loc[
                            :, "Gross tertiary education enrollment (%)"
                        ].item()
                        > 70
                    ):
                        points += 5
                    elif (
                        country_row.loc[
                            :, "Gross primary education enrollment (%)"
                        ].item()
                        >= 95
                    ):
                        points += 3

                    """Single conditions"""
                    if (
                        country_row.loc[
                            :, "Gross primary education enrollment (%)"
                        ].item()
                        < 100
                    ):
                        points -= 3
                    elif (
                        country_row.loc[
                            :, "Gross primary education enrollment (%)"
                        ].item()
                        <= 90
                    ):
                        points -= 5
                    if (
                        country_row.loc[
                            :, "Gross tertiary education enrollment (%)"
                        ].item()
                        < 10
                    ):
                        points -= 5
                    if country_row.loc[:, "Physicians per thousand"].item() > 4:
                        points += 3
                    elif country_row.loc[:, "Physicians per thousand"].item() < 0.1:
                        points -= 3

                evaluate_education()

                def evaluate_health():
                    """Global variable points"""
                    global points

                    """Double calculations"""
                    if country_row.loc[:, "Life expectancy"].item() >= 70:
                        points += 7
                    elif country_row.loc[:, "Life expectancy"].item() >= 65:
                        points += 3
                    if (
                        country_row.loc[:, "Infant mortality"].item() <= 6
                        and country_row.loc[:, "Maternal mortality ratio"].item() <= 50
                    ):
                        points += 7
                    elif (
                        country_row.loc[:, "Infant mortality"].item() <= 20
                        and country_row.loc[:, "Maternal mortality ratio"].item() <= 100
                    ):
                        points += 3

                    """Individual calculations"""
                    if country_row.loc[:, "Life expectancy"].item() > 80:
                        points += 3
                    elif country_row.loc[:, "Life expectancy"].item() < 60:
                        points -= 5
                    if country_row.loc[:, "Infant mortality"].item() > 30:
                        points -= 3
                    elif country_row.loc[:, "Infant mortality"].item() > 50:
                        points -= 5

                evaluate_health()

                def evaluate_enviroment():
                    """Global variable points"""
                    global points

                    """Double conditions"""
                    if (
                        country_row.loc[:, "Co2-Emissions"].item() <= 30000
                        and country_row.loc[:, "CO2-Emissions/person"].item() <= 350
                    ):
                        points += 5
                    elif (
                        country_row.loc[:, "Co2-Emissions"].item() <= 75000
                        and country_row.loc[:, "CO2-Emissions/person"].item() <= 500
                    ):
                        points += 3

                    """Single conditions"""
                    if country_row.loc[:, "Forested Area (%)"].item() > 30:
                        points += 3
                    if country_row.loc[:, "Forested Area (%)"].item() <= 10:
                        points -= 3

                evaluate_enviroment()

            else:
                raise ValueError(f"Country {c} has null values")

            # check points
            if points > 32:
                print({c: "Pretty nice country to live"})
            elif points > 24:
                print({c: "Nice country to live"})
            elif points > 15:
                print({c: "Not bad at all to live"})
            elif points > 8:
                print({c: "Bad country to live"})
            else:
                print({c: "Very bad country to live"})

    else:
        raise TypeError("Country must be a string or a list of strings")

