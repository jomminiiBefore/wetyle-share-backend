import time
import csv

from selenium import webdriver
from bs4 import BeautifulSoup

url = 'https://www.styleshare.kr/goods/295509'
driver = webdriver.Chrome(('/Applications/chromedriver'))
driver.get(url)
time.sleep(5)

product_info = []

try:
    productName = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/p')
    productImg  = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[1]/div/picture/img')

    # 할인가가 있을 때
    try:
        productPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/s/text()[1]')
        productDiscountPrice = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[1]/div/p/text()')

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
    print("error message : ", e.message)

finally:
    product_info.append(
        {
            "name"           : productName.text,
            "image"          : productImg.get_attribute("src"),
            "price"          : int(productPrice.text.split()[1].split('원')[0].replace(",", "")),
            "discount_price" : int(productDiscountPrice.text.split()[1].split('원')[0].replace(",", "")),
            "detail_info"    : detailImageList,
            "add_info"       : productAddInfo,
            "category_id"    : category.get_attribute("data-category_id"),
        }
    )

print(product_info)

driver.quit()
