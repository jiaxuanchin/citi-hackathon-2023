from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options  # Import ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Create ChromeOptions and add the command-line option
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36')

# Initialize the Selenium WebDriver with ChromeOptions
driver = webdriver.Chrome(options=chrome_options)  # Use options=chrome_options here

# Open the Yahoo Finance News page
url = 'https://finance.yahoo.com/news/'
driver.get(url)

# Scroll down to load more news articles (adjust the number of scrolls as needed)
scroll_js = "window.scrollBy(0, 200);"
num_scrolls = 20
for _ in range(num_scrolls):
    driver.execute_script(scroll_js)
    time.sleep(1)
    driver.find_element(By.ID, 'Main').send_keys(Keys.END)

# Get the page source after scrolling
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Find and extract the news articles (customize the selector as needed)
articles = soup.find_all('li', class_='js-stream-content')

# Process and print the article titles and links

titles = []
links = []
for article in articles:
    title = article.find('h3').get_text()
    titles.append(title)
    link = article.find('a').get('href')
    links.append(link)
    # print(f'Title: {title}')
    # print(f'Link: {link}')
    # print('-' * 30)

# print(len(titles))
# print(len(links))

refined_links = [link if "https://finance.yahoo.com" in link else "https://finance.yahoo.com" + link for link in links]

# print(refined_links[180])
# Close the browser
driver.quit()


