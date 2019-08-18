from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


def init_browser():
    executable_path ={'executable_path':'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless= False)
    exec_path = {'executable_path': 'app/.chromedrive/bin/chromedrive'}
    return Browser('chrome', headless=True, **exec_path)

mars_data = {}

def scrape_mars_news():
    try:
        browser = init_browser()

        ##Start Nasa News
        news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
        browser.visit(news_url)

        news_html = browser.html
        news_soup = BeautifulSoup(news_html, 'html.parser')
        
        titles = news_soup.find('div', class_='content_title').find('a').text
        paragraphs = news_soup.find('div',class_='article_teaser_body').text
        mars_data['news_title'] = titles
        mars_data['news_paragraph'] = paragraphs
        return mars_data
    finally:
        browser.quit()

def scrape_mars_img():
    try:
        browser = init_browser()
        ##Start Featured Image
        image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(image_url)
        image_html = browser.html
        image_soup = BeautifulSoup(image_html,"html.parser")
        image = image_soup.find(id= 'full_image')
        image_url_tail =image.get('data-fancybox-href')
        image_url_head = "https://www.jpl.nasa.gov/"
        featured_image_url = image_url_head + image_url_tail
        mars_data['featured_image_url'] = featured_image_url
        return mars_data
    finally:
        browser.quit()

def scrape_mars_weather():
    try:
        browser = init_browser()
        mars_weather_url = "https://twitter.com/marswxreport?lang=en"
        browser.visit(mars_weather_url)
        mars_weather_html = browser.html
        mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')
        all_tweets = []
        weather_timeline = mars_weather_soup.select('#timeline li.stream-item')
        for tweet in weather_timeline:
            tweet_text = tweet.select('p.tweet-text')[0].get_text()
            all_tweets.append(tweet_text)
        mars_weather = all_tweets[4]
        mars_data['mars_weather'] = mars_weather
        return mars_data
    finally:
        browser.quit()


def scrape_mars_facts():
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts_tables = pd.read_html(mars_facts_url)
    mars_facts_df = mars_facts_tables[0]
    mars_table_html = mars_facts_df.to_html()
    mars_data['mars_facts'] = mars_table_html
    return mars_data

def scrape_mars_hemispheres():
    try:
        browser = init_browser()
        ##Mar Hemispheres
        Hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(Hemispheres_url)
        hemisphere_html = browser.html
        hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')
        hemisphere_main_url = 'https://astrogeology.usgs.gov'
        items = hemisphere_soup.find_all('div', class_= 'item')
        hemisphere_img_urls = []
        for i in items:
            title = i.find('h3').text
    
            partial_img_url = i.find('a',class_='itemLink product-item')['href']
    
            browser.visit(hemisphere_main_url + partial_img_url)
    
            partial_img_html = browser.html
    
            partial_img_soup = BeautifulSoup(partial_img_html, 'html.parser')
            hemisphere_img_url = hemisphere_main_url + partial_img_soup.find('img',class_='wide-image')['src']
            hemisphere_img_urls.append({"Title": title, "Image_Url": hemisphere_img_url})
        mars_data['mars_hemisphere_data'] = hemisphere_img_urls
        
        return mars_data
    finally:
        browser.quit()
