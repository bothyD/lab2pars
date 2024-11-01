from pages.hh_page import HhPage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from vacancy import Vacancy
import json
import pandas as pd

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json_data = [el.to_dict() for el in data]  
        json.dump(json_data, f, ensure_ascii=False, indent=4) 

def display_with_pandas(data):
    df = pd.DataFrame([el.to_dict() for el in data])  
    print(df) 

def create_browser():
    options = Options()
    options.add_argument('--headless')  
    chrome_browser = webdriver.Chrome(service=Service(), options=options)
    chrome_browser = webdriver.Chrome(options)
    chrome_browser.implicitly_wait(10)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    for key, value in headers.items():
        chrome_browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": value})
        chrome_browser.execute_cdp_cmd('Network.setExtraHTTPHeaders', {"headers": {key: value}})
    return chrome_browser

def main():
    input_text = input("Введите инетерсную вакансию:   ")
    url = 'https://novosibirsk.hh.ru/'  
    browser = create_browser()  
    page = HhPage(browser)
    page.open(url)
    sleep(12)
    # try:      
    #     page.input_work((input_text))
    #     page.button_search_click()
    # except:
    #     print('dead try(')    
    # try:
    #     page.button_close_tab_click()
    # except:
    #     print('cant close tab')
    
    # try:
    #     res = page.check_count_vacancy()
    #     print(f'кол-во - {res}')
    # except:
    #     print('не посчиталось')


    # try:
    #     sleep(35)
    #     result = page.get_vacancy_by_request()
    #     print('кол-во найденных вакансий  - ', len(result))
    # except:
    #     print('not found(')
    # try:
    #     save_to_json(result, 'jobs.json')
    # except:
    #     print('not json')
    # try:

    #     display_with_pandas(result)
    # except:
    #     print('not dispaly pandas')
    browser.quit() 

if __name__ == "__main__":
    main()
