import requests
from bs4 import BeautifulSoup
import sqlite3
connection = sqlite3.connect('test.db')
cursor = connection.cursor()
headers = {'Accept': 'text/html', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5844.0 Safari/537.36'}
#ключевые переменные
global site
site = input('Введите ссылку на сайт')
global IDs
IDs = 1
while 1:
    try:
        req = requests.get(url=site + f'/index/8-{IDs}', headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        name = soup.find_all('div', id='block1')
	#парсинг ника
        for data in name:
            name = str(data.get_text())
            name = name.split(' ')[1]
	#парсинг группы
        grp = soup.find_all('div', id='block2')
        for data in grp:
            grp = str(data.get_text())
            grp = grp.split(':')[1]
            grp = grp.replace('\n', '')
            grp = grp.replace(' ', '')
            print(grp)
	#парсинг ника
        username = soup.find_all('div', id='block5')
        for data in username:
            username = str(data.get_text())
            username = username.split('[')[0]
            username = username.replace('Имя:', '')
            username = username.replace(' ', '')
	#парсинг секса
        sex = soup.find_all('div', id='block5')
        for data in sex:
            sex = str(data.get_text())
            sex = sex.split('[')[1]
            sex = sex.split(']')[0]
            sex = sex.replace(' ', '')
	#проверка на отсутствие пустоты
        if len(grp) < 1:
            break
	#запись в БД
        cursor.execute('INSERT INTO data(site,id,name,grp,nick,sex) VALUES (?, ?, ?, ?, ?, ?)', (str(site),(IDs), str(name), str(grp), str(username), str(sex)))
        connection.commit()
	#идём к следующему ID
        IDs += 1
    except:
        break
