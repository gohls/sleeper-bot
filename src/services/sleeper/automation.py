import os
from decouple import config
from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

SLEEPER_BASE_URL = 'https://sleeper.com'
SLEEPER_LOGIN_URL = SLEEPER_BASE_URL + '/login'


class SleeperAutomationBot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SleeperAutomationBot, cls).__new__(cls)
            cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, wait=5):
        self.driver = Driver(uc=True)
        self.driver.implicitly_wait(wait) 
        self.is_logged_in = False

    def close(self):
        self.driver.close()

    def get_current_url(self):
        return self.driver.current_url

    def nav_to(self, nav_to):
        if nav_to is not self.get_current_url():
            self.driver.get(nav_to)

    def accept_cookies(self):
            try:
                accept_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_button.click() 
            except NoSuchElementException:
                pass

    def is_element_disabled(element):
        class_attribute = element.get_attribute("class")
        return "disable" in class_attribute

    def login(self, email="", password="") -> None:
        if self.is_logged_in:
            return 
        
        self.nav_to(SLEEPER_LOGIN_URL)
        time.sleep(5)

        if "login" not in self.get_current_url():
            # Assuming we are redirected when we are logged in
            self.is_logged_in = True
            return 
        
        email = email or os.getenv('EMAIL')
        password = password or os.getenv('PASSWORD')
        actions = ActionChains(self.driver)

        try:
            # Enter email, submit email, enter password, and submit password
            actions \
                .send_keys(email) \
                .send_keys(Keys.ENTER) \
                .pause(2) \
                .send_keys(password) \
                .pause(2) \
                .send_keys(Keys.ENTER) \
                .pause(2) \
                .perform()
            time.sleep(5)
            # Should be redirected after login success
            if "login" not in self.get_current_url():
                self.is_logged_in = True
        except Exception as e:
            print("An error occurred: ", e)

    def filter_players_in_draftroom(self, player=""):
        success = False
        try:
            self.driver.find_element(By.CLASS_NAME, "player-search") \
                .pause(2) \
                .find_element(By.TAG_NAME, "input") \
                .pause(2) \
                .send_keys(player)
            success = True
        except:
            success = False
        
        return success

    def draft_player(self, player):
        player_filtered = self.filter_availabe_player_in_draft(player)
        if player_filtered:
            self.driver.find_element(By.CLASS_NAME, "draft-button").click()

    def post_comment_to_league_chat(self, comment):
        player_filtered = self.filter_availabe_player_in_draft(comment)
        if player_filtered:
            self.driver.find_element(By.CLASS_NAME, "draft-button").click()

    def post_comment_to_league_chat(self, comment):
        player_filtered = self.filter_availabe_player_in_draft(comment)
        if player_filtered:
            self.driver.find_element(By.CLASS_NAME, "draft-button").click()

