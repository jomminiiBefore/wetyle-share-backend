import time
import csv

from selenium import webdriver

url = 'https://www.styleshare.kr/categories/350'
driver = webdriver.Chrome(('/Applications/chromedriver'))
driver.get(url)
driver.implicitly_wait(3)

product_list = []
second_category_list = driver.find_elements_by_xpath('//*[@id="app"]/div/div[2]/ul/li/span')

for second_category_index in range(len(second_category_list)+1)[1:]:
    second_category_element = driver.find_element_by_xpath(f'//*[@id="app"]/div/div[2]/ul/li[{second_category_index}]/span')
    driver.execute_script('arguments[0].click();', second_category_element)
    time.sleep(2)

    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    count = 0
    while count < 3:
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

        count += 1
        print(second_category_index," : ", count)
    try:
        products = driver.find_elements_by_xpath('//*[@id="app"]/div/div[5]/div/div/a')
    except Exception as e:
        print(e)
    finally:
        for product in products:
            product_list.append(
                {
                    "second_category_index":second_category_index,
                    "link":product.get_attribute("href"),
                 }
                )

with open('./product_lists.csv', mode='w') as product_lists:
    product_writer = csv.writer(product_lists)
    for product in product_list:
        product_writer.writerow([product["second_category_index"], product["link"]])

driver.quit()
