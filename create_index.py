import pandas as pd

# Databases links:
# https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023

# Create an index that determine if a country is well developed or not.
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


# Create index
def index(country):
    # High class country
    if df['Gross primary education enrollment (%)'] > 105 and df['GDP per capita'] > 
    
def create_index(country):
    if isinstance(country, str):
        select_country = df.loc[df['Country'] == country]
    elif isinstance(country, list) and all(isinstance(i, str) for i in country):
        select_country = df[df['Country'].isin(country)]
    else:
        raise TypeError('Country must be a string or a list of strings')
    
create_index(['Brazil', 'Afghanistan'])
