import os
import re
import constants
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import math


class Bot(webdriver.Chrome):
    def __init__(self, driver_path=r"D:/SeleniumDrivers", teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += driver_path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        super(Bot, self).__init__(options=options)
        self.implicitly_wait(30)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def anime_planet_home_page(self):
        self.get(constants.ANIME_PLANET_URL)
        # check if logged in (if not, log in)
        login_link = self.find_element_by_css_selector(
            'a[href="/login"]'
        )
        if login_link:
            login_link.click()
            username_input = self.find_element_by_id("username")
            password_input = self.find_element_by_id("password")
            username = os.getenv('ANIME_PLANET_USERNAME')
            password = os.getenv('ANIME_PLANET_PASS')
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_btn = self.find_element_by_id("loginButton")
            login_btn.click()

    def get_reading_list(self):
        a = ActionChains(self)
        profile_badge = self.find_element_by_class_name("loggedIn")
        a.move_to_element(profile_badge).perform()
        my_manga_link = self.find_element_by_css_selector(
            'a[href$="/manga/reading"]'
        )
        my_manga_link.click()

        self.refresh()

        reading_list_cards = self.find_element_by_class_name(
            'cardGrid'
        ).find_elements_by_css_selector(
            'li[data-type="manga"]'
        )

        reading_list = []
        for manga_el in reading_list_cards:
            manga_title = manga_el.find_element_by_css_selector(
                'h3[class="cardName"]'
            ).get_attribute('innerHTML').strip()
            chapters_read = manga_el.get_attribute("data-episodes")
            manga_el_info = manga_el.find_element_by_class_name("tooltip")
            manga_info = manga_el_info.get_attribute("title")

            # Extract alt title info
            reg_str = "<h6 class='theme-font tooltip-alt'>(.*?)</h6>"
            alt_title_res = re.findall(reg_str, manga_info)
            alt_titles = []
            if len(alt_title_res) == 1:
                alt_title_str = alt_title_res[0].replace('Alt title: ', '').replace('Alt titles: ', '')
                alt_titles.extend(alt_title_str.split(", "))

            reading_list.append({"title": manga_title, "chapters_read": chapters_read, "alt_titles": alt_titles})

        return reading_list

    def reading_site_home_page(self):
        self.get(constants.READING_SITE_URL)

    def search_title(self, title):
        search_btn = self.find_element_by_css_selector(
            'a[href="javascript:;"]'
        )
        search_btn.click()
        search_input = self.find_element_by_css_selector(
            'input[name="s"]'
        )
        search_input.clear()
        search_input.send_keys(title)
        search_input.send_keys(Keys.ENTER)

    def get_title_page(self, alt_titles):
        try:
            result_list = self.find_element_by_css_selector(
                'div[role="tabpanel"]'
            ).find_elements_by_css_selector(
                'h3'
            )
        except Exception as e:
            return "Error"

        if len(result_list) != 1:
            for res in result_list:
                link = res.find_element_by_css_selector('a')
                title = link.get_attribute('innerHTML').strip()
                href = link.get_attribute('href')
                if title in alt_titles:
                    return href
        else:
            link = result_list[0].find_element_by_css_selector('a')
            return link.get_attribute('href')

    def get_latest_chapter(self, link, chapters_read):
        if link:
            self.get(link)
            print(link)
            summary_image = self.find_element_by_css_selector(
                'div[class="summary_image"]'
            ).find_element_by_css_selector('img')
            summary_content = self.find_element_by_class_name(
                'summary__content'
            )

            image = summary_image.get_attribute('src')
            summary = summary_content.get_attribute('innerHTML').strip()

            latest_chapter_el = self.find_element_by_class_name(
                "listing-chapters_wrap"
            ).find_elements_by_css_selector('li>a')

            if len(latest_chapter_el) > 0:
                latest_chapter = 0
                read_chapters = 0
                try:
                    latest_chapter = float(latest_chapter_el[0].get_attribute('innerHTML').strip()[8:])
                    read_chapters = float(chapters_read)
                except ValueError as e:
                    print(e)

                chap_diff = latest_chapter - read_chapters
                if chap_diff > 0:
                    j = math.floor(chap_diff)
                    while j < len(latest_chapter_el) - 1:
                        try:
                            chapter_no = float(latest_chapter_el[j].get_attribute('innerHTML').strip()[8:])
                        except ValueError:
                            print("Cannot convert to numerical. Skip...")
                            continue
                        if chapter_no == read_chapters:
                            return {
                                "latest_chapter": latest_chapter,
                                "chapters_read": read_chapters,
                                "read_latest_chapter": latest_chapter_el[0].get_attribute('href'),
                                "read_next_chapter": latest_chapter_el[j-1].get_attribute('href'),
                                "image": image,
                                "summary": summary
                            }
                        j += 1
            return {
                "latest_chapter": 0,
                "chapters_read": chapters_read,
                "read_latest_chapter": link,
                "read_next_chapter": link,
                "image": image,
                "summary": summary
            }
        else:
            return {
                "chapters_read": chapters_read
            }
