from datetime import time

from icecream import ic
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class CompanyPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.company_links = []
        self.title_of_company_page = (By.XPATH, "//h1[.='List of Pharmaceutical Companies']")
        self.compannies_name = (By.CSS_SELECTOR, "a[href*='/companies/']")
        self.next_button_locator = (By.XPATH, "//a[@rel='next']")
        self.active_page_locator = (By.XPATH, "//li[@class='page-item active']")
        self.last_page_locator = (By.XPATH, "parent::li/preceding-sibling::li[1]")

    def navigate_to_base_page(self, context):
        self.navigate_to_base_url(context.base_url)

    def display_status_of_company_page(self):
        element = self.wait_for_element_visibility(self.title_of_company_page)
        return element.is_displayed()
        # return self.is_element_displayed(self.title_of_login_page)

    def collect_company_links(self):
        companies = self.wait_for_all_elements_presence(self.compannies_name)
        for company in companies:
            link = company.get_attribute("href")
            if link not in self.company_links:
                self.company_links.append(link)

    def handle_pagination(self):
        active_page_number = int(self.get_element_text(self.active_page_locator))
        next_button = self.get_element(self.next_button_locator)
        last_page = self.get_element(self.last_page_locator, parent_element=next_button)
        last_page_number = int(last_page.text)
        # ic(active_page_number, last_page_number)

        for page in range(active_page_number, last_page_number+1):
            self.collect_company_links()
            # ic(page, "Stored")
            # ic(len(self.company_links))
            if page < last_page_number:
                try:
                    next_button = self.wait_for_element_clickable(next_button)
                    next_button.click()
                    active_page_number = int(self.get_element_text(self.active_page_locator))
                    next_button = self.get_element(self.next_button_locator)
                    last_page = self.get_element(self.last_page_locator, parent_element=next_button)
                    last_page_number = int(last_page.text)
                    # ic(active_page_number, last_page_number)
                except NoSuchElementException:
                    pass
