#!pip install yfinance --upgrade --no-cache-dir
#pip install pandas
#pip install matplotlib
#pip install numpy
#https://pypi.org/project/fix-yahoo-finance/


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from csv import reader
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import time
import datetime as dt
import pyarrow as pa
import pyarrow.parquet as pq

pd.options.mode.chained_assignment = None # default='warn'
# find the symbol (i.e., google the instrument + 'yahoo finance') to any data series you are interested at
# e.g., market/sector index ETF for your chosen country and various asset classes (e.g., Comex Gold's symbol is 'GC=F')
# e.g., SPY (https://finance.yahoo.com/quote/SPY/)

symbols_list = []
symbols_set = set()

def scrape_symbols_from_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Use a CSS selector to target <td> elements with <a> child elements containing 'data-symbol'
        symbols = [a['data-symbol'] for a in soup.select('td a[data-symbol]')]
        symbols_set.update(symbols)
        return symbols_set
    except Exception as e:
        print(f"Error scraping symbols from {url}: {e}")
        return []

# Define the base URL and parameters
base_url = 'https://finance.yahoo.com/lookup/equity'
total_pages = 14  # Total number of pages to scrape

# Loop through the pages
for page_number in range(total_pages):
    # Calculate the 'b' parameter for the current page
    b_param = page_number * 100

    # Construct the URL for the current page
    page_url = f'{base_url}?s=new&t=A&b={b_param}&c=100'
    

    # Scrape symbols from the current page and add to the list
    symbols_on_page = scrape_symbols_from_page(page_url)
    # print("Scraping from url:", page_url, "......")
    symbols_list.extend(symbols_on_page)
    # print("Symbols found:", symbols_on_page)

    time.sleep(1)

# Print the collected symbols
symbols_list=list(symbols_set)
# print(symbols_list)

valid_symbols = []

# # Loop through symbols and filter out invalid ones
# for symbol in symbols_list:
#     try:
#         data = yf.download(symbol, period='1mo')
#         if not data.empty:
#             valid_symbols.append(symbol)
#     except Exception as e:
#         print(f"Error downloading data for symbol {symbol}: {e}")

valid_symbols= symbols_list
start = dt.datetime(2018,1,1)
end = dt.datetime(2023,8,8)
data = yf.download(valid_symbols, start=start, end=end)

# Convert the DataFrame to a PyArrow Table
table = pa.Table.from_pandas(data)

# Specify the Parquet file path
parquet_file = 'stock_data_cache.parquet'

# Write the Table to a Parquet file
pq.write_table(table, parquet_file)

print("Dataset saved to Parquet file:", parquet_file)

# print(data)

