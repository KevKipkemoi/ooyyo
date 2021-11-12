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
        self.rest = []
        self.headers = []
        self.driver = webdriver.Chrome(service=_service, options=chrome_options)
        self.driver.get(_URL)

        self.ANDROID_APP_MODAL = '//*[@id="o-modal-1636619015751"]/div'
        self.ANDROID_APP_CANCEL_BTN = '//*[@id="o-modal-1636619015751"]/div/div/div[2]/button[1]'
        self.SEARCH_BTN = '/html/body/section/div[1]/div/div/div[2]/div/div/div[5]/div[4]/a'
        self.COUNTRY_DROPDOWN_INPUT = '/html/body/section/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/input'
        self.COUNTRIES = '/html/body/section/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/ul'
        self.RESULT_NUM = '/html/body/section/div[2]/h2'
        self.CAR_DETAILS = '/html/body/section/div[2]/div/div[4]/a[1]/div[2]/div[2]/h2'
        self.CAR_LOCATION = '/html/body/section/div[2]/div/div[4]/a[1]/div[2]/div[2]/div/div[1]/div[1]/span[1]/strong'
        self.CAR_MILEAGE = '/html/body/section/div[2]/div/div[4]/a[1]/div[2]/div[2]/div/div[1]/div[3]/strong'
        self.CAR_DETAILS = '/html/body/section/div[2]/div/div[4]/a[1]/div[2]/div[2]/div/div[1]/div[4]'
        self.CAR_PRICE = '/html/body/section/div[2]/div/div[4]/a[1]/div[2]/div[2]/div/div[2]/div/span[2]'
        self.CAR_CARD = '/html/body/section/div[2]/div/div[4]/a[1]'
        self.CAR_COLUMN = '/html/body/section/div[2]'

        self.navigate_to_country(country = country)

    def navigate_to_country(self, country):
        country = country.capitalize()
        if country == "Germany":
            pass
        else:
            element = self.driver.find_element(By.XPATH, self.COUNTRY_DROPDOWN_INPUT)
            element.click()
            li_elem = self.driver.find_element(By.XPATH, self.COUNTRIES).find_elements(By.TAG_NAME, 'li')
            for item in li_elem:
                if item.text.split('\n')[0] == country:
                    item.click()
                    break
        self.driver.find_element(By.XPATH, self.SEARCH_BTN).send_keys(Keys.RETURN)


if __name__ == '__main__':
    scrapper = Scrapper("Austria")
    scrapper.driver.quit()
    