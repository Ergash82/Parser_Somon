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

       # Парсим выбранную рубрику и получаем количество страниц

        pages = soup.find_all(class_='page-number')
        if len(pages) > 0:
            page_n = int(pages[-1].text)
        else:
            page_n = 1

        # Запрашиваем с какого  и какое количество страниц хотим получить (записываем сылки в список)
        links = []

        def get_pages_link():
            print('Имеется: {} страниц'.format(page_n))
            end_page = int(input('Сколько страниц хотите получить? \n')) + 1
            start_page = int(input('С какой страницы начнем? \n')) - 1
            if page_n > 1:
                for page, _ in zip(range(start_page - 1, end_page + 1), tqdm(range(start_page, end_page))):
                    response = req.get(url=f'{rubrics[sel_rubric][1]}?page={page}', headers=headers)
                    soup = bs(response.text, 'lxml')
                    refer = soup.find_all(class_="card__title-link")
                    if len(refer) == 0:
                        refer = soup.find_all('a', class_="mask")

                    time.sleep(1)  # for progress bar
                    for link in refer:
                        links.append(f"https://somon.tj/{link['href']}")
                print('\nИмеется: {} записей'.format(len(links)))
            else:
                response = req.get(url=rubrics[sel_rubric][1], headers=headers)
                soup = bs(response.text, 'lxml')
                refer = soup.find_all(class_="card__title-link")
                if len(refer) == 0:
                    refer = soup.find_all('a', class_="mask")

                time.sleep(1)  # for progress bar
                for link in refer:
                    links.append(f"https://somon.tj/{link['href']}")
                print('\nИмеется: {} записей'.format(len(links)))

            if len(links) > 0:
                return 1
            else:
                print('Записи отсуствуют!')
                return 0

        get_pages_link()

# Парсим необходимые данные со страниц
        data = []
        header = []

        # Получение доп. данных со страницы
        def get_chart(soup):
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/107.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            chart_dict = {}
            chart_col = soup.find('ul', class_="chars-column").findAll('li')
            title = soup.find(id="ad-title").text.strip().replace('\n', '')
            location = soup.find(class_="announcement-meta__left").find('span', attrs={"itemprop": "address"}).text
            details = soup.find(class_="announcement__details").find('span', class_="date-meta").text.strip()
            price = soup.find(class_="announcement-price__cost").find('meta', itemprop="price").get('content').replace(
                '.',
                ',')
            description = soup.find(class_="announcement-description").text.strip()

            chart_dict['Имя'] = title
            chart_dict['Цена'] = price
            try:
                phone_check = soup.find(class_="phone-author")['data-url']
                response = req.get(url="https://somon.tj/" + phone_check, headers=headers)
                phone_number = response.json()['tel']
                chart_dict['Телф'] = phone_number
            except:
                print('нет номера телефона')

            def get_chart(chart_col):
                try:
                    for chart in chart_col:
                        key_char = chart.find(class_="key-chars").text
                        key_char_val = chart.find(class_="value-chars").text
                        chart_dict[key_char] = key_char_val.strip()
                except:
                    print('Нет дополнительной информации')

            get_chart(chart_col)

            chart_dict['Регион'] = location
            chart_dict['Статус'] = details
            chart_dict['Описание'] = description

            if chart_dict.keys() - header:
                for key in chart_dict.keys() - header:
                    header.append(key)
            return chart_dict

        # Запрос и Получение необходимых данных со всех выбранных страниц

        def get_pages_data(links):
            end_page = int(input('\nСколько записей хотите получить? ')) + 1
            start_page = int(input('С какой записи начнем? \n')) - 1

            for link, _ in zip(links[start_page:end_page], tqdm(links[start_page:end_page])):
                page = req.get(link, headers)
                soup2 = bs(page.text, 'lxml')
                try:
                    chart_col = soup2.find('ul', class_="chars-column").findAll('li')
                except:
                    continue
                data.append(get_chart(soup2))
                time.sleep(.1)  # for progress bar

        get_pages_data(links)


if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
