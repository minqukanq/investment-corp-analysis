from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display

import argparse
import time
import re


def arg_parse():
    parser = argparse.ArgumentParser(description="This is a parser for crawling application reviews")
    #Defining main arguments
    parser.add_argument("--url", type=str, required=True, help="URL of the page to crawl")
    parser.add_argument("--chrome", type=str, required=True, help="chromedriver path")
    parser.add_argument("--save_dir", type=str, default='output.csv', help="Crawled data filename, ex) 'output.csv'")
    return parser.parse_args()

def crawl_google_playstore(url, driverPath):
    # Open url with fullscreen
    options = Options()
    options.add_argument('--start-fullscreen')
    driver = webdriver.Chrome(driverPath, options=options)
    driver.get(url)
    
    # Scroll down the page
    scroll_pause_time = 1.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        for i in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_pause_time)

        if driver.find_elements_by_xpath("//span[@class='RveJvd snByac']"):
            driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
        
        else:
            break

    # Spread long reviews
    driver.execute_script("window.scrollTo(document.body.scrollHeight, 0)")
    spread_review = driver.find_elements_by_xpath("//button[@jsaction='click:TiglPc']")
    for i in range(len(spread_review)):
        isTrue = spread_review[i].is_displayed()
        print("Element is visible? " + str(isTrue))
    
        if isTrue:
            spread_review[i].click()
            print(str(i)+"th more button is clicked and wait 2 secs...")
            time.sleep(2)

    # Get each review via tag
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div_reviews = soup.find_all("div", {"class":"d15Mdf bAhLNe"})
    reviews_dict = []

    for div in div_reviews:
        try:
            star = div.find('div',{"class":"pf5lIe"}).find_next()['aria-label']    

            date_text = div.find('span',{"class":"p2TkOb"}).get_text()
            t = re.findall(r"\d*\.\d+|\d+",date_text) 
            date = '{0}-{1}-{2}'.format(t[0],t[1],t[2])

            like_text = div.find('div',{"class":"YCMBp GVFJbb"}).get_text()
            like = like_text[1:2]

            short_content = div.find('span',{'jsname':'bN97Pc'}).get_text()
            long_content = div.find('span',{'jsname':'fbQN7e'}).get_text()
            content = short_content if short_content!='' else long_content
            content.encode("utf-8")

        except Exception as e:
            print(f'{e}')
            continue

        else:
            reviews_dict.append({
                'DATE'   : date,
                'STAR'   : star,
                'LIKE'   : like,
                'REVIEW' : content
            })
    
    return  pd.DataFrame(reviews_dict)

def main():
    args        = arg_parse()
    url         = args.url
    driverPath  = args.chrome
    output      = args.save_dir

    res_df      = crawl_google_playstore(url, driverPath)
    res_df.to_csv(output)

if __name__ == "__main__":
    main()