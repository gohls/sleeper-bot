import os
from typing import Optional
from seleniumbase import Driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
from functools import wraps


SLEEPER_BASE_URL = 'https://sleeper.com/'
SLEEPER_LOGIN_URL = SLEEPER_BASE_URL + 'login/'

def login_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_logged_in:
            print("Need to log in")
            return False
        else:
            return func(self, *args, **kwargs)
    return wrapper

def handle_exceptions(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return True if result is None else result
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            return False
    return wrapper

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

    @handle_exceptions
    def close(self) -> bool:
        self.driver.close()

    @handle_exceptions
    def accept_cookies(self) -> bool:
        accept_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click() 

    @handle_exceptions
    def get_current_url(self) -> str | bool:
        return self.driver.current_url
    
    @handle_exceptions
    def nav_to(self, nav_to) -> bool:
        if nav_to is not self.get_current_url():
            self.driver.get(nav_to)

    @handle_exceptions
    def login(self, email="", password="") -> bool:
        self.nav_to(SLEEPER_LOGIN_URL)
        time.sleep(5)

        # Assuming we are redirected when we try to go to login page
        if "login" not in self.get_current_url():
            self.is_logged_in = True
            return 
        
        try:
            self.accept_cookies()
        except Exception as e:
            print(f"Error accepting cookies: {str(e)}")
        
        time.sleep(1)

        email = email or os.getenv('EMAIL')
        password = password or os.getenv('PASSWORD')
        
       
        # Focus on username input field
        self.driver.find_element(By.TAG_NAME, "input").click()
        time.sleep(2)

        # Enter email, submit email, enter password, and submit password
        actions = ActionChains(self.driver)
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
        if SLEEPER_BASE_URL in self.get_current_url() and "login" not in self.get_current_url():
            self.is_logged_in = True

    '''
    GENERAL OPERATIONS
    '''
    @login_required
    @handle_exceptions
    def post_comment_to_league_chat(self, league_id=None, comment="") -> bool:
        league_id = league_id or os.getenv('LEAGUE_ID')

        self.nav_to(SLEEPER_BASE_URL + "leagues/" + str(league_id))
        time.sleep(5)

        # Focus on channel message text field
        self.driver.find_element(By.CLASS_NAME, "chat-input").find_element(By.TAG_NAME, "textarea").click()
        
        actions = ActionChains(self.driver)
        actions \
            .send_keys(comment) \
            .pause(2) \
            .send_keys(Keys.ENTER) \
            .pause(2) \
            .perform()
        time.sleep(5)
        
    @login_required
    @handle_exceptions
    def add_player(self, comment) -> bool:
        self.driver.find_element(By.CLASS_NAME, "chat-input") \
            .pause(2) \
            .find_element(By.TAG_NAME, "textarea") \
            .pause(2) \
            .send_keys(comment) \
            .send_keys(Keys.ENTER)
        
    @login_required
    @handle_exceptions
    def drop_player(self, comment) -> bool:
        self.driver.find_element(By.CLASS_NAME, "chat-input") \
            .pause(2) \
            .find_element(By.TAG_NAME, "textarea") \
            .pause(2) \
            .send_keys(comment) \
            .send_keys(Keys.ENTER)
        

    '''
    DRAFT OPERATIONS
    '''
    @login_required
    @handle_exceptions
    def draft_player(self, player) -> bool:
        player_filtered = self.filter_availabe_player_in_draft(player)
        if player_filtered:
            self.driver.find_element(By.CLASS_NAME, "draft-button") \
                .pause(2) \
                .click()

    @login_required
    @handle_exceptions
    def filter_players_in_draftroom(self, player="") -> bool:
        self.driver.find_element(By.CLASS_NAME, "player-search") \
            .pause(2) \
            .find_element(By.TAG_NAME, "input") \
            .pause(2) \
            .send_keys(player)

        

