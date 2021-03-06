# Challenge
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt


#####################################
# Mars Article
#####################################

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Setup the HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        # isolate the first article
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # find the summary text and save it
        summary_text = slide_elem.find("div", class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, summary_text

#####################################
# Featured Image
#####################################

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None    

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url

#####################################
# Mars Facts
#####################################
def mars_facts():
    # Select the first table from the we page and convert it to a DataFrame
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        
    except BaseException:
      return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

#####################################
# Mars Hemispheres
#####################################
def hemisphere_images(browser):
    # Visit URL
    baseurl = 'https://astrogeology.usgs.gov'
    url = f'{baseurl}/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    # parse html and find the link locations
    html = browser.html
    hemi_soup = soup(html, 'html.parser')
    articles = hemi_soup.find_all('a', class_="itemLink product-item")
    
    # make empty lists to hemisphere url and img location
    hemisphere_urls=[]
    hemispheres = []

    # find the url of each hemisphere
    for article in articles:
        # create the first url and see if its been visited
        ext = article['href']
        url = f'{baseurl}{ext}'
        
        # if it has not been visited, get the absolute url of the image
        if url not in hemisphere_urls:

            # add to the list and visit the site
            hemisphere_urls.append(url)
            browser.visit(url)
            
            # parse the html
            html = browser.html
            img_soup = soup(html, 'html.parser')
            
            # find the sample button and save the linking url and title
            img = img_soup.find('a', text='Sample')
            img_url = img['href']
            title = browser.find_by_css("h2.title").text
            hemi_dict = {title:img_url}
            hemispheres.append(hemi_dict.copy())
    
    return hemispheres

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)


    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemisphere_images(browser)
      }
    
    #Close the browsing session and return the data
    browser.quit()
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



