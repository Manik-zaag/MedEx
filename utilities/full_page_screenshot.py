import os
import time


# To take Full Page ScreenShot
# Must run in Headless mode
def take_full_page_screen_shot(context, folder_path="screenshots"):
    # Get the original window size
    original_size = context.driver.get_window_size()  # Use context.driver
    web_page_width = original_size['width']

    # Calculate the full height of the page
    web_page_height = context.driver.execute_script(
        "return Math.max(document.body.scrollHeight, "
        "document.body.offsetHeight, document.documentElement.clientHeight, "
        "document.documentElement.scrollHeight, document.documentElement.offsetHeight);"
    )

    # Set the window size to the full page dimensions
    context.driver.set_window_size(width=web_page_width, height=web_page_height)

    # Take FUll page screenshot
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    screenshot_path = os.path.join(folder_path, f"full_page_screenshot_{int(time.time())}.png")
    context.driver.save_screenshot(screenshot_path)