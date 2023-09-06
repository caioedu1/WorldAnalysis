import matplotlib.pyplot as plt
import pandas as pd
import locale
from functions import data_clean
import plotly.express as px

"""
Database links:
https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023
"""

"""world-data-2023.csv analysis"""
# Configure locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

# Process files
data = "world-data-2023.csv"
read_data = pd.read_csv(data)
df = pd.DataFrame(read_data)

# Data clean
df = data_clean(df)

# transform csv file into xlsx file for visualization purposes
df.to_excel("world-data-2023.xlsx", index=False)


"""Extract general informations and pass them to analysis.txt"""


def general_info():
    """Task 1: Create a simple data frame containing the top 5 countries
    with the highest gasoline price and its respective Co2 Emissions."""
    gasoline_price_sort = (
        df.sort_values(by="Gasoline Price", ascending=False).dropna().head(5)
    )
    gasoline_price_sort = gasoline_price_sort[
        ["Country", "Gasoline Price", "Co2-Emissions"]
    ].reset_index(drop=True)

    """Task 2: Generate two data frames. One for the 5 countries with the
    lowest minimum wage and another for the 5 countries with the highest minimum wage.
    Include labor force participation (%) and the unemployment rate for each data frame."""
    high_minimum_wage = (
        df.sort_values(by="Minimum wage", ascending=False).dropna().head(5)
    )
    high_minimum_wage = high_minimum_wage[
        [
            "Country",
            "Minimum wage",
            "Labor force participation (%)",
            "Unemployment rate",
        ]
    ].reset_index(drop=True)
    low_minimum_wage = (
        df.sort_values(by="Minimum wage", ascending=True).dropna().head(5)
    )
    low_minimum_wage = low_minimum_wage[
        [
            "Country",
            "Minimum wage",
            "Labor force participation (%)",
            "Unemployment rate",
        ]
    ].reset_index(drop=True)

    """Task 3: Identify the top 5 countries with the biggest armed forces, and
    the top 5 countries with the smallest armed forces."""
    smallestAF = df.sort_values(by="Armed Forces size", ascending=True).dropna().head(5)
    countries_smallest_AF = smallestAF[["Country", "Armed Forces size"]].reset_index(
        drop=True
    )
    highestAF = (
        df.sort_values(by="Armed Forces size", ascending=False)
        .dropna(subset=["Armed Forces size"])
        .head(5)
    )
    countries_highest_AF = highestAF[["Country", "Armed Forces size"]].reset_index(
        drop=True
    )

    """Task 4: Identify the country with the highest density, the country with the lowest density, and
    the average world population density."""
    max_dens = df["Density (P/Km2)"].max()
    min_dens = df["Density (P/Km2)"].min()
    country_high_dens = df.loc[df["Density (P/Km2)"].idxmax(), "Country"]
    country_low_dens = df.loc[df["Density (P/Km2)"].idxmin(), "Country"]
    avg_dens = df["Density (P/Km2)"].mean()

    """Task 5: Find the country with the highest birth rate, the country with the lowest birth rate, and
    the average world birth rate."""
    max_br = df["Birth Rate"].max()
    min_br = df["Birth Rate"].min()
    country_high_br = df.loc[df["Birth Rate"].idxmax(), "Country"]
    country_low_br = df.loc[df["Birth Rate"].idxmin(), "Country"]
    avg_birth_rate = df["Birth Rate"].mean()

    """Task 6: Calculate the average infant mortality rate for countries that
    have a number of physicians per thousand above the global average and the average
    infant mortality for countries that have a number of physicians per thousand that is half of the global mean."""
    avg_phythousand = df["Physicians per thousand"].mean()
    avg_infant_above_phys = df.loc[
        df["Physicians per thousand"] > avg_phythousand, "Infant mortality"
    ].mean()
    avg_infant_half_phys = df.loc[
        df["Physicians per thousand"] < (avg_phythousand / 2), "Infant mortality"
    ].mean()

    """Task 7: Find the country with the highest primary school enrollment rate,
    the country with the lowest primary school enrollment rate,
    and the average primary school enrollment rate."""
    avg_primary_education = df["Gross primary education enrollment (%)"].mean()
    highest_primary_education = df["Gross primary education enrollment (%)"].max()
    lowest_primary_education = df["Gross primary education enrollment (%)"].min()
    high_countries_PE = df.loc[
        df["Gross primary education enrollment (%)"].idxmax(), "Country"
    ]
    low_countries_PE = df.loc[
        df["Gross primary education enrollment (%)"].idxmin(), "Country"
    ]

    """Task 8: Find the country with the highest tertiary school enrollment rate,
    the country with the lowest tertiary school enrollment rate,
    and the average tertiary school enrollment rate."""
    avg_tertiary_education = df["Gross tertiary education enrollment (%)"].mean()
    highest_tertiary_education = df["Gross tertiary education enrollment (%)"].max()
    lowest_tertiary_education = df["Gross tertiary education enrollment (%)"].min()
    high_countries_TE = df.loc[
        df["Gross tertiary education enrollment (%)"].idxmax(), "Country"
    ]
    low_countries_TE = df.loc[
        df["Gross tertiary education enrollment (%)"].idxmin(), "Country"
    ]

    """Task 9: Determine which three languages are the primary languages in the most countries."""
    spoken = df.groupby("Official language").size()
    top_languages = spoken.sort_values(ascending=False).head(3).to_string()
    top_languages = "\n".join(top_languages.split("\n")[1:])

    """Task 10: Conduct an analysis of how GDP per capita is
    correlated with the unemployment rate, life expectancy, CPI, and other indicators."""
    low_GDPpercapita = df.sort_values(by="GDP per capita", ascending=True).head(20)
    high_GDPpercapita = df.sort_values(by="GDP per capita", ascending=False).head(20)
    lower_sel_GDPcols = low_GDPpercapita[
        [
            "Country",
            "GDP per capita",
            "Unemployment rate",
            "Life expectancy",
            "CPI",
            "Total tax rate",
            "Tax revenue (%)",
        ]
    ].reset_index(drop=True)
    high_sel_GDPcols = high_GDPpercapita[
        [
            "Country",
            "GDP per capita",
            "Unemployment rate",
            "Life expectancy",
            "CPI",
            "Total tax rate",
            "Tax revenue (%)",
        ]
    ].reset_index(drop=True)

    highGDPpc_AVGunemployement = high_GDPpercapita["Unemployment rate"].mean()
    lowGDPpc_AVGunemployement = low_GDPpercapita["Unemployment rate"].mean()
    highGDPpc_AVGtaxrevenue = high_GDPpercapita["Tax revenue (%)"].mean()
    lowGDPpc_AVGtaxrevenue = low_GDPpercapita["Tax revenue (%)"].mean()
    highGDPpc_AVGtotaltax = high_GDPpercapita["Total tax rate"].mean()
    lowGDPpc_AVGtotaltax = low_GDPpercapita["Total tax rate"].mean()
    highGDPpc_AVGle = high_GDPpercapita["Life expectancy"].mean()
    lowGDPpc_AVGle = low_GDPpercapita["Life expectancy"].mean()
    highGDPpc_AVGcpi = high_GDPpercapita["CPI"].mean()
    lowGDPpc_AVGcpi = low_GDPpercapita["CPI"].mean()

    """Configure df showing so it can be properly written in analysis.txt"""
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    """Write all the informations in analysis.txt"""
    content = f"""Comprehensive Examination of Selected Indicators

Gasoline Price
Data frame containing the country, gasoline price, and CO2 emissions sorted by the five costly gasoline prices
{gasoline_price_sort}

Minimum wage
Data frame containing the country, minimum wage, labor force participation, and unemployment rate, sorted by high levels of minimum wage
{high_minimum_wage}
Data frame containing the country, minimum wage, labor force participation, and unemployment rate, sorted by low levels of minimum wage
{low_minimum_wage}

Armed Forces
The top 5 countries with the highest armed forces are:
{countries_highest_AF}
The top 5 countries with the smallest armed forces are:
{countries_smallest_AF}

Population Density
Average world population density: {avg_dens:.1f}
The country with the highest population density is {country_low_dens} with a density of {min_dens}
The country with the lowest population density is {country_high_dens} with a density of {max_dens}

Birth Rate
Average birth rate: {avg_birth_rate:.2f}
The country with the highest birth rate is {country_high_br} with a birth rate of {max_br}
The country with the lowest birth rate is {country_low_br} with a birth rate of {min_br}

Infant mortality
Average infant mortality rates in nations with physician-to-population ratios surpassing the global mean: {avg_infant_above_phys:.2f}
Average infant mortality rates in nations with physician-to-population ratios below half the global mean: {avg_infant_half_phys:.2f}

Primary education enrollment rate
Average global primary education enrollment rate: {avg_primary_education:.2f}%
Country with the highest primary education enrollment rate: {high_countries_PE} with a rate of {highest_primary_education}%
Country with the lowest primary education enrollment rate: {low_countries_PE} with a rate of {lowest_primary_education}%

Tertiary education enrollment rate
Average global tertiary education enrollment rate: {avg_tertiary_education:.2f}%
Country with the highest tertiary education enrollment rate: {high_countries_TE} with a rate of {highest_tertiary_education}%
Country with the lowest tertiary education enrollment rate: {low_countries_TE} with a rate of {lowest_tertiary_education}%

Official languages
The top 3 widely spoken languages in the world are:
{top_languages}

-----------------------------------------------------------------------------------------------------------------------------------------------------
An examination of the interrelationship and influence of GDP per capita on various indicators

Mean values of diverse indicators within nations characterized by high and low GDP per capita.
Average life expectancy in countries with higher GDP per capita: {round(highGDPpc_AVGle)}
Average life expectancy in countries with lower GDP per capita: {round(lowGDPpc_AVGle)}
Average unemployment rate in countries with higher GDP per capita: {highGDPpc_AVGunemployement:.2f}%
Average unemployment rate in countries with lower GDP per capita: {lowGDPpc_AVGunemployement:.2f}%
Average tax revenue percentage in countries with higher GDP per capita: {highGDPpc_AVGtaxrevenue:.2f}%
Average tax revenue percentage in countries with lower GDP per capita: {lowGDPpc_AVGtaxrevenue:.2f}%
Average total tax rate percentage in countries with higher GDP per capita: {highGDPpc_AVGtotaltax:.2f}%
Average total tax rate percentage in countries with lower GDP per capita: {lowGDPpc_AVGtotaltax:.2f}%
Average CPI in countries with higher GDP per capita: {highGDPpc_AVGcpi:.2f}
Average CPI in countries with lower GDP per capita: {lowGDPpc_AVGcpi:.2f}


Data frame comprising indicators associated with countries exhibiting higher GDP per capita.
{high_sel_GDPcols}

Data frame comprising indicators associated with countries exhibiting lower GDP per capita.
{lower_sel_GDPcols}


Observations regarding the correlation between GDP per capita and selected indicators.
Note 1:
Life expectancy in countries with the highest GDP per capita is,
on average, 20 years higher than in countries with the lowest GDP.

Note 2:
The Consumer Price Index (CPI) in nations boasting higher GDP levels typically spans from 100 to 120,
whereas countries with lower GDP tend to display a wider range, reaching as high as 1344 in the case of Sudan.

Note 3:
Nations characterized by a lower GDP per capita often exhibit a higher
average unemployment rate compared to those nations with a higher GDP per capita.
Nevertheless, it is imperative to acknowledge that numerous countries with low GDP per capita maintain an
unemployment rate lower than their counterparts with a higher unemployment rate. Consequently, it is evident
that while GDP per capita may exert an influence on the unemployment rate, its impact is not necessarily substantial.

Note 4:
It's evident that countries with a higher GDP per capita collect nearly
double the amount of taxes compared to countries with lower GDP per capita.

Note 5:
Countries with a higher per capita GDP tend to have lower corporate tax rates,
whereas countries with a lower GDP per capita typically impose lower corporate taxes.

Note 6:
Another noteworthy observation is that the majority of countries with the lowest GDP per capita
are located on the African continent, while those with the highest GDP are primarily found in Europe and the West.

Note 7:
It becomes evident that the CPI in nations characterized by the lowest GDP per capita
surpasses that of countries with the highest GDP per capita by a margin exceeding twofold.
"""
    with open("analysis.txt", "w") as f:
        f.write(content)

    """Reseting options to default"""
    pd.reset_option("display.max_columns")
    pd.reset_option("display.width")


general_info()


"""Plot tasks"""


"""Task 1: Identify the top 5 countries with the highest GDP.
Create a table that includes gross primary education enrollment, unemployment rate,
labor force participation, Consumer Price Index (CPI), and life expectancy for these countries."""
high_gdp = df.sort_values(by="GDP", ascending=False).head(5)
high_gdp["GDP"] = high_gdp["GDP"].apply(lambda x: locale.currency(x, grouping=True))
high_gdp = high_gdp[
    [
        "Country",
        "GDP",
        "Life expectancy",
        "CPI",
        "Labor force participation (%)",
        "Unemployment rate",
        "Gross primary education enrollment (%)",
    ]
]
gdp_highGDP = high_gdp["GDP"]


def top5GDP_info():
    fig, ax = plt.subplots(figsize=(25, 15))
    ax.axis("off")

    cell_text = high_gdp.values.tolist()
    for row in cell_text:
        del row[0]
    name_mapping = {"Gross primary education enrollment (%)": "GPEE (%)"}
    columns = [name_mapping.get(col, col) for col in high_gdp.columns]
    columns.remove("Country")
    rows = high_gdp["Country"].tolist()

    table = plt.table(
        cellText=cell_text,
        rowLabels=rows,
        colLabels=columns,
        loc="center",
        edges="closed",
        cellLoc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(15)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_fontsize(17)
        cell.set_width(0.175)
        cell.set_height(0.12)
        cell.set_linewidth(0.5)
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\top5GDPinfo.png",
        format="png",
        dpi=300,
    )
    plt.close()


top5GDP_info()


"""Task 2: Identify the top 5 countries with the highest inflation rates and the top 5 countries with
the lowest inflation rates."""
cpi_analysis = df[["Country", "CPI"]]
sort_cpi_analysis = cpi_analysis.sort_values(by="CPI", ascending=True)
sort_cpi_analysis = sort_cpi_analysis.dropna(subset=["Country", "CPI"])


def inflation_rate_plot():
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(sort_cpi_analysis["Country"].head(5), sort_cpi_analysis["CPI"].head(5))
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("CPI", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Countries with low inflation rate", fontsize=14)

    plt.subplot(1, 2, 2)
    plt.bar(sort_cpi_analysis["Country"].tail(5), sort_cpi_analysis["CPI"].tail(5))
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("CPI", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Countries with high inflation rate", fontsize=14)

    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.tight_layout()
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\inflation_rates.png",
        format="png",
        dpi=300,
    )
    plt.close()


inflation_rate_plot()

"""Task 3: Identify all the countries with the ten highest urban populations,
as well as all the countries with the ten lowest urban populations."""
sort_urban_lowest = df[["Country", "Urban population"]].sort_values(
    by="Urban population", ascending=True
    ).head(10)
sort_urban_highest = df[["Country", "Urban population"]].sort_values(
    by="Urban population", ascending=False
    ).head(10)


def urban_population_plot():
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(sort_urban_lowest["Country"], sort_urban_lowest["Urban population"])
    plt.ylabel("Urban Population", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 lowest urban populations", fontsize=14)

    plt.subplot(1, 2, 2)
    plt.bar(sort_urban_highest["Country"], sort_urban_highest["Urban population"])
    plt.ylabel("Urban Population", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 highest urban populations", fontsize=14)

    plt.tight_layout()
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\urbanplot.png",
        format="png",
        dpi=300,
    )
    plt.close()


urban_population_plot()


"""Task 4: Obtain information on the top 10 countries with the highest agricultural land percentage and
the top 10 countries with the lowest agricultural land percentage."""
sort_agricultural_lowest = df[["Country", "Agricultural Land (%)"]].sort_values(
    by="Agricultural Land (%)", ascending=True
).head(10)
sort_agricultural_highest = df[["Country", "Agricultural Land (%)"]].sort_values(
    by="Agricultural Land (%)", ascending=False
).head(10)


def agricultural_land_plot():
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(
        sort_agricultural_lowest["Country"],
        sort_agricultural_lowest["Agricultural Land (%)"],
    )
    plt.ylabel("Agricultural Land (%)", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 lowest agricultural lands", fontsize=14)

    plt.subplot(1, 2, 2)
    plt.bar(
        sort_agricultural_highest["Country"],
        sort_agricultural_highest["Agricultural Land (%)"],
    )
    plt.ylabel("Agricultural Land (%)", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 highest agricultural lands", fontsize=14)

    plt.tight_layout()
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\agriculturalplot.png",
        format="png",
        dpi=300,
    )
    plt.close()


agricultural_land_plot()

"""Task 5: Produce a bar chart depicting the Total Tax Rate (TTR) for the top 10 countries with the highest GDP."""
gdp10sorted = df.sort_values(by="GDP", ascending=False)
ten_highest_gdp = gdp10sorted[["Country", "Total tax rate"]].head(10)

def TTR_plot():
    plt.figure(figsize=(10, 6))
    plt.bar(ten_highest_gdp["Country"], ten_highest_gdp["Total tax rate"])
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Total Tax Rate", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Total Tax Rate of the 10 countries with the highest GDP", fontsize=14)

    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.tight_layout()
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\TTRinCountriesHighestGDP.png",
        format="png",
        dpi=300,
    )
    plt.close()


TTR_plot()

"""Task 6: Generate a scatterplot illustrating the correlation between Forested Area and CO2 Emissions."""
max_x_value = 100
max_y_value = 10000000

"""Plot image to png file"""


def forest_co2_plot_png():
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df["Forested Area (%)"], df["Co2-Emissions"])
    plt.xlim(0, max_x_value)
    plt.ylim(0, max_y_value)
    plt.xlabel("Forested Area (%)", fontsize=10)
    plt.ylabel("CO2 Emissions", fontsize=10)

    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\forest_co2_plot.png",
        format="png",
        dpi=300,
    )
    plt.close()


forest_co2_plot_png()

"""Plot to an interactive html file."""


def forest_co2_plot_html():
    plt.figure(figsize=(10, 6))
    fig = px.scatter(
        df, x="Forested Area (%)", y="Co2-Emissions", hover_data=["Country"]
    )
    plt.xlim(0, max_x_value)
    plt.ylim(0, max_y_value)
    plt.xlabel("Forested Area (%)", fontsize=10)
    plt.ylabel("CO2 Emissions", fontsize=10)

    fig.write_html(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\forest_co2_plot.html"
    )
    plt.close()


forest_co2_plot_html()
