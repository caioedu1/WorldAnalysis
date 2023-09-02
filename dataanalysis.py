import matplotlib.pyplot as plt
import pandas as pd
import locale
from create_index import QOLindex
from functions import data_clean
import plotly.express as px

"""Database links:
https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023
obs: data may not be 100% accurate, but the main purpose of this project is just show my abilities in data analysis,
so any information extracted is exclusively based in this database."""

"""world-data-2023.csv analysis"""
# configure locale
locale.setlocale(locale.LC_ALL, "en_US.UTF-8")

# Process files
data = "world-data-2023.csv"
read_data = pd.read_csv(data)
df = pd.DataFrame(read_data)
# Data Clean
df = data_clean(df)

# transform csv file into xlsx file for visualization purposes
df.to_excel("world-data-2023.xlsx", index=False)


"""General informations"""
def general_info():
    
    """Task 1: Identify the country with the highest density, the country with the lowest density and
    the average world population density"""
    max_dens = df["Density (P/Km2)"].max()
    min_dens = df["Density (P/Km2)"].min()
    country_high_dens = df.loc[df["Density (P/Km2)"].idxmax(), "Country"]
    country_low_dens = df.loc[df["Density (P/Km2)"].idxmin(), "Country"]
    avg_dens = df["Density (P/Km2)"].mean()
    
    
    """Task 2: Identify the top 5 countries with the highest armed forces, and 
    the top 5 countries with the lowest armed forces"""
    
    smallestAF = df.sort_values(by="Armed Forces size", ascending=True).dropna().head(5)
    countries_smallest_AF = smallestAF[["Country", "Armed Forces size"]].reset_index(drop=True)
    countries_smallest_AF.index += 1
    highestAF = df.sort_values(by="Armed Forces size", ascending=False).dropna(subset=["Armed Forces size"]).head(5)
    countries_highest_AF = highestAF[["Country", "Armed Forces size"]].reset_index(drop=True)
    countries_highest_AF.index += 1

    """Task 3: Find the country with the highest birth rate, the country with the lowest birth rate and
    the average world birth rate"""
    max_br = df["Birth Rate"].max()
    min_br = df["Birth Rate"].min()
    country_high_br = df.loc[df["Birth Rate"].idxmax(), "Country"]
    country_low_br = df.loc[df["Birth Rate"].idxmin(), "Country"]
    avg_birth_rate = df["Birth Rate"].mean()


    """Task 4: Find the country with the highest primary school enrollment rate,
    the country with the lowest primary school enrollment rate,
    and the avg primary school enrollment rate."""
    avg_primary_education = df["Gross primary education enrollment (%)"].mean()
    highest_primary_education = df["Gross primary education enrollment (%)"].max()
    lowest_primary_education = df["Gross primary education enrollment (%)"].min()
    high_countries_PE = df.loc[df["Gross primary education enrollment (%)"].idxmax(), "Country"]
    low_countries_PE = df.loc[df["Gross primary education enrollment (%)"].idxmin(), "Country"]

    """Task 5: Find the country with the highest tertiary school enrollment rate,
    the country with the lowest tertiary school enrollment rate,
    and the avg tertiary school enrollment rate."""
    avg_tertiary_education = df["Gross tertiary education enrollment (%)"].mean()
    highest_tertiary_education = df["Gross tertiary education enrollment (%)"].max()
    lowest_tertiary_education = df["Gross tertiary education enrollment (%)"].min()
    high_countries_TE = df.loc[df["Gross tertiary education enrollment (%)"].idxmax(), "Country"]
    low_countries_TE = df.loc[df["Gross tertiary education enrollment (%)"].idxmin(), "Country"]
    
    """Task 6: Identify what is the top 3 most spoken language in the world."""
    spoken = df.groupby("Official language").size()
    top_languages = spoken.sort_values(ascending=False).head(3).to_string()
    top_languages = '\n'.join(top_languages.split('\n')[1:])
    
    """Task 7: Make a full analysis of how GDP per capita is related with unemployement rate, 
    life expectancy, CPI and others indicators."""
    less_GDPpercapita = df[df["GDP per capita"] < 700]
    sort_less_GDPpc = less_GDPpercapita.sort_values(by="GDP per capita", ascending=True)
    high_GDPpercapita = df[df["GDP per capita"] > 50000]
    sort_high_GDPpc = high_GDPpercapita.sort_values(by="GDP per capita", ascending=True)

    highGDPpc_AVGunemployement = sort_high_GDPpc["Unemployment rate"].mean()
    lowerGDPpc_AVGunemployement = sort_less_GDPpc["Unemployment rate"].mean()
    highGDPpc_AVGtaxrevenue = sort_high_GDPpc["Tax revenue (%)"].mean()
    lowerGDPpc_AVGtaxrevenue = sort_less_GDPpc["Tax revenue (%)"].mean()
    highGDPpc_AVGtotaltax = sort_high_GDPpc["Total tax rate"].mean()
    lowerGDPpc_AVGtotaltax = sort_less_GDPpc["Total tax rate"].mean()
    highGDPpc_AVGle = sort_high_GDPpc["Life expectancy"].mean()
    lowerGDPpc_AVGle = sort_less_GDPpc["Life expectancy"].mean()
    
    """Task 8: Find the average life expectancy of the country with the highest out of pocket health expenditure"""
    # highOOPHE_avgLE = df.loc[df["Out of pocket health expenditure"].idxmax, "Life expectancy"]
    
    
    """Write all the informations in analysis.txt"""
    content = f"""General analysis of some indicators
    
Population Density
Average world population density: {avg_dens:.1f}
The country with the highest population density is {country_high_dens} with a density of {max_dens}
The country with the lowest population density is {country_low_dens} with a density of {min_dens}

Armed Forces
The top 5 countries with the highest Armed Forces are: 
{countries_highest_AF}
The top 5 countries with the smallest Armed Forces are: 
{countries_smallest_AF}

Birth Rate
Average birth rate: {avg_birth_rate:.2f}
The country with the highest birth rate is {country_high_br} with a birth rate of {max_br}
The country with the lowest birth rate is {country_low_br} with a birth rate of {min_br}

Primary Education enrollment rate
Average primary education enrollment rate: {avg_primary_education:.2f}%
Country with the highest primary education enrollment rate: {high_countries_PE} with an rate of {highest_primary_education}%
Country with the lowest primary education enrollment rate: {low_countries_PE} with a rate of {lowest_primary_education}%

Tertiary Education enrollment rate
Average primary education enrollment rate: {avg_tertiary_education:.2f}%
Country with the highest primary education enrollment rate: {high_countries_TE} with an rate of {highest_tertiary_education}%
Country with the lowest primary education enrollment rate: {low_countries_TE} with a rate of {lowest_tertiary_education}%

Official languages
The top 3 widely spoken languages in the world are:
{top_languages}

-----------------------------------------------------------------------------------------------------------------------------------------------------
Analysis of how GDP per capita are related and influence to some other indicators:

Average life expectancy in countries with higher GDP per capita: {round(highGDPpc_AVGle)}
Average life expectancy in countries with lower GDP per capita: {round(lowerGDPpc_AVGle)}
Average unemployment rate in countries with higher GDP per capita: {highGDPpc_AVGunemployement:.2f}%
Average unemployment rate in countries with lower GDP per capita: {lowerGDPpc_AVGunemployement:.2f}%
Average tax revenue percentage in countries with higher GDP per capita: {highGDPpc_AVGtaxrevenue:.2f}%
Average tax revenue percentage in countries with lower GDP per capita: {lowerGDPpc_AVGtaxrevenue:.2f}%
Average total tax rate percentage in countries with higher GDP per capita: {highGDPpc_AVGtotaltax:.2f}%
Average total tax rate percentage in countries with lower GDP per capita: {lowerGDPpc_AVGtotaltax:.2f}%

Note 1: Life expectancy in countries with the highest GDP per capita is, on average, 20 years higher than in countries with the lowest GDP.

Note 2: CPI in countries with higher GDP in the range of 100 to 120, while countries with lower
GDP has a wider range, from 100 to 1344 in Sudan's case.

Note 3: An interesting fact is that countries with lower levels of GDP per capita
have an average unemployment rate lower than the average unemployment rate of countries with higher levels of
GDP per capita.

Note 4: We observe that countries with higher GDP per capita capture almost twice as much taxes as countries
with lower GDP per capita.

Note 5: Countries with higher per capita GDP have lower corporate tax levels,
while countries with lower GDP per capita have lower levels of corporate taxes.

Note 6: Another thing we can observe is that most of the countries with the lowest GDP per capita are
located in the African continent, while the countries with the highest GDP are mainly in Europe/West.
"""
    with open("analysis.txt", "w") as f:
        f.write(content)
general_info()


"""Plot tasks"""


"""Task 1: Identify the top 5 countries with the highest GDP (Gross Domestic Product).
Create a table of these countries containing gross primary education enrollment, unemployment rate,
labor force participation, CPI and life expectancy."""
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


"""Task 8: Identify the top 5 countries with the highest inflation rates and
the top 5 countries with the lowest inflation rates.
Also, get the CPI Change (%) of all countries that match those queries."""
cpi_analysis = df[["Country", "CPI", "CPI Change (%)"]]
sort_cpi_analysis = cpi_analysis.sort_values(by="CPI", ascending=True)
sort_cpi_analysis = sort_cpi_analysis.dropna(subset=["Country", "CPI"])

def show_inflation_rate():
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


show_inflation_rate()

# Task 9: Identify all the countries with the top 10 highest urban population,
# as well as all the countries with the top 10 lowest urban population.
# Also, get the top 5 countries with the highest and top 10 countries with the lowest agricultural land percentage.
urban_df = pd.DataFrame(df[["Country", "Urban_population"]])
sort_urban_lowest = urban_df.sort_values(by="Urban_population", ascending=True).head(10)
sort_urban_highest = urban_df.sort_values(by="Urban_population", ascending=False).head(
    10
)

agricultural_df = pd.DataFrame(df[["Country", "Agricultural Land (%)"]])
sort_agricultural_lowest = agricultural_df.sort_values(
    by="Agricultural Land (%)", ascending=True
).head(10)
sort_agricultural_highest = agricultural_df.sort_values(
    by="Agricultural Land (%)", ascending=False
).head(10)


def show_urbanPopulation():
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.bar(sort_urban_lowest["Country"], sort_urban_lowest["Urban_population"])
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Urban_population", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 lowest urban populations", fontsize=14)

    plt.subplot(2, 2, 2)
    plt.bar(sort_urban_highest["Country"], sort_urban_highest["Urban_population"])
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Urban_population", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 highest urban populations", fontsize=14)

    plt.subplot(2, 2, 3)
    plt.bar(
        sort_agricultural_lowest["Country"],
        sort_agricultural_lowest["Agricultural Land (%)"],
    )
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Agricultural Land (%)", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 lowest agricultural lands", fontsize=14)

    plt.subplot(2, 2, 4)
    plt.bar(
        sort_agricultural_highest["Country"],
        sort_agricultural_highest["Agricultural Land (%)"],
    )
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("Agricultural Land (%)", fontsize=10)
    plt.xticks(rotation=75)
    plt.title("Top 10 highest agricultural lands", fontsize=14)

    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.tight_layout()
    plt.savefig(
        r"C:\Users\Caioe\OneDrive\Área de Trabalho\Caio\GitHub\HarvardCS50\plot_figs\urban_populations.png",
        format="png",
        dpi=300,
    )
    plt.close()


show_urbanPopulation()


"""Task 5: Create a bar plot that demonstrates the total tax rate (TTR)
of the 10 countries with highest GDP."""
gdp10sorted = df.sort_values(by="GDP", ascending=False)
ten_highest_gdp = gdp10sorted[["Country", "Total tax rate"]].head(10)


def TTR_plot():
    plt.figure(figsize=(10, 6))
    plt.bar(ten_highest_gdp["Country"], ten_highest_gdp["Total tax rate"])
    plt.xlabel("Country", fontsize=10)
    plt.ylabel("CPI", fontsize=10)
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

"""Task 12: Create a scatter graph that shows the relationship between Forested Area and Co2-Emissions."""
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


"""Plot to an interactive html file. CS50.ai, or the famous DuckDebugger, helped me with the interactivity"""


def forest_co2_plot_png():
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


forest_co2_plot_png()
plt.show()
