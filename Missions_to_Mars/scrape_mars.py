# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape():
    ### NASA Mars News

    # Set the chrome driver
    executable_path = {"executable_path": "d:/chrome_driver/chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    #  Open the NASA's Mars news page on Chrome
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    # Read html from the page
    html = browser.html
    soup = bs(html, "html.parser")

    # Scrape the very first news title and paragraph text
    news_title = soup.find_all("div", class_="content_title")[1].text
    news_p = soup.find("div", class_="article_teaser_body").text


    ### JPL Mars Space Images - Featured Image

    # Open the JPL page on Chrome
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Move to the page having the full size image
    browser.links.find_by_partial_text("FULL IMAGE").first.click()
    browser.links.find_by_partial_text("more info").first.click()
    browser.find_by_text("Full-Res JPG: ").first.find_by_tag("a").first.click()

    # Scrape the image url
    featured_image_url = browser.find_by_tag("img").first["src"]


    ### Mars Facts

    # Scrape the first table from https://space-facts.com/mars/
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)[0]
    table.columns = ["Description", "Value"]

    # Convert the table to html
    table_html = table.to_html(index=False, justify="left").replace("\n", "")

    ### Mars Hemispheres

    # Open the Mars Hemispheres page on Chrome
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get the number of images
    num_of_img = len(browser.find_by_css("img[class='thumb']"))

    # Scrape each image title and url
    for i in range(num_of_img):
        browser.find_by_css("img[class='thumb']")[i].click()
        hemisphere_image_urls.append({"title":browser.find_by_css("h2[class='title']").first.text.replace(" Enhanced", ""),
                                      "img_url":browser.find_by_text("Sample").first["href"]})
        browser.back()

    # Store all information to a dictionary
    my_dict = {
        "news_title":news_title,
        "news_paragraph":news_p,
        "featured_image_url":featured_image_url,
        "table": table_html,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    browser.quit()

    return my_dict