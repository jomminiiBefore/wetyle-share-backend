import time
import csv

from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome(('/Applications/chromedriver'))

with open('./product_lists_08.csv', mode='r') as product_lists:
    reader = csv.reader(product_lists)

    product_info = []

    for product in reader:
        url = f'{product[1]}'
        driver.get(url)
        time.sleep(5)

        try:
            productName = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/p')
            productImg  = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[1]/div/picture/img')
            brand_id    = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/div/a')
            # 할인가가 있을 때
            try:
                productPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/s')
                productDiscountPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/p')

            #할인가가 없을 때
            except Exception:
                productPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/p')
                productDiscountPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/p')

            productDetailInfo = driver.find_elements_by_css_selector('#app > div > div > div > div > div > div > div > div > picture > img')
            detailImageList = []
            for image in productDetailInfo:
                detailImageList.append(image.get_attribute("data-src"))

            allPage        = driver.page_source
            soup           = BeautifulSoup(allPage,'html.parser')
            productAddInfo = soup.select('#app > div > div.Box-fzpncP.iIZfvh > div:nth-child(3) > div > div')

            try:
                category   = driver.find_element_by_css_selector('#app > div > div.Box-fzpncP.ewLxnc > div.Box-fzpncP.erzKmA.goods__category-best')
            except Exception:
                category   = driver.find_element_by_css_selector('#app > div > div.Box-fzpncP.erzKmA.goods__category-best')

        except Exception as e:
            print("error",e, url)
        finally:
            try:
                print(productPrice.text, productDiscountPrice.text)
                product_info.append(
                    {
                        "name"           : productName.text,
                        "image"          : productImg.get_attribute("src"),
                        "price"          : round(int(productPrice.text.split('원')[0].replace(",", "")),-2),
                        "discount_price" : round(int(productDiscountPrice.text.split()[1].split('원')[0].replace(",", "")),-2),
                        "detail_info"    : detailImageList,
                        "add_info"       : productAddInfo,
                        "category_id"    : category.get_attribute("data-category_id"),
                        "brand_id"       : brand_id.get_attribute("href"),
                    }
                )
                print(product_info)
            except Exception as e:
                print(e)

with open('./product_details_08.csv', mode='w') as product_details:
    product_writer = csv.writer(product_details)

    for product in product_info:
        product_writer.writerow([product["name"],product["image"],product["price"],product["discount_price"],product["detail_info"],product["add_info"],product["category_id"], product["brand_id"]])

driver.quit()
