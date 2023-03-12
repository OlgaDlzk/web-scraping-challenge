# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import pandas as pd

def scrape():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site: https://static.bc-edx.com/data/web/mars_news/index.html
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    new_soup = soup(html, 'html.parser')

    results = new_soup.select_one('div', class_='list_text')

    title = results.find('div', class_='content_title').text.strip()

    text = results.find('div', class_='article_teaser_body').text

    browser.quit()

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    image_soup = soup(html, 'html.parser')

    relative_image_path = image_soup.find('img', class_='headerimage fade-in')["src"]
    featured_img_url = url + relative_image_path

    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)

    df = tables[1]

    df.columns = ['Parameter','Value']
    df['Parameter'] = df['Parameter'].str.replace(':','')

    df_html = df.to_html()

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the https://marshemispheres.com/
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Retrieve all elements that contain book information
    items = browser.find_by_css('a.product-item img')
    #print(items)

    hemisphere_image_url = []

    for item in range(len(items)):

            
    #     # Store link that leads to full image website
        browser.find_by_css('a.product-item img')[item].click()
        header = browser.find_by_css('h2.title').text
        sample = browser.links.find_by_text('Sample').first
        full_url = sample['href']

            
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_url.append({"title" : header, "img_url" : full_url})
        browser.back()

    browser.quit()

    scraped_data = {
        'news_title': title,
        'news_paragraph': text,
        'featured_image': featured_img_url,
        'facts': df_html,
        'hemispheres': hemisphere_image_url
    }

    return scraped_data

if __name__== '__main__':
    print(scrape())