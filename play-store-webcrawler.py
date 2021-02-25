from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import re

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


# ---------------------------------------
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    div_reviews = soup.find_all("div", {"class":"d15Mdf bAhLNe"})
    reviews = []

    for div in div_reviews:
        # grade = len(div.find_all('div',{'class' : 'nt2C1d'}))
        grade = div.find('div',{"class":"pf5lIe"}).find_next()['aria-label']
        print(grade)
        
        date_text = div.find('span',{"class":"p2TkOb"}).get_text()
        t = re.findall(r"\d*\.\d+|\d+",date_text) 
        date = '{0}-{1}-{2}'.format(t[0],t[1],t[2])
        print(date)
        good = div.find('div',{"class":"YCMBp GVFJbb"}).get_text()
        print(good)
        short_content = div.find('span',{'jsname':'bN97Pc'}).get_text()
        long_content = div.find('span',{'jsname':'fbQN7e'}).get_text()
        content = short_content if long_content=='' else long_content
        content.encode("utf-8")
        print(content)
        reviews.append((date,grade,good,content))


    
    print(len(reviews))
    
    return reviews
    # # Separate short and long reviews
    # reviews = driver.find_elements_by_xpath("//span[contains(@jsname, 'bN97Pc')]")
    # long_reviews = driver.find_elements_by_xpath("//span[@jsname='fbQN7e']")
        
    # # Merge all reviews
    # merged_review = [t.text if t.text!='' else long_reviews[i].text for i, t in enumerate(reviews)]

    # # Scrape dates, likes, and rating scores
    # dates = driver.find_elements_by_xpath("//span[@class='p2TkOb']")
    # likes = driver.find_elements_by_xpath("//div[@aria-label='이 리뷰가 유용하다는 평가를 받은 횟수입니다.']")
    # stars = driver.find_elements_by_xpath("//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")
    
    # # Make a dataframe
    # res_dict = []
    # for i in range(len(merged_review)):
    #     res_dict.append({
    #         'DATE' : dates[i].text, 
    #         'STAR' : stars[i].get_attribute('aria-label'), 
    #         'LIKE' : likes[i].text, 
    #         'REVIEW' : merged_review[i]
    #     })
    
    # res_df = pd.DataFrame(res_dict)
    
    # return res_df

url = "https://play.google.com/store/apps/details?id=com.linkzen.app&showAllReviews=true"
driverPath = "chromedriver.exe"
reviews = crawl_google_playstore(url, driverPath)
# display(res_df)

# res_df.to_csv('kiwoom.csv')