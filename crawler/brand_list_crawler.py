import time
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.styleshare.kr/brands'

driver = webdriver.Chrome(('/Applications/chromedriver'))
driver.get(url)

brand_list = []

for page in range(1,4):
    driver.implicitly_wait(5)

    if page == 1:
        pass
    
    else :
        elements = driver.find_element_by_xpath(f'//*[@id="app"]/div/div[2]/div[1]/div/button[{page}]')
        driver.execute_script("arguments[0].click();", elements)

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break

        last_height = new_height

    brandImg  = driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div/a/img')
    brandName = driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div/div/div/a')
    brandLink = driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div[1]/div/a')

    for item in zip(brandName,brandImg,brandLink):
        brand_list.append(
            {
                "name" : item[0].text,
                "img"  : item[1].get_attribute("src"),
                "link" : item[2].get_attribute("href"),
            }
        )

with open('./brand_infos.csv', mode='w') as brand_infos:
    brand_writer = csv.writer(brand_infos)

    for list in brand_list:
        brand_writer.writerow([list["name"], list["img"], list["link"]])

driver.quit()
