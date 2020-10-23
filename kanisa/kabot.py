import os
import sys
import threading
import time
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException, TimeoutException, NoSuchElementException
)
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
from collections import OrderedDict
from .vituko import *


orders = []
editedOrders = []

botconfigs = {
    "refresh_rate": 100,
    "minDeadline": 0,
    "maxDeadline": 10000000,
    "minPages": 0,
    "maxPages": 1000,
    "threads": 1,
    "refreshAt": 10,
    "minCustomerRating": 0,
    "browser": "Chrome",
    "discard_orders_with_client_contacts": False,
    "exclude_displine": False,
    "dicard_assignments": True,
    "discard_editing_or_rewriting": True,
    "discard_offline_customers": True,
    "username": "kennedykoech983@gmail.com",
    "password": "Alexis@254",
}

BASE_PATH = os.path.dirname(sys.executable)
if 'DJANGO_DEVELOPMENT' in os.environ:
    BASE_PATH = './'


def get_path(filepath):
    return os.path.join(BASE_PATH, filepath)


class MyListener(AbstractEventListener):

    def __init__(self, config):
        self.config = config


class KaEssaySharkBot():
    def __init__(
        self,
        refresh_rate=100,
        min_pages=0,
        max_pages=1000,
        min_customer_rating=0,
        minDeadline=0,
        maxDeadline=10000000,
        discard_orders_with_client_contacts=False,
        exclude_displine=False,
        dicard_assignments=True,
        discard_editing_or_rewriting=True,
        discard_offline_customers=True,
        username="kennedykoech983@gmail.com",
        password="Alexis@254",
        thread_count=3,
        browser='chrome',
    ):
        super(KaEssaySharkBot, self).__init__()
        self.browser = browser.lower()
        self.refresh_rate = refresh_rate
        self.min_pages = min_pages
        self.max_pages = max_pages
        self.minDeadline = minDeadline
        self.maxDeadline = maxDeadline
        self.min_customer_rating = min_customer_rating
        self.discard_orders_with_client_contacts = discard_orders_with_client_contacts
        self.exclude_displine = exclude_displine
        self.dicard_assignments = dicard_assignments
        self.discard_editing_or_rewriting = discard_editing_or_rewriting,
        self.discard_offline_customers = discard_offline_customers,
        self.username = username
        self.password = password
        self.thread_count = thread_count  # number of threads

        self.drivers = OrderedDict()

    def get_driver(self, num):
        if self.browser.lower() == 'firefox':
            print("Please use chrome")
        else:
            botOptions = webdriver.ChromeOptions()
            botOptions.add_argument('headless')
            #botOptions.add_argument('window-size=1200x600')

            driver = webdriver.Chrome(options=botOptions)
            #driver = webdriver.Chrome(get_path('assets/chrome/chromedriver'), options=botOptions)

        driver.set_window_position(num * 150, num * 100)
        driver.set_window_size(1020, 690)

        edriver = EventFiringWebDriver(driver, MyListener(config=self.config_to_json()))
        return edriver

    def init_bot(self):
        for x in range(0, self.thread_count):
            driver = self.get_driver(x)
            self.drivers[x] = driver
            thread = threading.Thread(target=self.login, args=(driver, x), name="thread_{}".format(x), )
            #thread.daemon = True
            thread.start()
            time.sleep(5)

    def login(self, driver, x):
        try:
            driver.get("https://essayshark.com/writer/orders/")
            usernameEl = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "id_esauth_login_field"))
            )
            usernameEl.send_keys(self.username)
            passwordEl = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, "id_esauth_pwd_field"))
            )
            passwordEl.send_keys(self.password)
            driver.find_element_by_id("id_esauth_auth_form").submit()
            # print(f"Logging you in, thread {x}")
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@id='discard_all_visible']"))
            )
        finally:
            self.clean_orders(driver, x)

    def close(self, driver):
        driver.close()

    def search_orders(self, driver, x):
        # print(f"Searching for orders, thread {x}")
        try:
            driver.get("https://essayshark.com/writer/orders/")
            self.close_windows(driver)
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, "available_orders_list_container"))
            )
            wait_4_order(driver)
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//tr[contains(@id,'id_order_container_')]"
                ))
            )
            tr_element = driver.find_element_by_xpath("//tr[contains(@id,'id_order_container_')]")
            order_id = tr_element.get_attribute("data-id")
            link = "https://essayshark.com/writer/orders/{}.html".format(order_id)
            global orders
            if link not in orders:
                self.open_order(driver, link, x, order_id)
            else:
                try:
                    tr_element.find_element_by_xpath("//span[contains(@class, 'details_changed_order')]")
                    self.open_order(driver, link, x, order_id, is_edited=True)
                except NoSuchElementException:
                    WebDriverWait(driver, 30).until(
                        EC.new_window_is_opened(driver.window_handles)
                    )
        #     self.search_orders(driver)
        # except TimeoutException:
        #     self.search_orders(driver)
        # except Exception as e:
        #     raise e
        finally:
            self.search_orders(driver, x)

    def open_order(self, driver, order_link, x, order_id, is_edited=False, min_amount=-10):
        start = time.perf_counter()
        global orders
        orders.append(order_link)
        driver.get(order_link)
        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.ID, "id_bid"))
            )
            check_conditions(driver, self.config_to_json())
            process_bid(driver)
            dowload_files(driver)
            ping_timeout_and_submit_bid(driver)
            if len(driver.window_handles) > 1:
                parentGUID = driver.current_window_handle
                handles = list(driver.window_handles)
                handles.remove(parentGUID)
                for handle in handles:
                    driver.switch_to_window(handle)
                    if driver.current_url == order_link:
                        check_conditions(driver, self.config_to_json())
                        process_bid(driver)
                        dowload_files(driver)
                        ping_timeout_and_submit_bid(driver)
                driver.switch_to_window(parentGUID)
            if is_edited:
                time.sleep(5)
            else:
                timeout = WebDriverWait(driver, self.refresh_rate).until(
                    EC.visibility_of_element_located((By.ID, "id_read_timeout_sec"))
                )
                timeout = int(timeout.text)
                WebDriverWait(driver, 120).until(
                    EC.visibility_of_element_located((By.ID, "btn_cancel_this_order_3"))
                )
        finally:
            finish = time.perf_counter()
            # print(f"Finished bidding order {order_id} in {round(finish-start, 2)} seconds")
            self.search_orders(driver, x)

    def close_windows(self, driver):
        parentGUID = driver.current_window_handle
        all_clear = driver.find_element(By.XPATH, "//span[contains(@class, 'orders_list_info_filtered_qty')]").text == "0"
        if len(driver.window_handles) > 1 and all_clear:
            handles = list(driver.window_handles)
            handles.remove(parentGUID)
            for handle in handles:
                driver.switch_to_window(handle)
                driver.close()
        driver.switch_to_window(parentGUID)

    def quit(self):
        for driver in self.drivers.values():
            driver.quit()


    def clean_orders(self, driver, x):
        # print(f"Discarding orders, thread {x}")
        driver.get("https://essayshark.com/writer/orders/")
        try:
            discard_all = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@id='discard_all_visible']"))
            )
            driver.execute_script("arguments[0].click();", discard_all)
            discard_btn = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, "//a[@class='ZebraDialog_Button_1']"))
            )
            time.sleep(2)
            driver.execute_script("arguments[0].click();", discard_btn)
        # except Exception as e:
        #     raise e
        finally:
            self.search_orders(driver, x)

    def config_to_json(self):
        config = {
            "min_pages": self.min_pages,
            "max_pages": self.max_pages,
            "minDeadline": self.minDeadline,
            "maxDeadline": self.maxDeadline,
            "min_customer_rating": self.min_customer_rating,
            "discard_orders_with_client_contacts": self.discard_orders_with_client_contacts,
            "dicard_assignments": self.dicard_assignments,
            "discard_editing_or_rewriting": self.discard_editing_or_rewriting,
            "discard_offline_customers": self.discard_offline_customers,
        }
        return json.dumps(config)

if __name__ == '__main__':
    bot = KaEssaySharkBot()
    print("Starting the bot in a moment. You will not see any statement unless the bot fails")
    bot.init_bot()
