from datetime import time

from icecream import ic
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.BasePage import BasePage


class CompanyBrandsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.brand_links = []
        self.available_brand_name_title = (By.XPATH, "//small[normalize-space()='Available Brand Names']")
        self.view_all_brands = (By.XPATH, "//a[contains(text(),'View all')]")
        self.brands_names = (By.XPATH, "//div[@class='row']/div/a")
        self.next_button_locator = (By.XPATH, "//a[@rel='next']")
        self.active_page_locator = (By.XPATH, "//li[@class='page-item active']")
        self.last_page_locator = (By.XPATH, "parent::li/preceding-sibling::li[1]")

    def retrieve_current_url(self):
        return self.get_current_url()

    def check_all_brands_available(self):
        element = self.wait_for_element_visibility(self.available_brand_name_title, 5)
        all_brand_status = element.is_displayed()
        if not all_brand_status:
            self.click_on_element(self.view_all_brands)
            element = self.wait_for_element_visibility(self.available_brand_name_title, 5)
            all_brand_status = element.is_displayed()
            if not all_brand_status:
                ic("check_all_brands_available Status", all_brand_status)
            else:
                return True
        else:
            return True

    def collect_brand_links(self):
        brands = self.wait_for_all_elements_presence(self.brands_names)
        for brand in brands:
            link = brand.get_attribute("href")
            if link not in self.brand_links:
                self.brand_links.append(link)

    def handle_pagination(self):
        while self.check_all_brands_available():
            self.collect_brand_links()
            # ic(len(self.brand_links))
            # Check if there is a "Next" button
            try:
                next_button = self.get_element(self.next_button_locator)
            except NoSuchElementException:
                ic("No pagination available. Collected links from the current page.")
                return

            while True:
                try:
                    # Check if the "Next" button is displayed
                    if next_button.is_displayed():
                        active_page_number = int(self.get_element_text(self.active_page_locator))
                        # next_button = self.get_element(self.next_button_locator)
                        last_page = self.get_element(self.last_page_locator, parent_element=next_button)
                        last_page_number = int(last_page.text)
                        # ic(active_page_number, last_page_number)

                        for page in range(active_page_number, last_page_number + 1):
                            self.collect_brand_links()
                            ic(page, "Stored")
                            ic(len(self.brand_links))
                            if page < last_page_number:
                                try:
                                    next_button = self.wait_for_element_clickable(next_button)
                                    next_button.click()
                                    active_page_number = int(self.get_element_text(self.active_page_locator))
                                    next_button = self.get_element(self.next_button_locator)
                                    last_page = self.get_element(self.last_page_locator, parent_element=next_button)
                                    last_page_number = int(last_page.text)
                                    ic(active_page_number, last_page_number)
                                except NoSuchElementException:
                                    pass
                            else:
                                break
                    else:
                        break
                except NoSuchElementException:
                    ic("Reached the last page. No more pagination.")
                    break

