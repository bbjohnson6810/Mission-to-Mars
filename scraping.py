## functions to scrape Mars data for a custom web application
# run via app.py
# to run, in terminal: python app.py
# if port is occuppied, in terminal: lsof -i tcp:5000, then: kill -9 <programID>

# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# function to get all desired data
def scrape_all():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) # headless: F = watch in action, T = don't watch

    news_title, news_paragraph = mars_news(browser)
    
    # run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": get_hemispheres(browser)
    }
    
    # stop webdriver and return data
    browser.quit()
    return data


# function to get Mars news articles
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    # url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # search for elements with tag 'div' and attribute 'list_text'
    browser.is_element_present_by_css('div.list_text', wait_time=1) # Optional delay to load the page

    # set up html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try: # get articles, with error handling

        slide_elem = news_soup.select_one('div.list_text') # parent element

        # find the first 'a' tag 
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    # return the scraped article
    return news_title, news_p


# function to get Mars images
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1] # click the second button
    full_image_elem.click()

    # Parse the resulting html
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

        # find the relative image URL
        # use the link that's inside the <img /> tag with <fancybox-image /> class
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


# function to get Mars facts
def mars_facts():
    
    try:

        # use pandas to read the table
        # read_html returns a list of tables
        df = pd.read_html('https://galaxyfacts-mars.com')[0] 
    
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # pandas: convert df to html
    return df.to_html()


# function to get hemisphere photos
def get_hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    for i in range(4):
        
        hemispheres = {}
        browser.find_by_tag('h3')[i].click()
        hemi_url = browser.links.find_by_text('Sample').first 
        hemispheres['img_url'] = hemi_url['href'] 
        hemispheres['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemispheres)
        browser.back()

    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())