import pandas as pd

# Databases links:
# https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023

# Create an index that determine if a country is well developed or not.
# Process files
data = "world-data-2023.csv"
read_data = pd.read_csv(data)
df = pd.DataFrame(read_data)
