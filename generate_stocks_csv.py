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
import os

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

# Loop through symbols and filter out invalid ones
for symbol in symbols_list:
    try:
        data = yf.download(symbol, period='1d')
        if not data.empty:
            valid_symbols.append(symbol)
    except Exception as e:
        print(f"Error downloading data for symbol {symbol}: {e}")

# symbols_list = ['aaaaaa','NVDA','VWRA.L','IWDA.L','EIMI.L','KWEB','3067.HK','SPGP','IDRV','FCG','O87.SI','CIBR','ESPO','BOTZ','CLOU','BLOK','ARKF','ARKW','ESGE','ESGU','ESGD','PHO','FAN','LIT','ICLN','TAN','XLV','IHF','IHI','IBB','XHE','ARKG']
start = dt.datetime(2018,1,1)
end = dt.datetime(2023,8,8)
data = yf.download(valid_symbols, start=start, end=end)

# Check if a cached CSV file exists
cache_file = 'stock_data_cache.csv'
if os.path.isfile(cache_file):
    # If the cached file exists, load data from it
    data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
else:
    # If the cached file doesn't exist, download the data and save it to a CSV file
    data = yf.download(symbols_list, start=start, end=end)
    data.to_csv(cache_file)  # Save data to a CSV file for future use

# print(data)

