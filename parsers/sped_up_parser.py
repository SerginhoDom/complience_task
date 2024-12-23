import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Функция для загрузки ИНН из CSV
def load_inns_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['ИНН'].tolist()

# Настройка браузера для использования с Selenium
def setup_browser(download_folder):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Указываем путь для скачивания PDF файлов
    prefs = {
        "download.default_directory": download_folder,  # Папка для загрузки
        "download.prompt_for_download": False,  # Отключаем запросы на подтверждение загрузки
        "plugins.always_open_pdf_externally": True,  # Открытие PDF без запроса
        "safebrowsing.enabled": True  # Включаем безопасный просмотр
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Парсер для поиска и скачивания PDF
def download_pdf_for_inn(driver, inn, download_folder):
    driver.get("https://egrul.nalog.ru/index.html")
    
    time.sleep(1)
    
    # Находим поле ввода ИНН и вводим значение
    query_input = driver.find_element(By.ID, "query")
    query_input.clear()
    query_input.send_keys(inn)
    query_input.send_keys(Keys.RETURN)  # Нажимаем Enter, чтобы начать поиск

    time.sleep(1) 
    
    # Нажимаем на кнопку "Найти"
    search_button = driver.find_element(By.ID, "btnSearch")
    search_button.click()
    
    time.sleep(1)
    
    # Ожидаем появления кнопки "Получить выписку"
    try:
        excerpt_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-excerpt"))
        )
        excerpt_button.click()
    except Exception as e:
        print(f"Theres no download button for {inn}: {e}")
        return

    time.sleep(1)
    
    downloaded_files = os.listdir(download_folder)
    for file in downloaded_files:
        if file.endswith(".pdf"):
            return
    
def main():
    inns = load_inns_from_csv("data/dataset.csv")
    download_folder = r"D:\Study\MachineLearning\xmas_hack\output_pdfs"
    
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    driver = setup_browser(download_folder)
    
    for inn in inns:
        try:
            download_pdf_for_inn(driver, inn, download_folder)
        except Exception as e:
            print(f"Error {inn}: {e}")
    
    driver.quit()

if __name__ == "__main__":
    main()