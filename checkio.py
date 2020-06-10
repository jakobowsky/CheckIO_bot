import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass

def read_credentials():
    secrets = 'secrets.json'
    with open(secrets) as f:
        keys = json.loads(f.read())
        return keys

@dataclass
class Task:
    name: str
    link: str

class CheckIOSolver:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.google = "https://www.google.com/"
        self.base_url = "https://checkio.org/"
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def main_logic(self):
        self.login_to_checkio()
        # links = self.get_islands_links()
        self.get_unsolved_tasks_from_island('https://py.checkio.org/station/home/')
        time.sleep(3)
        self.driver.quit()

    def solve_tasks_on_island(self, link_to_island):
        pass

    def get_unsolved_tasks_from_island(self, link_to_island):
        self.driver.get(link_to_island)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tasks = soup.find_all(class_='island-tasks__container')
        unsolved_tasks = []
        for task in tasks:
            task_status = task.find(class_='island-tasks__side__sign').get('title')
            if task_status != 'Solved':
                title = task.find(class_='island-tasks__task__title').get('title')
                link = task.find('a').get('href')
                unsolved_tasks.append(Task(title, link))
        print(unsolved_tasks)


    def get_islands_links(self):
        opened_stations = self.driver.find_elements_by_xpath("//div[contains(@class,'map__station_state_opened')]")
        opened_stations_links = []
        for link in opened_stations:
            opened_stations_links.append(link.find_element_by_css_selector('a.map__station__link').get_attribute("href"))
        return opened_stations_links

    def login_to_checkio(self):
        self.driver.get(self.base_url)
        self.get_on_python_checkio()
        self.put_credentials_to_form()

    def put_credentials_to_form(self):
        try:
            # Enter user credentials and Click on Submit button to Logins
            self.driver.find_element_by_id("id_username").send_keys(self.login)
            time.sleep(2)
            password_field = self.driver.find_element_by_id("id_password")
            password_field.send_keys(self.password)
            password_field.submit()
            time.sleep(3)

        except NoSuchElementException:
            print("Exception NoSuchElementException")

    def get_on_python_checkio(self):
        try:
            self.driver.find_element_by_link_text('Python').click()
            time.sleep(2)
        except NoSuchElementException:
            print("incorrect Page")


if __name__ == '__main__':
    credentials = read_credentials()
    bot = CheckIOSolver(credentials['username'], credentials['password'])
    bot.main_logic()
