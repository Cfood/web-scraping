#!/usr/bin/env python
# coding: utf-8

# In[1]:


#dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:

def scrape_mars():
    #splinter browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    #specify page url
    url="https://redplanetscience.com/"
    browser.visit(url)


    # In[4]:


    #save html to varable and parse
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[5]:
    mars_info_dict= {}

    #select newest headline and syummary from "soup"
    newest_headline = soup.find_all('div', class_='content_title')[0].text
    newest_summary = soup.find_all('div', class_='article_teaser_body')[0].text
    newest_headline, newest_summary

    mars_info_dict.update({'newest_headline':newest_headline,'newest_summary':newest_summary})
    # In[6]:


    #url for the featured image
    images_url="https://spaceimages-mars.com/"
    browser.visit(images_url)


    # In[7]:


    #save html to varable and parse
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # In[8]:


    #locate featured image path in website and append to url
    src = soup.find('img', class_='headerimage')['src'] 
    image_location = images_url+src
    image_location

    mars_info_dict.update({'mars_image_location': image_location})
    # In[9]:


    #url for the table
    facts_url="https://galaxyfacts-mars.com/"
    browser.visit(facts_url)


    # In[10]:


    #get tables from the table url
    tables = pd.read_html(facts_url)
    tables = pd.DataFrame(tables)
    tables= tables.to_html()

    mars_info_dict.update({'mars_facts':tables})
    # In[11]:


    hemis_url="https://marshemispheres.com/"
    browser.visit(hemis_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres_list = []
    hemispheres = soup.find_all('div', class_='item')

    for hemi in hemispheres:
        name = hemi.find('h3').text[:-9]
        hemi_link = hemi.find('a')['href']
        url = hemis_url + hemi_link
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        fs_img = soup.find('img',class_='wide-image')
        fs_img_link = fs_img['src']
        hemi_dict = {'hemishpere name': name ,'image_url':hemis_url + fs_img_link}
        hemispheres_list.append(hemi_dict)
    hemispheres_list

    mars_info_dict.update({'hemispheres': hemispheres_list})
    # In[12]:


    browser.quit()

    return mars_info_dict
