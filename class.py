#%%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

#%%
########################
# Get Articles
########################
# Create an instance of a splinter browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

#%%
# visit page
url = 'https://www.nhl.com/news/'
browser.visit(url)


#%%
html = browser.html
news_soup = soup(html, 'html.parser')
articles = news_soup.find_all('a', class_="article-item__headline")


# %%
print(articles)

# %%
for article in articles:
    print(article['class'])


# %%

