from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

s = Service('./firefoxdriver')
driver = webdriver.Firefox(service=s)
driver.get('https://www.mvideo.ru')

#
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='blocks']")))

actions = ActionChains(driver)

for i in range(2):
    time.sleep(2) #!!!
    actions.scroll_by_amount(delta_x=0, delta_y=3000)
    actions.perform()

btn_trend = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='tab-button ng-star-inserted']")))
btn_trend.click()

num_goods_in_trend = \
    int(driver.find_element(By.XPATH, "//button[@class='tab-button ng-star-inserted']/div/span[@class='count']").text)

xpath_goods_in_trend = '//mvid-carousel[@class="carusel ng-star-inserted"]/div/div/mvid-product-cards-group/div'
input_data = driver.find_elements(By.XPATH, xpath_goods_in_trend)

step = int(len(input_data)/num_goods_in_trend)

client = MongoClient('localhost:27017')
mongo_db = client['homework7']
collection = mongo_db['mvideo']

for i in range(0, len(input_data), step):
    name = input_data[i+3].text
    rating = input_data[i+4].text
    price = input_data[i+5].text
    url = input_data[i+1].find_element(By.XPATH, './/div/a').get_attribute('href')

    item = {
        'name': name,
        'rating': rating,
        'price': price,
        'url': url
    }

    collection.insert_one(item)

client.close()

print()
driver.close()
