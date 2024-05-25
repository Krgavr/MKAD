import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import re
import time

# Instalace ovladače Chrome
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Složka pro ukládání souborů
save_folder = "downloaded_json_files"
os.makedirs(save_folder, exist_ok=True)

# Funkce pro stažení souboru JSON
def download_json_file(file_url, title):
    # Odstranění neplatných znaků z názvu souboru
    file_name = re.sub(r'[<>:"/\\|?*]', '_', title) + ".json"
    file_path = os.path.join(save_folder, file_name)
    try:
        file_response = requests.get(file_url, verify=False)
        with open(file_path, 'wb') as file:
            file.write(file_response.content)
        print(f"File {file_path} successfully downloaded.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading a file {file_name}: {e}")

# Otevření hlavní stránky
url = "https://data.gov.cz/datov%C3%A9-sady?velikost-str%C3%A1nky=600&kl%C3%AD%C4%8Dov%C3%A1-slova=%C3%BA%C5%99edn%C3%AD%20deska"
driver.get(url)

# Čekání na úplné načtení stránky
time.sleep(5)

# Získat všechny odkazy na datové sady
dataset_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/datová-sada?iri=']")

# Průchod jednotlivými odkazy
for link in dataset_links:
    link_url = link.get_attribute('href')
    if link_url:
        driver.get(link_url)
        time.sleep(1)  # Čekání na úplné načtení stránky
        
        # Získat název stránky
        title_element = driver.find_element(By.TAG_NAME, "h1")
        title = title_element.text
        
        # Vyhledávání a stahování souborů JSON
        download_links = driver.find_elements(By.LINK_TEXT, "Stáhnout")
        for download_link in download_links:
            file_url = download_link.get_attribute('href')
            if file_url:
                download_json_file(file_url, title)
        
        driver.back()
        time.sleep(1)  # Čekání na úplné načtení předchozí stránky

# Zavření prohlížeče
driver.quit()
