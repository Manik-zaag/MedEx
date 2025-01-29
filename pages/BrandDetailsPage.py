from datetime import time

from icecream import ic
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class BrandDetailsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.brand_name_locator = (By.XPATH, "//div[@title='Generic Name']/preceding-sibling::div/h1")
        self.generic_name_locator = (By.XPATH, "//div[@title='Generic Name']")
        self.strength_locator = (By.XPATH, "//div[@title='Generic Name']")
        self.manufactured_by_locator = (By.XPATH, "//div[@title='Generic Name']")
        self.generic_name_locator = (By.XPATH, "//div[@title='Generic Name']")

    def retrieve_current_url(self):
        return self.get_current_url()

    class BrandDetailsPage:
        def __init__(self, driver):
            self.driver = driver

        def retrieve_details(self):
            details = {}
            try:
                details['brand_name'] = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[contains(@class, 'brand-name') or contains(text(), 'Brand')]"))
                ).text
                details['generic_name'] = self.driver.find_element(By.XPATH,
                                                                   "//div[contains(text(), 'Omeprazole')]").text
                details['strength'] = self.driver.find_element(By.XPATH, "//div[contains(text(), 'mg')]").text
                details['manufacturer'] = self.driver.find_element(By.XPATH,
                                                                   "//div[contains(text(), 'ACI Limited')]").text
                details['unit_price'] = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Unit Price')]").text
                details['strip_price'] = self.driver.find_element(By.XPATH,
                                                                  "//div[contains(text(), 'Strip Price')]").text
            except Exception as e:
                print("Error retrieving details:", e)
            return details