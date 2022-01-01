import os
import constants
from selenium import webdriver


class ReadingSite(webdriver.Chrome):
    def __init__(self, driver_path=r"D:/SeleniumDrivers", teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += driver_path
        super(ReadingSite, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def reading_site_home_page(self):
        self.get(constants.READING_SITE_URL)

    def search_title(self, title, alt_titles):
        search_btn = self.find_element_by_css_selector(
            'li[class="menu-search"]'
        )
        search_btn.click()
        search_input = self.find_element_by_css_selector(
            'input[name="s"]'
        )
        search_input.clear()
        search_input.send_keys(title)
        titles_list = self.find_element_by_id(
            "ui-id-1"
        ).find_elements_by_class_name("search-item")

        done = False
        while len(titles_list) != 1 and not done:
            for at in alt_titles:
                search_input.clear()
                search_input.send_keys(at)
                titles_list = self.find_element_by_id(
                    "ui-id-1"
                ).find_elements_by_class_name("search-item")
            done = True

        titles_list[0].click()
