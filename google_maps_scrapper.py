import pandas as pd
import time
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import wait, expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from arabic_reshaper import reshape
from bidi.algorithm import get_display
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
    }

options = ChromeOptions()
options.add_argument('--headless')
for x,y in headers.items():
    options.add_argument(f'--{x}={y}')
    
def check_exists(h,cn):
    try:
        h.find_element(By.CLASS_NAME,cn)
    except NoSuchElementException:
        return False
    return True

driver = Chrome(options=options)
driver.get('https://www.google.com/maps/')
driver.set_window_size(1024, 600)
driver.maximize_window()
x = driver.find_element(By.TAG_NAME,'input')
x.send_keys('hospitals in alexandria')
x.send_keys(Keys.RETURN)
time.sleep(10)
driver.save_screenshot(r"C:\Users\omars\OneDrive\Desktop\screen.png")

ff = driver.find_element(By.XPATH,'//div[@jstcache = "3"]')
after = 1
before = 0
while after > before:
    before = len(ff.find_elements(By.XPATH,'//a[@class = "hfpxzc"]'))
    ActionChains(driver).send_keys_to_element(ff,Keys.END).perform()
    time.sleep(8)
    driver.save_screenshot(r'C:\Users\omars\OneDrive\Desktop\screenss.png')
    after = len(ff.find_elements(By.XPATH,'//a[@class = "hfpxzc"]'))

details = ff.find_elements(By.XPATH,'//div[@class = "lI9IFe "]')

hos_link =ff.find_elements(By.XPATH,'//a[@class = "hfpxzc"]')


hospital_name = [i.find_element(By.CLASS_NAME,'NrDZNb').text for i in details]
links = [i.get_attribute('href') for i in hos_link]
number = [i.find_element(By.CLASS_NAME,'UsdlK').text if check_exists(i,'UsdlK') else 'no number' for i in details ]
hospital_names_correct = [get_display(reshape(i)) for i in hospital_name] 

data = pd.DataFrame({'Hospital_Name':hospital_names_correct,'Link':links,'Telephone':number})
data.index = data.index + 1
print(data)
data.to_csv(r'C:\Users\omars\OneDrive\Desktop\hospitals.xlsx')