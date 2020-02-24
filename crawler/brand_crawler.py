import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = 'https://www.styleshare.kr/brands'

# 크롬창을 띄우지 않는 옵션
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('disable-gpu')
# options=options

driver = webdriver.Chrome('/Applications/chromedriver')
# 암시적으로 최대 5초 기다림
# driver.implicitly_wait(5)

#url
#driver.get(url)

brand_list = []




for page in range(1,5):
    driver.get(url)
   # driver.implicitly_wait(5)
    element = driver.find_element_by_xpath(f'//*[@id="app"]/div/div[2]/div[1]/div/button[{page}]')
    driver.execute_script("arguments[0].click();", element)

    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    brandImg = driver.find_elements_by_css_selector('#app > div > div.filtered-brands > div.brands > div.brands-inner-wrapper > div > a > img')

    brandName = driver.find_elements_by_css_selector('#app > div > div.filtered-brands > div.brands > div.brands-inner-wrapper > div > div > div > a')
    
    for item in zip(brandName,brandImg):
        print(item)
        brand_list.append(
            {
                "name" : item[0].text,
                "img"  : item[1].get_attribute("src"),
            }
        )

print(brand_list)
#for i in range(len(brandNameList)):
#    print("brandName:",  brandNameList[i].text)
#for i in range(len(brandNameImg)):
#    print("brandImg:", brandNameImg[i].get_attribute("src"))
# 열어둔 webdriver 종료
driver.quit()
