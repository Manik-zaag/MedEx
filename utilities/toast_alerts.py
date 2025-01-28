from selenium.webdriver.common.by import By

from pages.BasePage import BasePage
from icecream import ic


class ToastAlerts(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Toast alert locators
        self.toast_title = (By.XPATH, "//div[@class='ant-notification-notice-message']")
        self.toast_description = (By.XPATH, "//div[@class='ant-notification-notice-description']")
        self.toast_icon_for_success = (By.XPATH, "//div/span[@aria-label='check-circle']")
        self.toast_icon_for_error = (By.XPATH, "//div/span[@aria-label='close-circle']")
        self.toast_cancel_button = (By.XPATH, "//a[@aria-label='Close']")

    def retrieve_toast_warning_title(self):
        element = self.wait_for_element_visibility(self.toast_title, 5)
        return element.text

    def retrieve_toast_warning_message(self):
        element = self.wait_for_element_visibility(self.toast_description, 5)
        return element.text

    def is_toast_success(self) -> bool:
        # Check if the toast has a success icon
        self.wait_for_element_visibility(self.toast_icon_for_success)
        return self.is_element_displayed(self.toast_icon_for_success)

    def is_toast_error(self) -> bool:
        # Check if the toast has an error icon
        self.wait_for_element_visibility(self.toast_icon_for_error)
        return self.is_element_displayed(self.toast_icon_for_error)

    def close_toast(self):
        # Close the toast
        element = self.wait_for_element_clickable(self.toast_cancel_button)
        element.click()

    def handle_toast_success(self):
        if self.is_toast_success():
            title = self.retrieve_toast_warning_title()
            description = self.retrieve_toast_warning_message()
            self.close_toast()
            return {"title": title, "description": description, "status": "success"}
        else:
            raise Exception("Success toast not found.")

    def handle_toast_error(self):
        if self.is_toast_error():
            title = self.retrieve_toast_warning_title()
            description = self.retrieve_toast_warning_message()
            self.close_toast()
            return {"title": title, "description": description, "status": "error"}
        else:
            raise Exception("Error toast not found.")


"""
# Access Toast return
# Assume `toast_alerts` is an instance of the ToastAlerts class
toast_alerts = ToastAlerts(driver)

# Handle a success toast
try:
    success_toast = toast_alerts.handle_toast_success()
    print("Toast Details:")
    print(f"Title: {success_toast['title']}")
    print(f"Description: {success_toast['description']}")
    print(f"Status: {success_toast['status']}")
except Exception as e:
    print(f"Error handling success toast: {str(e)}")

# Handle an error toast
try:
    error_toast = toast_alerts.handle_toast_error()
    print("Toast Details:")
    print(f"Title: {error_toast['title']}")
    print(f"Description: {error_toast['description']}")
    print(f"Status: {error_toast['status']}")
except Exception as e:
    print(f"Error handling error toast: {str(e)}")
"""
