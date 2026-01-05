searchname = input('Введите ключевое слово: ')
#импорты
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import sqlite3
#настройки драйвера
opts=wd.ChromeOptions();[opts.add_argument(a)for a in["--headless","--start-maximized","--no-sandbox","--disable-gpu","--disable-dev-shm-usage","--user-agent=Mozilla/5.0"]]
browser = wd.Chrome(options=opts)
browser.get("https://www.liveinternet.ru/rating/ru/")

try:
    #поиск кнопки
    wait = WebDriverWait(browser, 1)
    open_search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search_ico")))
    open_search.click()
    #поиск поля
    search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".search-block .select input")))
    search.clear()
    #ввод текста
    search.send_keys(searchname)
    open_click = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#msg_search")))
    open_click.click()
except Exception as e:
    print(f"Ошибка: {e}")
#перенос в базу данных
soup = BeautifulSoup(browser.page_source, 'html')
all_publications = \
    soup.find_all('div', {'class': 'text'})[1:5]
for article in all_publications:
    print(article)
    name = article.get_text()
    link = str(article)
    link = link.split('\"')
    connection = sqlite3.connect(r'test.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO data(name, link) VALUES (?, ?)", (str(name), str(link[3])))
    connection.commit()

browser.quit()