#!/usr/bin/env python
# coding: utf-8


# # Dependencies
from splinter import Browser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    
    executable_path = {"executable_path": "/app/.chromedriver/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

 


def scrape():
    browser = init_browser()

    all_data = {}

    now = datetime.datetime.now()
    now=now.strftime("%a %Y-%m-%d %I:%M:%S %p")
    all_data['current']=now

    url = 'https://mars.nasa.gov/news'

    browser = webdriver.Chrome()
    browser.get(url)

    html_source = browser.page_source
    # browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')
    mars_content = soup.find_all('li', class_="slide")


    x = 1
    for result in mars_content:
        try:
            title = result.find('div', class_="content_title").text
            body = result.find('div', class_="article_teaser_body").text

            if (title and body):
                # print(f'ARTICLE {x} ------------')
                # print(title)
                # print(body)
                all_data['title'] = title
                all_data['body'] = body
                x += 1

        except AttributeError as e:
            print(e)
            x += 1
    print('Section 1 Complete')
    # browser.quit()  


    ####SECTION TWO: SPLINTER#####
    browser = init_browser()

    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    url_img=browser.find_by_id('full_image')
    featured_image_url= 'https://www.jpl.nasa.gov' + url_img['data-fancybox-href']

  


    # browser = init_browser()

    # url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # browser.visit(url_2)
    # html = browser.html
    # soup = BeautifulSoup(html, 'html.parser')

    # browser.find_by_id('full_image').first.click()
    # lightbox = soup.find_all('a', class_='button')

    # for item in lightbox:
    #     url_item = item.get('data-link')
    #     if url_item != None:
    #         url_3 = 'https://www.jpl.nasa.gov' + url_item
    #         browser.visit(url_3)
    #         # time.sleep(0.5)
    #         # browser.click_link_by_partial_href('.gov/jpeg/')
    #         url_img=browser.find_link_by_partial_href('.gov/jpeg/')
    #         featured_image_url = browser.url
    #         browser.quit()
    #     else:
    #         continue


    ##### DOESN't WORK#####
    # item=lightbox[0]
    # url_item=item.get('data-link')
    # url_3 = 'https://www.jpl.nasa.gov' + url_item
    # browser.visit(url_3)
    # url_img=browser.find_link_by_partial_href('.gov/jpeg/')
    # browser.visit(url_img)
    # featured_image_url = browser.url
        ##### DOESN't WORK#####




    all_data['featured_image_url']=featured_image_url
    print('Section 2 Complete')


    ##SECTION 3 Mars Weather###


    url = 'https://twitter.com/marswxreport?lang=en'
    tweets = []

    browser = webdriver.Chrome()
    browser.get(url)

    html_source = browser.page_source
    # browser.quit()

    soup = BeautifulSoup(html_source, 'html.parser')
    mars_tweet = ''
    mars_tweets = soup.find_all('div', class_="js-tweet-text-container")

    mars_weather_tweets = []

    for item in mars_tweets:
        if 'InSight sol' in item.text:
                mars_weather_tweets.append(item)
                if len(mars_weather_tweets) == 1:
                        break

    latest_tweet = mars_weather_tweets[0].text
    mars_weather = latest_tweet.replace('\n', ' ')
    if 'pic.twitter' in mars_weather:
        mars_weather_text = mars_weather.partition("pic.twitter")[0]
        mars_weather_popup_link = "pic.twitter" + mars_weather.partition("pic.twitter")[2]
      
        soup = BeautifulSoup(html_source, 'html.parser')
        mars_tweet_popup_link = soup.find('img', attrs={'src': re.compile("^https://pbs.twimg.com/media/+")})
        mars_tweet_popup_link=mars_tweet_popup_link["src"]
        # mars_weather_link=(mars_tweet_popup["data-image-url"].text)
        
        all_data['mars_tweet_popup_link']=mars_tweet_popup_link
        # all_data['mars_tweet_popup']=mars_tweet_popup
        all_data['mars_weather_text']=mars_weather_text
        # all_data['mars_weather_link']=mars_weather_link
    else: 
        mars_weather=mars_weather
    browser.quit()
    
    all_data['mars_weather']=mars_weather
    
    print('Section 3 Complete')

    ##SECTION 4 FACTS###
    browser = init_browser()

    url_4 = 'https://space-facts.com/mars/'

    table = pd.read_html(url_4)
    table

    table_titles=[]
    table_values=[]
    
    df = table[0]
    df.columns = ["title", "value"]
    df.set_index("title", inplace=True)

    for x in range(len(df)):
        table_titles.append(df.iloc[x].name[0:-1])
        table_values.append(df.iloc[x].value)
    all_data['table_titles']=table_titles
    all_data['table_values']=table_values


    html_table = df.to_html()
    html_table

    
    all_data['html_table']=html_table
    print('Section 4 Complete')

    ###SECTION 5 MARS HEMISPHERES ####
    browser = init_browser()

    url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(url_5)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemi_collection = []
    hemi_list = soup.find_all('a', class_='itemLink product-item')
    for item in hemi_list:
        if item.text != '':
                hemi_collection.append(item)
    # browser.quit()

    # browser = init_browser()
    hemis_dicts_all = []

    for item in hemi_collection:
        # browser = init_browser()
        link = 'https://astrogeology.usgs.gov' + item.get('href')
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemi_title = soup.find('h2', class_='title').text
        hemi_body = soup.find('p').text
        img_links = soup.find('a', attrs={'href': re.compile("^http://")})
        img_link = img_links['href']
        hemi_dict = {}
        hemi_dict = {"title": hemi_title, "img_url": img_link, "body": hemi_body}
        hemis_dicts_all.append(hemi_dict)
        x += 1
        # browser.quit()

    all_data['hemis_dicts_all']= hemis_dicts_all
    print('Section 5 Complete')

    #Create references for table icons

    table_icons=["icons/orbit.png","icons/earth.png","icons/mass.png", "icons/moon.png", "icons/solar-system.png", "icons/jupiter-with-satellite.png","icons/celsius.png","icons/clipboard.png", "icons/telescope.png"]

    all_data['table_icons']= table_icons
    print('All sections complete')



    return all_data
