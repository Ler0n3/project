"""Базовый класс для всех PageObject."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver, base_url: str = "https://automationexercise.com"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path: str = ""):
        """Открыть страницу."""
        self.driver.get(f"{self.base_url}{path}")
        return self

    def find(self, locator):
        """Найти элемент с ожиданием."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        """Найти все элементы."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def dismiss_ad_popup(self):
        """Закрыть попап согласия, если он есть."""
        try:
            consent_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
            )
            consent_btn.click()
            WebDriverWait(self.driver, 3).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fc-dialog-overlay"))
            )
        except Exception:
            pass

    def click(self, locator):
        """Кликнуть на элемент с защитой от попапа."""
        self.dismiss_ad_popup()
        element = self.wait.until(EC.element_to_be_clickable(locator))

        popups = self.driver.find_elements(By.CSS_SELECTOR, ".fc-dialog-overlay")
        if popups:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fc-dialog-overlay"))
            )

        element.click()
        return self

    def type_text(self, locator, text):
        """Ввести текст в поле."""
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator):
        """Получить текст элемента."""
        return self.find(locator).text

    def is_visible(self, locator) -> bool:
        """Проверить, виден ли элемент."""
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def get_current_url(self) -> str:
        """Получить текущий URL."""
        return self.driver.current_url