import pandas as pd
import os
import pyarrow.parquet as pq
import subprocess

cache_file = 'stock_data_cache.parquet'
if not os.path.isfile(cache_file):
    # If the cached file does not exist, generate it
    subprocess.run(["python", "generate_stocks_csv.py"])

# Read the Parquet file into a PyArrow Table
table = pq.read_table(cache_file)

# Convert the PyArrow Table to a DataFrame
data = table.to_pandas()

data.dropna(axis=1, how='all', inplace=True)

# Calculate the day of the week and store it in a new column 'Day_of_Week'
data['Day_of_Week'] = data.index.dayofweek

print(data.head)

# Loop through each stock symbol and fill missing values accordingly
for column in data.columns[:-1]:  # Exclude the 'Day_of_Week' column
    is_weekday = data['Day_of_Week'] < 5  # True for weekdays (0 to 4)
    is_weekend = ~is_weekday  # True for weekends (5 or 6)

    # Interpolate missing values for weekdays
    data[column].where(is_weekday, data[column].interpolate(method='linear'), inplace=True)

    # Forward fill missing values for weekends
    data[column].where(is_weekend, data[column].ffill(), inplace=True)
6
# Drop the 'Day_of_Week' column as it's no longer needed
data.drop(columns=['Day_of_Week'], inplace=True)

print(data)
missing_values = data.isna().sum()
print(missing_values)









