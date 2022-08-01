# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# search for elements with tag 'div' and attribute 'list_text'
browser.is_element_present_by_css('div.list_text', wait_time=1) # Optional delay to load the page


# set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text') # parent element


# find the first 'a' tag 
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button

full_image_elem = browser.find_by_tag('button')[1] # click the second button
full_image_elem.click()


# Parse the resulting html
html = browser.html
img_soup = soup(html, 'html.parser')


# find the relative image URL

# use the link that's inside the <img /> tag with <fancybox-image /> class
image_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
image_url_rel


# create an absolute URL

img_url = f'https://spaceimages-mars.com/{image_url_rel}'
img_url


# ## Mars facts

# use pandas to read the table
# read_html returns a list of tables

df = pd.read_html('https://galaxyfacts-mars.com')[0] 
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

for i in range(4):
    
    hemispheres = {}
    browser.find_by_tag('h3')[i].click()
    hemi_url = browser.links.find_by_text('Sample').first 
    hemispheres['img_url'] = hemi_url['href'] 
    hemispheres['title'] = browser.find_by_css('h2.title').text
    
    hemisphere_image_urls.append(hemispheres)
    
    browser.back()


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()