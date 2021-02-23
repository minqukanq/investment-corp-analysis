from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

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
            time.sleep(SCROLL_PAUSE_TIME)

        driver.find_element_by_xpath("//span[@class='RveJvd snByac']").click()
        
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
    # Spread long reviews
    spread_review = driver.find_elements_by_xpath("//button[@jsaction='click:TiglPc']")
    for i in range(len(spread_review)):
        isTrue = spread_review[i].is_displayed()
        print("Element is visible? " + str(isTrue))
    
        if isTrue:
            spread_review[i].click()
            print(str(i)+"th more button is clicked and wait 2 secs...")
            time.sleep(2)
            
    # Separate short and long reviews
    reviews = driver.find_elements_by_xpath("//span[contains(@jsname, 'bN97Pc')]")
    for i in range(len(reviews)):
        print(str(i) + "\t" + reviews[i].text)
    
    long_reviews = driver.find_elements_by_xpath("//span[@jsname='fbQN7e']")
    for i in range(len(reviews)):
        print(str(i) + "\t" + long_reviews[i].text)
        
    # Merge all reviews
    merged_review = [t.text if t.text!='' else long_reviews[i].text for i, t in enumerate(reviews)]

    # Crawl dates, likes, and rating scores
    dates = driver.find_elements_by_xpath("//span[@class='p2TkOb']")
    likes = driver.find_elements_by_xpath("//div[@aria-label='이 리뷰가 유용하다는 평가를 받은 횟수입니다.']")
    stars = driver.find_elements_by_xpath("//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")
    
    # Make dataframe
    res_dict = []
    for i in range(len(merged_review)):
        res_dict.append({
            'DATE' : dates[i].text, 
            'STAR' : stars[i].get_attribute('aria-label'), 
            'LIKE' : likes[i].text, 
            'REVIEW' : merged_review[i]
        })
    
    res_df = pd.DataFrame(res_dict)
    res_df