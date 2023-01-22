from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient

from params import LOGIN, PASSWORD, START_PAGE

s = Service('./firefoxdriver')
driver = webdriver.Firefox(service=s)
driver.get(START_PAGE)

wait = WebDriverWait(driver, 10)
login = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
login.send_keys(LOGIN)

btn = driver.find_element(By.XPATH, "//button[@type='submit']")
btn.click()

password = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
password.send_keys(PASSWORD)

btn = driver.find_element(By.XPATH, "//button[@type='submit']")
btn.click()

time.sleep(5) #!!! нужно заменить на wait

letters = driver.find_elements(By.XPATH, ".//div[@class='letter-list__react']/div/div/div/div/a")

urls = []

for letter in letters:
    urls.append(letter.get_attribute('href'))

letters_content = []

for url in urls:
    driver.get(url)
    time.sleep(10) #!!!

    from_field = driver.find_element(By.XPATH, "//span[@class='letter-contact']").get_attribute('title')
    date_field = driver.find_element(By.XPATH, ".//div[@class='letter__date']").text
    subject_field = driver.find_element(By.XPATH, "//h2[@class='thread-subject']").text
    text_field = driver.find_element(By.XPATH, "//div[@class='letter-body']").text

    item = {
        'from_field': from_field,
        'date_field': date_field,
        'subject_field': subject_field,
        'text_field': text_field
    }

    letters_content.append(item)


client = MongoClient('localhost:27017')
mongo_db = client['homework7']
collection = mongo_db['email']

for content in letters_content:
    collection.insert_one(content)
client.close()


print()
driver.close()