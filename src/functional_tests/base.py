from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from unittest import skip
import os
import time
from datetime import datetime
from pathlib import Path

MAX_WAIT = 5

SCREEN_DUMP_LOCATION = Path(__file__).absolute().parent / "screendumps"

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        test_server = os.environ.get("TEST_SERVER")
        if test_server:
            self.live_server_url = "http://" + test_server

    def tearDown(self):
        if self._test_has_failed():
            if not SCREEN_DUMP_LOCATION.exists():
                SCREEN_DUMP_LOCATION.mkdir(parents=True)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _test_has_failed(self):
        # slightly obscure but couldn't find a better way!
        return self._outcome.result.failures or self._outcome.result.errors

    def take_screenshot(self):
            path = SCREEN_DUMP_LOCATION / self._get_filename("png")
            print("screenshotting to", path)
            self.browser.get_screenshot_as_file(str(path))

    def dump_html(self):
        path = SCREEN_DUMP_LOCATION / self._get_filename("html")
        print("dumping page HTML to", path)
        path.write_text(self.browser.page_source)

    def _get_filename(self, extension):
            timestamp = datetime.now().isoformat().replace(":", ".")[:19]
            return (
                f"{self.__class__.__name__}.{self._testMethodName}-{timestamp}.{extension}"
            )

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element(By.ID, "id_text")
