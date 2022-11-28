# -*- coding: utf-8 -*-
# Импортируем необходимые модули
from bs4 import BeautifulSoup as bs
import requests as req
import time
from tqdm import tqdm  # progress bar
import pandas as pd
import openpyxl
import json

# Заголовок программы
def main():
    print('''
       ########     ###    ########   ######  ######## ########      ######   #######  ##     ##  #######  ##    ##     ########       ## 
       ##     ##   ## ##   ##     ## ##    ## ##       ##     ##    ##    ## ##     ## ###   ### ##     ## ###   ##        ##          ## 
       ##     ##  ##   ##  ##     ## ##       ##       ##     ##    ##       ##     ## #### #### ##     ## ####  ##        ##          ## 
       ########  ##     ## ########   ######  ######   ########      ######  ##     ## ## ### ## ##     ## ## ## ##        ##          ## 
       ##        ######### ##   ##         ## ##       ##   ##            ## ##     ## ##     ## ##     ## ##  ####        ##    ##    ## 
       ##        ##     ## ##    ##  ##    ## ##       ##    ##     ##    ## ##     ## ##     ## ##     ## ##   ### ###    ##    ##    ## 
       ##        ##     ## ##     ##  ######  ######## ##     ##     ######   #######  ##     ##  #######  ##    ## ###    ##     ######  
         ''')

    # Добавляем адрес страницы и заголовки
    headers = {'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    # url = r'https://somon.tj/telefonyi-i-svyaz/hudzhand/'
    # url = r"https://somon.tj/transport/"
    # url = r'https://somon.tj/vakansii/'
    # url = r'https://somon.tj/nedvizhimost/'
    # url = r'https://somon.tj/kompyuteryi-i-orgtehnika/'
    # url = r'https://somon.tj/biznes-i-uslugi/'
    url = input('Введите аддрес сайта (пример: https://somon.tj/telefonyi-i-svyaz/\n\n')

    # Создаем обьект супа
    html = req.get(url=url, headers=headers)
    sel_rubric = 0
    if html.status_code == 200:
        soup = bs(html.text, 'lxml')
        rubrics = []

        # Парсим первую страниу и получаем список рубрик

        # 1 Получаем имя Города
        def get_city():
            ''' Запрос и Получение Города'''
            rubrics_city = []
            rubrics_cities_list = soup('ul', class_="rubric-cities-list")
            for rubric_city in rubrics_cities_list:
                for j, link in enumerate(rubric_city.findAll('li', class_="rubric-cities-list-item")):
                    refr_city = link.find('a')['href']
                    rubrics_city.append(refr_city.split('/')[2])
                    print(f'№:{j} - {refr_city.split("/")[2]}')
            sel_city = int(input('Выберите Город! №:\n'))
            print(rubrics_city[sel_city])
            return rubrics_city[sel_city]
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
