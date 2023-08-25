import pandas as pd

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
df['Forested Area (%)'] = pd.to_numeric(df['Forested Area (%)'].str.replace('%', ''))
df['Gross primary education enrollment (%)'] = pd.to_numeric(df['Gross primary education enrollment (%)'].str.replace('%', ''))
df['Urban_population'] = pd.to_numeric(df['Urban_population'].str.replace(',', ''))
df['Agricultural Land (%)'] = pd.to_numeric(df['Agricultural Land (%)'].str.replace('%', ''), errors='coerce')
df['Population'] = pd.to_numeric(df['Population'].str.replace(',', ''))
df['Country'] = df['Country'].str.replace('S�����������', 'Sao Tome and Principe')
df['Unemployment rate'] = pd.to_numeric(df['Unemployment rate'].str.replace('%', ''))
df['Tax revenue (%)'] = pd.to_numeric(df['Tax revenue (%)'].str.replace('%', ''))
df['Total tax rate'] = pd.to_numeric(df['Total tax rate'].str.replace('%', ''))
df['Physicians per thousand'] = pd.to_numeric(df['Physicians per thousand'])
df['Gross tertiary education enrollment (%)'] = pd.to_numeric(df['Gross tertiary education enrollment (%)'].str.replace('%', ''))
df['Co2-Emissions'] = pd.to_numeric(df['Co2-Emissions'].str.replace(',', ''))
df['Land Area(Km2)'] = pd.to_numeric(df['Land Area(Km2)'].str.replace('"', '').str.replace(',', ''))

# Create average CO2 Emissions per person
df['CO2-Emissions/person'] = df['Population'] / df['Co2-Emissions']

# Create GDP per capita column
df['GDP per capita'] = df['GDP'] / df['Population']

# Create a simple enviroment index
# df['Land Area per capita'] = df['Population'] / df['Land Area(Km2)']
df['Forested Area (Km2)'] = df['Forested Area (%)'] * df['Land Area(Km2)'] / 100 

df['Environmental Quality Index'] = (df['Forested Area (Km2)'] / df['Co2-Emissions']) / 100

df['Normalized EQI'] = 0 + (((df['Environmental Quality Index'] - df['Environmental Quality Index'].min()) * (
    (100 - 0) ) / (df['Environmental Quality Index'].max() - df['Environmental Quality Index'].min()))
) * 100

# df.to_excel("aaaaaa.xlsx", index=False)

# Create indexes
def human_development_index(country):
    if isinstance(country, list) and all(isinstance(i, str) for i in country) or (
        isinstance(country, str)
    ):
        points = 0
        if not isinstance(country, list):
            country = [country]
        for c in country:
            country_row = df[df['Country'] == c]

            if not pd.isnull(country_row[['Gross primary education enrollment (%)', 'GDP per capita']]).any().any():
                if country_row.loc[:, 'Gross primary education enrollment (%)'].item() >= 100 and country_row.loc[:, 'GDP per capita'].item() >= 45000:
                    points += 7
                elif country_row.loc[:, 'Gross primary education enrollment (%)'].item() >= 95 and country_row.loc[:, 'GDP per capita'].item() >= 25000:
                    points += 3
                else:
                    points += 1
            else:
                raise ValueError('Country has null values')

            if not pd.isnull(country_row[['Life expectancy', 'Unemployment rate']]).any().any():
                if country_row.loc[:, 'Life expectancy'].item() >= 70 and country_row.loc[:, 'Unemployment rate'].item() <= 6:
                    points += 7
                elif country_row.loc[:, 'Life expectancy'].item() >= 65 and country_row.loc[:, 'Unemployment rate'].item() <= 10:
                    points += 3
                else:
                    points += 1
            else:
                raise ValueError('Country has null values')

            if not pd.isnull(country_row[['Tax revenue (%)', 'Total tax rate']]).any().any():
                if country_row.loc[:, 'Total tax rate'].item() < 50 or country_row.loc[:, 'Tax revenue (%)'].item() < 15:
                    points += 3
                elif country_row.loc[:, 'Total tax rate'].item() < 65 or country_row.loc[:, 'Tax revenue (%)'].item() < 20:
                    points += 1
            else:
                raise ValueError('Country has null values')

            if not pd.isnull(country_row[['Infant mortality', 'Maternal mortality ratio']]).any().any():
                if country_row.loc[:, 'Infant mortality'].item() <= 6 and country_row.loc[:, 'Maternal mortality ratio'].item() <= 50:
                    points += 7
                elif country_row.loc[:, 'Infant mortality'].item() <= 20 and country_row.loc[:, 'Maternal mortality ratio'].item() <= 100:
                    points += 3
                else:
                    points += 1
            else:
                raise ValueError('Country has null values')

            if not pd.isnull(country_row[['Gross tertiary education enrollment (%)', 'Physicians per thousand']]).any().any():
                if country_row.loc[:, 'Gross tertiary education enrollment (%)'].item() > 70 and country_row.loc[:, 'Physicians per thousand'].item() > 0.9:
                    points += 3
                elif country_row.loc[:, 'Gross tertiary education enrollment (%)'].item() > 50 and country_row.loc[:, 'Physicians per thousand'].item() > 0.5:
                    points += 1
            else:
                raise ValueError('Country has null values')
            
            # if not pd.isnull(country_row[df['Environmental Quality Index']]).any():
            #     if country_row.loc[:, 'Environmental Quality Index'].item() > 90
            
            # check points
            if points > 18:
                print({c: 'Nice country'})
            elif points > 12:
                print({c: 'Mid level country'})
            else:
                print({c: 'Bad country'})
    else:
        raise TypeError('Country must be a string or a list of strings')
        
def enviroment_index(country):
    if isinstance(country, list) and all(isinstance(i, str) for i in country) or (
        isinstance(country, str)
    ):
        if not isinstance(country, list):
            country = [country]
        for c in country:
            points = 0
            country_row = df[df['Country'] == c]
            
            if not pd.isnull(country_row['Forested Area (%)']).any():
                if country_row.loc[:, 'Forested Area (%)'].item() >= 40:
                    points += 7                    
                elif country_row.loc[:, 'Forested Area (%)'].item() >= 30:
                    points += 5
                elif country_row.loc[:, 'Forested Area (%)'].item() >= 20:
                    points += 3
                elif country_row.loc[:, 'Forested Area (%)'].item() > 5:
                    points += 1
                else:
                    points -= 3
            print(points)
            if not pd.isnull(country_row[['CO2-Emissions/person', 'Co2-Emissions']]).any().any():
                if country_row.loc[:, 'Co2-Emissions'].item() <= 10000 and country_row.loc[:, 'CO2-Emissions/person'].item() <= 300:
                    points += 7
                elif country_row.loc[:, 'Co2-Emissions'].item() <= 50000 and country_row.loc[:, 'CO2-Emissions/person'].item() <= 500:
                    points += 5
                if country_row.loc[:, 'Co2-Emissions'].item() >= 100000 and country_row.loc[:, 'CO2-Emissions/person'].item() > 1000:
                    points -= 3
            else:
                raise ValueError('Country has null values')
            print(points)
            # Here, I will consider density as a bad thing. Density can arguably mean good or bad things,
            # but general means bad things.
            if not pd.isnull(country_row['Density (P/Km2)']).any():
                if country_row.loc[:, 'Density (P/Km2)'].item() <= 25:
                    points += 3
                if country_row.loc[:, 'Density (P/Km2)'].item() >= 200:
                    points -= 1
                elif country_row.loc[:, 'Density (P/Km2)'].item() >= 300:
                    points -= 3
            else:
                raise ValueError('Country has null values')
            print(points)    
            
            if not pd.isnull(country_row['Normalized EQI']).any():
                if country_row.loc[:, 'Normalized EQI'].item() > 100:
                    points += 5
                elif country_row.loc[:, 'Normalized EQI'].item() > 70:
                    points += 3
                elif country_row.loc[:, 'Normalized EQI'].item() > 40:
                    points += 1
            print(points)

                    
            # check points
            if points > 15:
                print({c: 'Nice country'})
            elif points > 7:
                print({c: 'Mid level country'})
            else:
                print({c: 'Bad country'})
    else:
        raise TypeError('Country must be a string or a list of strings')
    
enviroment_index(['Sweden', 'Norway', 'Switzerland', 'United Kingdom', 'Brazil', 'China', 'Saudi Arabia', 'Russia', 'India'])  