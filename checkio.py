import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass
import pyperclip
from selenium.webdriver.common.keys import Keys


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
        self.base_url = "https://checkio.org"
        self.SEARCH_TEXT = "Python checkIO "
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def main_logic(self):
        self.login_to_checkio()
        # links = self.get_islands_links()
        unsolved_island_tasks = self.get_unsolved_tasks_from_island('https://py.checkio.org/station/home/')
        self.solve_tasks_on_island(unsolved_island_tasks)
        time.sleep(3)
        self.driver.quit()

    def solve_tasks_on_island(self, tasks_to_solve):
        for task in tasks_to_solve[:1]:
            self.solve_one_task(task)

    def solve_one_task(self, task):
        print('Solving current task: ', task.name)
        solution_links = self.get_google_solutions_for_task(task)
        for solution in solution_links:
            solution_code = self.copy_solution(solution)
            if self.solve_and_check_task(solution_code, task):
                break

    def solve_and_check_task(self, solution_code, task_obj):

        self.driver.get(f'{self.base_url}/{task_obj.link}')
        time.sleep(2)
        print("Click on Solve It button")
        try:
            self.driver.find_element_by_xpath("//a[@class='btn']").click()
        except ElementClickInterceptedException:
            self.driver.find_element_by_xpath("//div[@class='congratulation__body__accept']").click()
            time.sleep(2)
            self.driver.find_element_by_xpath("//a[@class='btn']").click()
        time.sleep(2)
        solution_textarea_element = self.driver.find_element_by_xpath("//textarea")
        solution_textarea_element.send_keys(Keys.COMMAND + "a")
        solution_textarea_element.send_keys(Keys.DELETE)

        for i in solution_code:
            solution_textarea_element.send_keys(i)
            solution_textarea_element.send_keys('\n')
            solution_textarea_element.send_keys(Keys.HOME)
        time.sleep(2)

        self.driver.find_element_by_id('check-code-btnEl').click()
        time.sleep(6)
        success_element = self.driver.find_elements_by_xpath("//div[@class='animation-success']")
        if len(success_element) > 0:
            print("Completed Task -: " + task_obj.name)
            return True
        else:
            print("Failed Task -: " + task_obj.name)
            return False

    def copy_solution(self, solution_link):
        self.driver.get(solution_link)
        time.sleep(2)
        publications_code = self.driver.find_element_by_xpath("//div[@class='publications__info__code']")
        solution_code = publications_code.find_elements_by_xpath("//span[@style='padding-right: 0.1px;']")
        curr_google_solution_code = []
        for data in solution_code:
            code_words = data.find_elements_by_css_selector('span')
            code_line = ""
            for word in code_words:
                code_line += word.text
            if len(code_line) > 0: curr_google_solution_code.append(code_line)
        return curr_google_solution_code

    def get_google_solutions_for_task(self, task):
        print("Google Search: Task - " + task.name + "\n")
        self.driver.get(self.google)
        time.sleep(2)
        searchbox = self.driver.find_element_by_name("q")
        searchbox.send_keys(self.SEARCH_TEXT + task.name)
        time.sleep(1)
        searchbox.submit()
        time.sleep(2)
        google_results = self.driver.find_elements_by_xpath("//div[@class='r']/a[contains(@href,'publications')]")
        current_google_result_links = []
        for results in google_results:
            current_google_result_links.append(results.get_attribute("href"))
        time.sleep(3)
        return current_google_result_links

    def get_unsolved_tasks_from_island(self, link_to_island):
        self.driver.get(link_to_island)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tasks = soup.find_all(class_='island-tasks__container')
        unsolved_tasks = []
        for task in tasks:
            try:
                task_status = task.find(class_='island-tasks__side__sign').get('title')
                if task_status != 'Solved':
                    title = task.find(class_='island-tasks__task__title').get('title')
                    link = task.find('a').get('href')
                    unsolved_tasks.append(Task(title, link))
            except Exception as e:
                print(e)
        return unsolved_tasks

    def get_islands_links(self):
        opened_stations = self.driver.find_elements_by_xpath("//div[contains(@class,'map__station_state_opened')]")
        opened_stations_links = []
        for link in opened_stations:
            opened_stations_links.append(
                link.find_element_by_css_selector('a.map__station__link').get_attribute("href"))
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
