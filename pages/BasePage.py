from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from icecream import ic


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def navigate_to_base_url(self, url):
        self.driver.get(url)

    def get_element(self, locator, parent_element=None):
        """
        Returns a web element identified by the locator.
        """
        if parent_element:
            return parent_element.find_element(*locator)
        return self.driver.find_element(*locator)
        # return self.wait_for_element_presence(locator)

    def get_elements(self, locator):
        """
        Returns a list of web elements identified by the locator.
        """
        return self.driver.find_elements(*locator)

    def get_attribute_value(self, locator, attribute_name):
        """
        Get the value of a specific attribute of an element.

        :param locator: Locator tuple (e.g., (By.ID, 'element_id')).
        :param attribute_name: The name of the attribute to get the value for (e.g., 'href', 'value', 'class', etc.).
        :return: The value of the attribute as a string or None if the attribute is not found.
        """
        try:
            element = self.get_element(locator)
            return element.get_attribute(attribute_name)
        except Exception as e:
            ic(f"Error getting attribute value: {e}")
            return None

    def get_value_of_css_property(self, locator, css_property):
        """
        Method to get the value of a CSS property for a specific element.
        """
        element = self.get_element(locator)
        return element.value_of_css_property(css_property)

    def click_on_element(self, locator):
        """
        Clicks on the element identified by the locator.
        """
        self.get_element(locator).click()

    def clear_element_text(self, locator):
        """
        Clears the text of the element identified by the locator.
        """
        self.get_element(locator).clear()

    def write_on_element(self, locator, text):
        """
        Types the given text into the element identified by the locator.
        """
        element = self.get_element(locator)
        element.clear()
        element.send_keys(text)

    def get_element_text(self, locator):
        """
        Returns the text of the element identified by the locator.
        """
        return self.get_element(locator).text.strip()

    def is_element_displayed(self, locator):
        """
        Checks if the element identified by the locator is displayed.
        """
        return self.get_element(locator).is_displayed()

    def is_element_enabled(self, locator):
        """
        Checks if the element identified by the locator is enabled.
        """
        return self.get_element(locator).is_enabled()

    def is_element_selected(self, locator):
        """
        Checks if the element identified by the locator is selected.
        """
        return self.get_element(locator).is_selected()

    def get_page_title(self):
        """
        Returns the title of the current page.
        """
        return self.driver.title

    def switch_to_frame(self, frame_locator):
        """
        Switches to the frame identified by the locator.
        """
        frame = self.get_element(frame_locator)
        self.driver.switch_to.frame(frame)

    def execute_js(self, script):
        """
        Executes JavaScript code in the context of the current page.
        """
        return self.driver.execute_script(script)

    def scroll_to_element(self, locator):
        """
        Scrolls the page to bring the element into view.
        """
        element = self.get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def hover_over_element(self, locator):
        """
        Performs a hover action over the element identified by the locator.
        """
        element = self.get_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def select_dropdown_by_visible_text(self, locator, visible_text):
        """
        Selects an option from a dropdown by visible text.
        """
        select = Select(self.get_element(locator))
        select.select_by_visible_text(visible_text)

    def select_dropdown_by_index(self, locator, index):
        """
        Selects an option from a dropdown by index.
        Index starts from 0 for the first option.
        """
        select = Select(self.get_element(locator))
        select.select_by_index(index)

    def select_option_from_dynamic_dropdown(self, dropdown_locator, option_text):
        """
        Selects an option from a dynamic dropdown based on the provided text.
        This method waits until the dropdown options are loaded.
        """
        try:
            # Wait until the dropdown is visible and enabled
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(dropdown_locator))

            # Create a Select object
            dropdown = Select(self.get_element(dropdown_locator))

            # Wait until options are loaded in the dropdown
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"{dropdown_locator[1]}/option"))
            )

            # Select the option by visible text
            dropdown.select_by_visible_text(option_text)

        except TimeoutException:
            print(f"Timeout: Dropdown {dropdown_locator} or its options did not load within 10 seconds.")

    def select_dropdown_by_value(self, locator, value):
        """
        Selects an option from a dropdown by value attribute.
        """
        select = Select(self.get_element(locator))
        select.select_by_value(value)

    def drag_and_drop(self, source_locator, target_locator):
        """
        Drags the source element to the target element.
        """
        source_element = self.get_element(source_locator)
        target_element = self.get_element(target_locator)
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()

    def get_current_url(self):
        """
        Returns the current URL of the page.
        """
        return self.driver.current_url

    def open_new_tab(self, url=None):
        """
        Opens a new tab in the browser. If `url` is provided, navigates to that URL.
        """
        self.driver.execute_script("window.open();")
        if url:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get(url)

    def switch_to_window(self, window_index=0):
        """
        Switches to the window/tab specified by index.
        """
        self.driver.switch_to.window(self.driver.window_handles[window_index])

    def close_current_tab(self):
        """
        Closes the current tab.
        """
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def alert_accept(self):
        """
        Accepts (clicks OK) on an alert pop-up.
        """
        self.driver.switch_to.alert.accept()

    def alert_dismiss(self):
        """
        Dismisses (clicks Cancel) on an alert pop-up.
        """
        self.driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        """
        Returns the text present in the alert pop-up.
        """
        return self.driver.switch_to.alert.text

    def switch_to_frame_by_index(self, index):
        """
        Switches to a frame based on its index.
        """
        self.driver.switch_to.frame(index)

    def switch_to_frame_by_name_or_id(self, name_or_id):
        """
        Switches to a frame based on its name or ID.
        """
        self.driver.switch_to.frame(name_or_id)

    def switch_to_parent_frame(self):
        """
        Switches to the parent frame from the current frame.
        """
        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        """
        Switches to the default content from a previously switched frame.
        """
        self.driver.switch_to.default_content()

    def refresh_page(self):
        """
        Refreshes the current page.
        """
        self.driver.refresh()

    def navigate_back(self):
        """
        Navigates back to the previous page in the browser history.
        """
        self.driver.back()

    def navigate_forward(self):
        """
        Navigates forward to the next page in the browser history.
        """
        self.driver.forward()

    def execute_script(self, script, *args):
        """
        Executes JavaScript code in the context of the current page.
        """
        return self.driver.execute_script(script, *args)

    def scroll_to_top(self):
        """
        Scrolls to the top of the page.
        """
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the page.
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def send_enter_key(self, locator):
        """
        Sends the Enter key to an element identified by the locator.
        """
        element = self.get_element(locator)
        element.send_keys(Keys.ENTER)

    def upload_file(self, locator, file_path):
        """
        Uploads a file to an input element identified by the locator.
        """
        element = self.get_element(locator)
        element.send_keys(file_path)

    def get_page_source(self):
        """
        Returns the page source of the current page.
        """
        return self.driver.page_source

    def get_cookies(self):
        """
        Returns all cookies of the current session.
        """
        return self.driver.get_cookies()

    def delete_all_cookies(self):
        """
        Deletes all cookies of the current session.
        """
        self.driver.delete_all_cookies()

    def add_cookie(self, cookie_dict):
        """
        Adds a cookie to the current session.
        """
        self.driver.add_cookie(cookie_dict)

    def maximize_window(self):
        """
        Maximizes the current browser window.
        """
        self.driver.maximize_window()

    def minimize_window(self):
        """
        Minimizes the current browser window.
        """
        self.driver.minimize_window()

    def fullscreen_window(self):
        """
        Puts the current browser window in full-screen mode.
        """
        self.driver.fullscreen_window()

    def capture_screenshot(self, filename):
        """
        Takes a screenshot of the current page and saves it to the specified filename.
        """
        self.driver.save_screenshot(filename)

    def close_browser(self):
        """
        Closes the current browser session.
        """
        self.driver.quit()

    def wait_for_element_visibility(self, locator, timeout=10):
        """
        Waits for the element identified by the locator to be visible.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not visible after {timeout} seconds.")

    def wait_for_element_invisibility(self, locator, timeout=10):
        """
        Waits for the element identified by the locator to be invisible (not displayed or not present).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} still visible after {timeout} seconds.")

    def wait_until_element_disappears(self, locator, timeout=10):
        """
        Waits until the element identified by the locator disappears from the DOM.
        """
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            print("Search results not found within timeout period.")

    def wait_for_element_presence(self, locator, timeout=10):
        """
        Waits for the element identified by the locator to be present in the DOM.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not present in DOM after {timeout} seconds.")

    def wait_for_all_elements_presence(self, locator, timeout=10):
        """
        Waits for all elements identified by the locator to be present in the DOM.
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except TimeoutException:
            raise NoSuchElementException(f"Elements {locator} not present in DOM after {timeout} seconds.")

    def wait_for_element_to_be_selected(self, locator, timeout=10):
        """
        Waits for the element identified by the locator to be selected (like a checkbox being checked).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_selected(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not selected after {timeout} seconds.")

    def wait_for_element_clickable(self, locator, timeout=10):
        """
        Waits for the element identified by the locator to be clickable.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not clickable after {timeout} seconds.")

    def wait_for_alert(self, timeout=10):
        """
        Waits for an alert to be present on the page.
        """
        try:
            alert = WebDriverWait(self.driver, timeout).until(
                EC.alert_is_present()
            )
            return alert
        except TimeoutException:
            raise TimeoutException(f"No alert present after {timeout} seconds.")

    def wait_for_alert_to_disappear(self, timeout=10):
        """
        Waits for the alert to disappear from the page (if it was present).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'alert')]"))
            )
        except TimeoutException:
            raise TimeoutException(f"Alert did not disappear after {timeout} seconds.")

    def wait_for_element_to_be_enabled(self, locator, timeout=10):
        """
        Waits for the element to be enabled (e.g., a button or input field).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_enabled(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} not enabled after {timeout} seconds.")

    def wait_for_element_to_have_text(self, locator, text, timeout=10):
        """
        Waits for the element identified by the locator to contain the specified text.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(locator, text)
            )
        except TimeoutException:
            raise TimeoutException(f"Text '{text}' not present in element {locator} after {timeout} seconds.")

    def wait_for_element_to_have_value(self, locator, value, timeout=10):
        """
        Waits for an element (e.g., input field) to have a specific value.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element_value(locator, value)
            )
        except TimeoutException:
            raise TimeoutException(f"Element {locator} does not have the value '{value}' after {timeout} seconds.")

    def wait_for_element_to_have_attribute(self, locator, attribute, value, timeout=10):
        """
        Waits for an element to have a specific attribute with a specific value.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.attribute_to_be(locator, attribute, value)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} does not have attribute '{attribute}' with value '{value}' after {timeout} seconds.")

    def wait_for_frame_to_be_available_and_switch_to_it(self, locator, timeout=10):
        """
        Waits for the frame to be available and switches to it.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
        except TimeoutException:
            raise TimeoutException(f"Frame {locator} not available for switching after {timeout} seconds.")

    def wait_for_window_to_be_available_and_switch(self, timeout=10):
        """
        Waits for a new browser window or tab to be available and switches to it.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.new_window_is_opened(self.driver.window_handles)
            )
            self.driver.switch_to.window(self.driver.window_handles[-1])
        except TimeoutException:
            raise TimeoutException(f"No new window or tab opened after {timeout} seconds.")

