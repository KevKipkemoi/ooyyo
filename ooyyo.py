import constants
import math
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Scrapper:
    def __init__(self, country = "Germany"):
        _URL = "https://www.ooyyo.com/"
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        _service = Service(ChromeDriverManager().install())
        self.total_results = 0
        self.car_details = []
        self.elements = []
        self.main_window = None
        self.driver = webdriver.Chrome(service=_service, options=chrome_options)
        self.driver.get(_URL)

        self.navigate_to_country(country = country)

    def navigate_to_country(self, country):
        country = country.capitalize()
        if country == "Germany":
            pass
        else:
            element = self.driver.find_element(By.XPATH, constants.COUNTRY_DROPDOWN_INPUT)
            element.click()
            li_elem = self.driver.find_element(By.XPATH, constants.COUNTRIES).find_elements(By.TAG_NAME, 'li')
            for item in li_elem:
                if item.text.split('\n')[0] == country:
                    item.click()
                    break
        self.driver.find_element(By.XPATH, constants.SEARCH_BTN).send_keys(Keys.RETURN)
        self.get_car_details()

    def find_total_navigations(self):
        return math.floor(int(self.driver.find_element(By.XPATH, constants.RESULT_NUM).text.split(' ')[2].replace(',', '')) / 15)

    def get_car_details(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        bs_info = soup.find_all("div", {"class": "info"})
        for idx, info in enumerate(bs_info):
            location = info.find("div", {"class": "location"}).get_text(strip=True)
            mileage = info.find("div", {"class": "mileage"}).get_text(strip=True)
            description = info.find("div", {"class": "description"}).get_text(strip=True)
            price_stat = info.find("div", {"class": "price-stat"}).get_text(strip=True)
            price_info = info.find("div", {"class": "price-info"}).get_text(strip=True)
            contact = self.navigate_to_contact(self.elements[idx], self.main_window)
            self.car_details.append([location, mileage, description, price_stat, price_info, contact])
        self.write_data(self.car_details)

    def write_data(self, details):
        workbook = xlsxwriter.Workbook('car_details.xlsx')
        worksheet = workbook.add_worksheet()
        for row_num, it in enumerate(details):
            worksheet.write_row(row_num, 0, it)
        workbook.close()

    def navigate_to_contact(self, element, main_window):
        element.click()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        html_source_code = self.driver.execute_script("return document.body.innerHTML;")
        html_soup = BeautifulSoup(html_source_code, 'html.parser')
        cnt_btn = html_soup.find("a", {"id": "contactSeller"})
        # self.driver.close()
        self.driver.switch_to.window(main_window)
        return cnt_btn['href']


if __name__ == '__main__':
    scrapper = Scrapper("Austria")
    scrapper.driver.quit()
    