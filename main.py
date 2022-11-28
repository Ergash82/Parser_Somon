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
    # Заголовок программы
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

        # 2 Получаем имя Города
        def get_city():
            ''' Запрос и Получение Города'''
            rubrics_city = []
            rubrics_cities_list = soup.find_all('ul', class_="rubric-cities-list")
            for rubric_city in rubrics_cities_list:
                for j, link in enumerate(rubric_city.findAll('li', class_="rubric-cities-list-item")):
                    refr_city = link.find('a')['href']
                    rubrics_city.append(refr_city.split('/')[2])
                    print(f'№:{j} - {refr_city.split("/")[2]}')
            select_city = int(input('Выберите Город! №:\n'))
            print(rubrics_city[select_city])
            return rubrics_city[select_city]

        # 1 Получаем Рубрику
        def get_rubrics():
            # global soup
            rubrics.clear()
            select_city = get_city()
            for rubric in soup.findAll(class_="rubrics-list"):
                for i, link in enumerate(rubric.findAll('li')):
                    refer = link.find('a')['href']
                    rubrics.append([refer.split('/')[2], "https://somon.tj" + refer + select_city])
                    print(f'№:{i} - {refer.split("/")[2]}')

            # Выбираем рубрику
            select_rubric = int(input('Выберите рубрику №: ! \n'))
            print(rubrics[select_rubric][0])
            return rubrics[select_rubric][1]

        # 3 Получаем под-Рубрику
        def get_sub_rubric(soup):
            # global soup
            # global sel_rubric
            rubrics.clear()
            for rubric in soup.findAll(class_="rubrics-list"):
                for link in rubric.findAll('li'):
                    refer = link.find('a')['href']
                    rubrics.append([refer.split('/')[3], "https://somon.tj" + refer])

            for i, rub in enumerate(rubrics):
                print(f'№:{i} - {rub[0]}')
                # Выбираем рубрику
            select_rubric = int(input('Выберите рубрику №: ! \n'))

            print(rubrics[select_rubric][0], rubrics[select_rubric][1])
            html = req.get(rubrics[select_rubric][1], headers)
            soup = bs(html.text, 'lxml')

        rubric_link = get_rubrics()
        html = req.get(rubric_link, headers)
        if bs(html.text, 'lxml').find(class_="rubrics-list").findAll('li'):
            soup = bs(html.text, 'lxml')
            get_sub_rubric(soup)  # Парсим под рубрику если она имеется!
        else:
            print('Под_рубрики не найдены!')



if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
