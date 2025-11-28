from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

class LCW:
    ACCEPT_COOKIES = (By.CSS_SELECTOR, ".cookieseal-banner-button")
    WEB_PUSH = (By.CSS_SELECTOR, ".ins-web-opt-in-reminder-close-button")
    CATEGORY_PAGE = (By.CSS_SELECTOR, ".menu-header-item")  # [1]
    SUBCATEGORY_PAGE = (By.CSS_SELECTOR, 'a[href="/kadin-hirka-t-186"]')
    PRODUCT_PAGE=(By.CSS_SELECTOR, ".product-card--full")  # [2]
    SELECT_SIZE=(By.CSS_SELECTOR, ".option-size-box__stripped")  # [1]
    ADD_TO_CART=(By.CSS_SELECTOR, ".add-to-card")  # [0]
    CART_PAGE=(By.CSS_SELECTOR, ".add-to-cart-preview__button")  # [1]
    HOME_PAGE=(By.CSS_SELECTOR, ".main-header-logo")  # [0]
    website = "https://www.lcw.com/"

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.website)
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def test_navigate(self):

        # Cookies kapat
        self.wait.until(EC.presence_of_all_elements_located(self.ACCEPT_COOKIES))[2].click()

        # Web push kapat
        self.wait.until(EC.presence_of_all_elements_located(self.WEB_PUSH))[0].click()

        # Ana kategori hover
        categories = self.wait.until(EC.presence_of_all_elements_located(self.CATEGORY_PAGE))
        kadin = categories[1]
        self.actions.move_to_element(kadin).perform()

        # Alt kategori tıklama
        self.wait.until(EC.element_to_be_clickable(self.SUBCATEGORY_PAGE)).click()

        # ✅ assertIn: URL 'kadin' içeriyor mu?
        assert "kadin" in self.driver.current_url, "Alt kategori sayfası açılmadı!"

        # Ürün seç
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_PAGE))[2].click()

        # ✅ assertTrue: sayfa başlığı belirli kelimeyi içeriyor mu?
        assert "kadin" in self.driver.current_url, "Ürün sayfası açılmadı!"

        # Beden seç
        self.wait.until(EC.presence_of_all_elements_located(self.SELECT_SIZE))[1].click()

        # Sepete ekle
        self.wait.until(EC.presence_of_all_elements_located(self.ADD_TO_CART))[0].click()
        time.sleep(10)

        # Sepete git
        self.wait.until(EC.presence_of_all_elements_located(self.CART_PAGE))[1].click()

        # ✅ assertEqual: sepete yönlendirme doğru URL mi?
        expected_cart_url = "https://www.lcw.com/sepetim"
        assert self.driver.current_url == expected_cart_url, "Sepet sayfası açılmadı!"

        # Anasayfaya dön
        self.wait.until(EC.element_to_be_clickable(self.HOME_PAGE)).click()

        # ✅ assertIn: home sayfasında 'lcw' var mı?
        assert "lcw" in self.driver.current_url, "Anasayfa açılmadı!"

LCW().test_navigate()
