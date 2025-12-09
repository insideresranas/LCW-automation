from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random

class LCW:
    ACCEPT_COOKIES = (By.CSS_SELECTOR, ".cookieseal-banner-button")
    WEB_PUSH = (By.CSS_SELECTOR, ".ins-web-opt-in-reminder-close-button")
    CATEGORY_PAGE = (By.CSS_SELECTOR, ".menu-header-item")
    SUBCATEGORY_ITEMS = (By.CSS_SELECTOR, ".menu-zone-item a")
    PRODUCT_PAGE = (By.CSS_SELECTOR, ".product-card--full")
    SELECT_SIZE = (By.CSS_SELECTOR, ".option-size-box__stripped")
    ADD_TO_CART = (By.CSS_SELECTOR, ".add-to-card")
    CART_PAGE = (By.CSS_SELECTOR, ".add-to-cart-preview__button")
    HOME_PAGE = (By.CSS_SELECTOR, ".main-header-logo")

    website = "https://www.lcw.com/"


    MAX_CATEGORY_COUNT = 12
    MAX_SUBCATEGORY_COUNT = 20

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.website)
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def test_navigate(self):

        #Cookies
        self.wait.until(EC.presence_of_all_elements_located(self.ACCEPT_COOKIES))[2].click()

        # Web push
        self.wait.until(EC.presence_of_all_elements_located(self.WEB_PUSH))[0].click()

        # Category & subcategory
        while True:
            categories = self.wait.until(
                EC.presence_of_all_elements_located(self.CATEGORY_PAGE)
            )

            # Only visible ones
            visible_categories = [
                cat for cat in categories
                if cat.is_displayed() and cat.size['width'] > 0
            ]

            max_index = min(len(visible_categories), self.MAX_CATEGORY_COUNT)
            selected_category = visible_categories[random.randrange(max_index)]

            # Hover
            self.actions.move_to_element(selected_category).perform()
            time.sleep(1)

            # Subcategory list
            subcategories = self.wait.until(
                EC.presence_of_all_elements_located(self.SUBCATEGORY_ITEMS)
            )

            visible_subcategories = [
                sub for sub in subcategories
                if sub.is_displayed() and sub.size['width'] > 0
            ]


            if len(visible_subcategories) == 0:
                continue

            break

        # Random subcategory
        max_sub = min(len(visible_subcategories), self.MAX_SUBCATEGORY_COUNT)
        selected_subcategory = visible_subcategories[random.randrange(max_sub)]
        selected_subcategory.click()

        # Product
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_PAGE))[2].click()

        # Product size
        self.wait.until(EC.presence_of_all_elements_located(self.SELECT_SIZE))[1].click()

        # ATC
        self.wait.until(EC.presence_of_all_elements_located(self.ADD_TO_CART))[0].click()
        time.sleep(10)

        self.wait.until(EC.presence_of_all_elements_located(self.CART_PAGE))[1].click()

        expected_cart_url = "https://www.lcw.com/sepetim"
        assert self.driver.current_url == expected_cart_url, "Sepet sayfası açılmadı!"

        # Home page
        self.wait.until(EC.element_to_be_clickable(self.HOME_PAGE)).click()

        assert "lcw" in self.driver.current_url, "Anasayfa açılmadı!"


LCW().test_navigate()
