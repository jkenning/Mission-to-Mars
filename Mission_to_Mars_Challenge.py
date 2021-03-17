#!/usr/bin/env python
# coding: utf-8

# In[97]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


# In[2]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[10]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[12]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[13]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[14]:


# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[17]:


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[19]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[116]:


# 1. Use browser to visit the URL 
hem_url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
browser.visit(hem_url)

# Parse the resulting html with soup
hem_html = browser.html
hem_soup = soup(hem_html, 'html.parser')


# In[117]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
# Find HTML tags
items = hem_soup.find('div', class_='result-list')
hemispheres = items.find_all('div', class_='item')

# Use for loop to iterate through tags
for item in hemispheres:
    # Create empty dictionary
    hemisphere = {}
    
    # Find each hemisphere link
    item_link = item.find('a')['href']
    img_link = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{item_link}'
    
    # Navigate to the full-resolution image page
    browser.visit(img_link)
    time.sleep(1)
    
    # Retrieve full-resolution image URL string
    img_html = browser.html
    img_soup = soup(img_html, "html.parser")
    location = img_soup.find('div', class_='wide-image-wrapper')
    img_link = location.find('img', class_='wide-image').get('src')
    img_url = f'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/{img_link}'
    
    # Retrieve title for each image
    title = img_soup.find('h2', class_='title').text.replace(' Enhanced', '')
    
    # Append dictionary and list
    hemisphere['title'] = title
    hemisphere['img_url'] = img_url
    hemisphere_image_urls.append(hemisphere)


# In[118]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[119]:


# 5. Quit the browser
browser.quit()

