from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from vacancy import Vacancy
from time import sleep
import re

input_search = (By.CSS_SELECTOR, 'input[name="text"]')
button_search = (By.CLASS_NAME, 'magritte-button-view___53Slm_5-1-17')

vacancy_search_block = (By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__results"]')
vacancy_search_result = (By.CSS_SELECTOR, 'div[data-sentry-element="Element"]')

button_close_tab = (By.CLASS_NAME, 'bloko-modal-close-button')


text_view_founded = (By.CSS_SELECTOR, 'span[data-qa="vacancies-total-found"]')

name_vacancy = (By.CSS_SELECTOR, 'span[data-qa="serp-item__title-text"]')
salary_vacancy = (By.CSS_SELECTOR, 'span[data-sentry-element="Text"]')
ref_vacancy = (By.CSS_SELECTOR, 'a[data-qa="serp-item__title"]')

class HhPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    def open(self, link):
        self.browser.get(link)

    def button_search_click(self):
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_element_located(button_search))
        return self.find(button_search).click()
    
    def input_work(self, text):
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_element_located(input_search))
        self.find(input_search).send_keys(text)

    def button_close_tab_click(self):
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_element_located(button_close_tab))
        return self.find(button_close_tab).click()
    

    def extract_number(self, text):
        pattern = r'[-+]?\d*[\s.,]?\d+'  
        match = re.search(pattern, text)

        if match:
            number = match.group(0).replace(' ', '').replace(',', '.')
            return int(number)
        else:
            return None  

    def check_count_vacancy(self):
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_element_located(text_view_founded))
        try:
            res = self.find(text_view_founded).text
        except:
            print('not found text_view_founded')
        try:
            return self.extract_number(res)
        except:
            return 0

    def extract_salary_and_currency(self, text):
        text = text.replace('\u202f', ' ')
        pattern = r'(\d[\d\s]*[\d]?)\s*[-–]?\s*(\d[\d\s]*[\d]?)?\s*([₽$€£¥])' 
        match = re.search(pattern, text)
        if match:
            min_salary = match.group(1).replace(' ', '')  
            max_salary = match.group(2).replace(' ', '') if match.group(2) else None 
            currency = match.group(3)
            if max_salary is not None:
                max_salary = max_salary
            else:
                max_salary = '-'
            
            return min_salary, max_salary, currency
        else:
            return '-', '-', '-'  

    def get_vacancy_by_request(self):
        wait = WebDriverWait(self.browser, 15)
        wait.until(EC.presence_of_element_located(vacancy_search_result))
        vacancy_block = self.find(vacancy_search_block)
        vacancy_elements = self.find_elements_from_block(vacancy_block, vacancy_search_result)
        vacancy_result = []
        i = 1 
        for el in vacancy_elements:
            print(f'Обработка {i}-ой вакансии...')
            try:
                nameVacancy = self.find_element_from_block(el, name_vacancy).text 
            except:
                nameVacancy = '-'
            try:         
                linkVacancy = self.find_element_from_block(el, ref_vacancy).get_attribute('href')  
            except:
                linkVacancy =  '-'        
            try:
                salaryVacancy = self.find_element_from_block(el, salary_vacancy).text
                salMin, salMax, salVal = self.extract_salary_and_currency(salaryVacancy)           
            except:
                salMin, salMax, salVal = '-', '-', '-'
 
            vacancy_el = Vacancy()
            vacancy_el.name = nameVacancy
            vacancy_el.refVacancy = linkVacancy
            vacancy_el.salaryzMax = salMax
            vacancy_el.salaryzMin = salMin
            vacancy_el.valuta = salVal
            vacancy_result.append(vacancy_el)
            i+=1
            
        return vacancy_result

    
        
    