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
print('''
   ########     ###    ########   ######  ######## ########      ######   #######  ##     ##  #######  ##    ##     ########       ## 
   ##     ##   ## ##   ##     ## ##    ## ##       ##     ##    ##    ## ##     ## ###   ### ##     ## ###   ##        ##          ## 
   ##     ##  ##   ##  ##     ## ##       ##       ##     ##    ##       ##     ## #### #### ##     ## ####  ##        ##          ## 
   ########  ##     ## ########   ######  ######   ########      ######  ##     ## ## ### ## ##     ## ## ## ##        ##          ## 
   ##        ######### ##   ##         ## ##       ##   ##            ## ##     ## ##     ## ##     ## ##  ####        ##    ##    ## 
   ##        ##     ## ##    ##  ##    ## ##       ##    ##     ##    ## ##     ## ##     ## ##     ## ##   ### ###    ##    ##    ## 
   ##        ##     ## ##     ##  ######  ######## ##     ##     ######   #######  ##     ##  #######  ##    ## ###    ##     ######  
     ''')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
