import csv
import re

from selenium                   import webdriver
from selenium.common.exceptions import NoSuchElementException

brand_url_list = []

with open('./brand_infos.csv', mode='r') as brand_infos:
    reader = csv.reader(brand_infos)

    for list in reader:
        brand_url_list.append(list[2])

driver = webdriver.Chrome(('/Applications/chromedriver'))

image_description_list = []

pattern = re.compile(r'ht.+700x394')

for brand_url in brand_url_list:
    url = f'{brand_url}'
    driver.get(url)

    try:
        name = driver.find_element_by_xpath('/html/body/article/section[1]/div[2]/div/p[1]').text

        imageElement = driver.find_element_by_xpath('/html/body/article/section[1]/div[1]/div[1]')
        imageProperty = imageElement.value_of_css_property('background-image')
        imageUrl = re.search(pattern, imageProperty).group()

        description = driver.find_element_by_xpath('/html/body/article/section[1]/div[2]/div/p[2]').text

    except NoSuchElementException:
        description = ""

    except AttributeError :
        imageUrl = ""

    image_description_list.append(
        {
            "name" : name,
            "imageUrl" : imageUrl,
            "description" : description,
        }
    )

with open('./brand_main_infos.csv', mode='w') as brand_main_infos:
    brand_writer = csv.writer(brand_main_infos)

    for list in image_description_list:
        brand_writer.writerow([list["name"], list["imageUrl"], list["link"]])

driver.quit()

