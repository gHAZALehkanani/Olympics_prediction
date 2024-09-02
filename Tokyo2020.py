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
all_data = [categories]  # Başlıkları ekleyerek başlıyoruz

for _ in range(93):  # Daha fazla döngü gerekiyorsa sayısını artırabilirsiniz
    scroll_position += 400  # Sayfayı aşağı kaydır
    driver.execute_script(f'window.scrollTo(0, {scroll_position})')

    # Ülke adını almak için dinamik XPATH
    country_row_number = 3 + _ * 8  # İlk ülkenin XPATH'i 3, sonra 11, 19, ...
    xpath_name = f'//*[@id="globalTracking"]/section/section[3]/div[1]/div[3]/div[{country_row_number}]/span'
    country_name = driver.find_element(By.XPATH, xpath_name).text

    row_data = [country_name]  # Her satır için verileri saklayacak liste, ülke adı ile başlıyor
    for i in range(4):  # 0'dan 3'e kadar döngü (Gold, Silver, Bronze, Total)
        row_number = _ * 8 + i + 4  # Satır numarasını hesapla (ilk satır numarası 4 olacak şekilde)
        xpath = f'//*[@id="globalTracking"]/section/section[3]/div[1]/div[3]/div[{row_number}]/span/span'
        value = driver.find_element(By.XPATH, xpath).text
        value = "0" if value == "-" else value

        row_data.append(value)

    all_data.append(row_data)  # Satırdaki tüm verileri all_data'ya ekle

# Create a DataFrame and save the results to a CSV file
medals_df = pd.DataFrame(all_data).drop_duplicates()
medals_df.to_csv("Tokyo2020", index=False)

driver.quit()


