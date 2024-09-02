import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


# Initialize Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://olympics.com/en/olympic-games/tokyo-2020/medals")

# Wait for the page to load
time.sleep(5)

accept_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
accept_button.click()

driver.execute_script(f'window.scrollTo(0,500)')

sort = driver.find_element(By.XPATH, '//*[@id="globalTracking"]/section/section[3]/div[1]/div[2]/div[7]/div')
sort.click()

scroll_position = 0
categories = ["Country", "Gold", "Silver", "Bronze", "Total"]
all_data = [categories] 

for _ in range(93):  
    scroll_position += 400 
    driver.execute_script(f'window.scrollTo(0, {scroll_position})')

   
    country_row_number = 3 + _ * 8  
    xpath_name = f'//*[@id="globalTracking"]/section/section[3]/div[1]/div[3]/div[{country_row_number}]/span'
    country_name = driver.find_element(By.XPATH, xpath_name).text

    row_data = [country_name]  
    for i in range(4): 
        row_number = _ * 8 + i + 4 
        xpath = f'//*[@id="globalTracking"]/section/section[3]/div[1]/div[3]/div[{row_number}]/span/span'
        value = driver.find_element(By.XPATH, xpath).text
        value = "0" if value == "-" else value

        row_data.append(value)

    all_data.append(row_data)  


medals_df = pd.DataFrame(all_data).drop_duplicates()
medals_df.to_csv("Tokyo2020", index=False)

driver.quit()


