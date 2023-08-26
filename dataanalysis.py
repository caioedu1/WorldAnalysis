import matplotlib.pyplot as plt
import pandas as pd
import locale
from create_index import human_development_index

# Database links:
# https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023
# obs: data may not be 100% accurate, but the main purpose of this project is just show my abilities in data analysis,
# so any information extracted is exclusively based in this database.

# world-data-2023.csv analysis
# configure locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Process files
data = "world-data-2023.csv"
read_data = pd.read_csv(data)
df = pd.DataFrame(read_data)
# Data Clean
pd.options.display.float_format = '{:.2f}'.format

df = df.rename(columns={"Agricultural Land( %)": "Agricultural Land (%)"})

df['Density (P/Km2)'] = pd.to_numeric(df.iloc[:, 1].str.replace('"', '').str.replace(' ', '').str.replace(',', '.'))
df['GDP'] = pd.to_numeric(df['GDP'].str.replace('[\$,]', '', regex=True).astype(float)).dropna()
df['Armed Forces size'] = pd.to_numeric(df['Armed Forces size'].str.replace('"', '').str.replace(',', ''))
df['Forested Area (%)'] = pd.to_numeric(df['Forested Area (%)'].str.replace('%', ''))
df['Gross primary education enrollment (%)'] = pd.to_numeric(df['Gross primary education enrollment (%)'].str.replace('%', ''))
df['CPI'] = pd.to_numeric(df['CPI'].str.replace(',', ''))
df['Urban_population'] = pd.to_numeric(df['Urban_population'].str.replace(',', ''))
df['Agricultural Land (%)'] = pd.to_numeric(df['Agricultural Land (%)'].str.replace('%', ''), errors='coerce')
df['Population'] = pd.to_numeric(df['Population'].str.replace(',', ''))
df['Country'] = df['Country'].str.replace('S�����������', 'Sao Tome and Principe')
df['Unemployment rate'] = pd.to_numeric(df['Unemployment rate'].str.replace('%', ''))
df['Tax revenue (%)'] = pd.to_numeric(df['Tax revenue (%)'].str.replace('%', ''))
df['Total tax rate'] = pd.to_numeric(df['Total tax rate'].str.replace('%', ''))
df['CPI Change (%)'] = pd.to_numeric(df['CPI Change (%)'].str.replace('%', '').str.replace('.', ''), errors='coerce') / 100
df['Co2-Emissions'] = pd.to_numeric(df['Co2-Emissions'].str.replace(',', ''))
df['Land Area(Km2)'] = pd.to_numeric(df['Land Area(Km2)'].str.replace('"', ''))

# transform csv file into xlsx file for visualization purposes
# df.to_excel("world-data-2023.xlsx", index=False)


df['CO2-Emissions/person'] = df['Population'] / df['Co2-Emissions']
print(df.loc[df['Country'] == 'Ethiopia', 'CO2-Emissions/person'])
# Task 1: Calculate the average world population density.
avg_dens = df['Density (P/Km2)'].mean()
print(f"Average world population density: {avg_dens:.1f}")

# Task 2: Identify the country with the highest GDP (Gross Domestic Product).
high_gdp_idx = df['GDP'].idxmax()
country_high_gdp = df.loc[high_gdp_idx, 'Country']
high_gdp = df.loc[high_gdp_idx, 'GDP']
high_gdpF = locale.currency(high_gdp, grouping=True)
print(f"The Country with the highest GDP is {country_high_gdp} with a GDP of {high_gdpF}")

# Task 3: Identify the country with the smallest Armed Forces.
smallestAF = df['Armed Forces size'].min()
smallestAF_idx = df['Armed Forces size'].idxmin()
country_smallest_AF = df.loc[smallestAF_idx,'Country']
print(f"The Country with the smallest Armed Forces is {country_smallest_AF} with an Armed Force of literally {smallestAF}!")

# Task 4: Calculate the average birth rate.
avg_birth_rate = df['Birth Rate'].mean()
print(f"Average birth rate: {avg_birth_rate:.2f}")

# Task 5: Find the country with the highest life expectancy.
highest_life_expectancy = df['Life expectancy'].max()
country_highest_LE = df.loc[df['Life expectancy'] == highest_life_expectancy, 'Country'].iloc[0]
print(f"The Country with the highest life expectancy is {country_highest_LE} with an expectancy of {highest_life_expectancy}")

# Task 6: Calculate the average percentage of forest area.
avg_forested_area = df['Forested Area (%)'].mean()
print(f"Global average percentage of forested area: {avg_forested_area:.2f}%")
print("-"*100)

# Task 7: Find the country with the highest, 
# the country with the lowest primary school, and the avg primary school enrollment rate.
avg_primary_education = df['Gross primary education enrollment (%)'].mean()
highest_primary_education = df['Gross primary education enrollment (%)'].max()
lowest_primary_education = df['Gross primary education enrollment (%)'].min()
highest_PE_idx = df['Gross primary education enrollment (%)'].idxmax()
lowest_PE_idx = df['Gross primary education enrollment (%)'].idxmin()
high_countries_PE = df.loc[highest_PE_idx, 'Country']
low_countries_PE = df.loc[lowest_PE_idx, 'Country']

print(f"Average primary education enrollment rate: {avg_primary_education:.2f}%")
print(f"Country with the highest primary education enrollment rate: {high_countries_PE} with an rate of {highest_primary_education}%")
print(f"Country with the lowest primary education enrollment rate: {low_countries_PE} with a rate of {lowest_primary_education}%")
print("-"*100)

# Task 8: Identify all the countries with an inflation rate higher than 300 
# and all the countries with an inflation rate less than 100. 
# Also, get the CPI Change (%) of all countries that match those queries.
cpi_higher = df.loc[df['CPI'] > 300, ['Country', 'CPI', 'CPI Change (%)']]
df_cpi_higher = pd.DataFrame(cpi_higher)
sort_higher_cpi = df_cpi_higher.sort_values(by='CPI')

cpi_lower = df.loc[df['CPI'] < 100, ['Country','CPI', 'CPI Change (%)']]
df_cpi_lower = pd.DataFrame(cpi_lower)
sort_lower_cpi = df_cpi_lower.sort_values(by='CPI')

def show_inflation_rate():
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.bar(df_cpi_lower['Country'], df_cpi_lower['CPI'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('CPI', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Countries with low inflation rate', fontsize=14)

    plt.subplot(1, 2, 2)
    plt.bar(df_cpi_higher['Country'], df_cpi_higher['CPI'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('CPI', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Countries with high inflation rate', fontsize=14)
    
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.tight_layout()
    plt.savefig('inflation_rates.png', format='png', dpi=300)

# show_inflation_rate()

# Task 9: Identify all the countries with the top 10 highest urban population,
# as well as all the countries with the top 10 lowest urban population. 
# Also, get the top 5 countries with the highest and top 10 countries with the lowest agricultural land percentage.
urban_df = pd.DataFrame(df[['Country', 'Urban_population']])
sort_urban_lowest = urban_df.sort_values(by='Urban_population', ascending=True).head(10)
sort_urban_highest = urban_df.sort_values(by='Urban_population', ascending=False).head(10)

agricultural_df = pd.DataFrame(df[['Country', 'Agricultural Land (%)']])
sort_agricultural_lowest = agricultural_df.sort_values(by='Agricultural Land (%)', ascending=True).head(10)
sort_agricultural_highest = agricultural_df.sort_values(by='Agricultural Land (%)', ascending=False).head(10)

def show_urbanPopulation():
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 2, 1)
    plt.bar(sort_urban_lowest['Country'], sort_urban_lowest['Urban_population'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('Urban_population', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Top 10 lowest urban populations', fontsize=14)
    
    plt.subplot(2, 2, 2)
    plt.bar(sort_urban_highest['Country'], sort_urban_highest['Urban_population'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('Urban_population', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Top 10 highest urban populations', fontsize=14)
    
    plt.subplot(2, 2, 3)
    plt.bar(sort_agricultural_lowest['Country'], sort_agricultural_lowest['Agricultural Land (%)'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('Agricultural Land (%)', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Top 10 lowest agricultural lands', fontsize=14)
    
    plt.subplot(2, 2, 4)
    plt.bar(sort_agricultural_highest['Country'], sort_agricultural_highest['Agricultural Land (%)'])
    plt.xlabel('Country', fontsize=10)
    plt.ylabel('Agricultural Land (%)', fontsize=10)
    plt.xticks(rotation=75)
    plt.title('Top 10 highest agricultural lands', fontsize=14)
    
    plt.subplots_adjust(hspace=0.5, wspace=0.5)
    plt.tight_layout()
    plt.savefig('urban_populations.png', format='png', dpi=300)
    
# show_urbanPopulation()


# Task 10: Add temporary GDP per capita.
# Make a full analysis of how unemployement rate, GDP, GDP per capita,
# life expectancy, CPI and other indicators are correlated.
df['GDP per capita'] = df['GDP'] / df['Population']
less_GDPpercapita = df[df['GDP per capita'] < 700]
sort_less_GDPpc = less_GDPpercapita.sort_values(by='GDP per capita', ascending=True)
select_columns = ['Country', 'Unemployment rate', 'GDP', 'GDP per capita', 'Life expectancy', 'CPI', 'Tax revenue (%)', 'Total tax rate']
print(sort_less_GDPpc[select_columns].reset_index(drop=True))
print("\n\n")

high_GDPpercapita = df[df['GDP per capita'] > 50000]
sort_high_GDPpc = high_GDPpercapita.sort_values(by='GDP per capita', ascending=True)
print(sort_high_GDPpc[select_columns].reset_index(drop=True))
print()

highGDPpc_AVGunemployement = sort_high_GDPpc['Unemployment rate'].mean()
print(f"Average unemployment rate in countries with higher GDP per capita: {highGDPpc_AVGunemployement:.2f}%")
lowerGDPpc_AVGunemployement = sort_less_GDPpc['Unemployment rate'].mean()
print(f"Average unemployment rate in countries with lower GDP per capita: {lowerGDPpc_AVGunemployement:.2f}%")

highGDPpc_AVGtaxrevenue = sort_high_GDPpc['Tax revenue (%)'].mean()
print(f"Average tax revenue percentage in countries with higher GDP per capita: {highGDPpc_AVGtaxrevenue:.2f}%")
lowerGDPpc_AVGtaxrevenue = sort_less_GDPpc['Tax revenue (%)'].mean()
print(f"Average tax revenue percentage in countries with lower GDP per capita: {lowerGDPpc_AVGtaxrevenue:.2f}%")

highGDPpc_AVGtotaltax = sort_high_GDPpc['Total tax rate'].mean()
print(f"Average total tax rate percentage in countries with higher GDP per capita: {highGDPpc_AVGtotaltax:.2f}%")
lowerGDPpc_AVGtotaltax = sort_less_GDPpc['Total tax rate'].mean()
print(f"Average total tax rate percentage in countries with lower GDP per capita: {lowerGDPpc_AVGtotaltax:.2f}%")
print('-'*100)  


