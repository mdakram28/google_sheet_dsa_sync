

from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle

class LeetCode:

    def __init__(self) -> None:
        self.base_url = "https://leetcode.com"
        self.login_url = f"{self.base_url}/accounts/login/"
        self.problem_url = f"{self.base_url}/problems/"
    
    def __enter__(self):
        self.browser = webdriver.Chrome('./chromedriver')
        self.browser.get(self.base_url)
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.browser.add_cookie(cookie)
        except:
            traceback.print_exc()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.close()
    

    def login(self):
        self.browser.get(self.login_url)
        print(self.browser.current_url)
        while self.browser.current_url.startswith(self.login_url):
            sleep(2)
        pickle.dump(self.browser.get_cookies(), open("cookies.pkl", "wb"))

    def fetch_problem(self, url: str):
        url = url.strip(" /") + "/submissions/"
        print(url)
        self.browser.get(url)
        sleep(1)
        table = self.browser.find_element(By.CSS_SELECTOR, '.ssg__qd-splitter-primary-w div.bg-layer-1 .h-full.w-full')
        ret = []
        for row in table.find_elements(By.CSS_SELECTOR, 'div.py-3'):
            if 'Accepted' in row.get_attribute('innerText'):
                # print(row)
                ret.append({
                    'status': row.find_element(By.CSS_SELECTOR, 'span.font-medium').get_attribute('innerText'),
                    'date': row.find_element(By.CSS_SELECTOR, 'span.text-xs.text-label-3').get_attribute('innerText'),
                    'language': row.find_element(By.CSS_SELECTOR, 'span.text-xs.rounded-full.bg-blue-0').get_attribute('innerText')
                })
        return ret

