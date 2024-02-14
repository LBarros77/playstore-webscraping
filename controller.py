from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep


class Base:
    def __init__(self):
        self.url = "https://play.google.com/store/apps/details?id=com.eventbrite.attendee"
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def set_up(self):
        self.driver.implicitly_wait(2)
        self.driver.get(self.url)

    def tear_down(self):
        self.driver.quit()


class AppInfo(Base):
    def __init__(self):
        super().__init__()

    def get_description_list(self):
        self.set_up()
        data_description = self.driver.find_element(By.CSS_SELECTOR, "data-g-id#description")
        descrition = [word.text for word in data_descrition]
        return description

    def get_description(self):
        descriptions = self.get_description_list()
        description = ""
        for words in descriptions:
            if(words is not None):
                description += words
        return description

    def has_name_in_description(self, name):
        data_description = self.driver.find_element(By.XPATH, "//section[@data-g-id='description']")
        description = BeautifulSoup(data_description.page_source, "html.parser")
        return True if description.find(string=re.compile(name)) else False


class RatingsAndReviews(Base):
    def __init__(self, url=None):
        super().__init__()

    def get_reviews_number(self):
        fragments = self.driver.find_element(By.XPATH, "//section[@data-g-id='reviews']")
        reviews_number = BeautifulSoup(fragments.page_source, "html.parser")
        reviews_number = reviews_number.find(class_="EHUI5b").text()
        return reviews_number.trip()

    def get_star_number(self):
        element = self.driver.find_element(By.XPATH, "//section[@data-g-id='reviews']")
        fragments = BeautifulSoup(element.page_source, "html.parser")
        star_number = fragments.find(class_="jILTFe").text()
        return star_number.strip()

    def get_views(self):
        self.browser.find_element(By.CSS_SELECTOR, ".Jwxk6d > div:nth-child(5) > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)").click()
        elements = self.driver.find_element(By.CSS_SELECTOR, "div.RHo1pe:nth-child(1)")
        fragments = elements.get_attribute("outerHTML")
        views = BeautifulSoup(fragments, "html.parser")
        return views


if __name__== "__main__":
    app = AppInfo()
    description = app.get_description_list()
    print(description)
    app.tear_down()
