"""PageObject для главной страницы."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.header_page import HeaderPage


class HomePage(BasePage):
    """Главная страница Automation Exercise."""

    SLIDER = (By.CSS_SELECTOR, "#slider-carousel")
    FEATURES_ITEMS = (By.CSS_SELECTOR, ".features_items")
    SUBSCRIPTION_EMAIL = (By.ID, "susbscribe_email")
    SUBSCRIPTION_BTN = (By.ID, "subscribe")
    SUBSCRIPTION_SUCCESS = (By.CSS_SELECTOR, ".alert-success")

    def __init__(self, driver, base_url=None):
        super().__init__(driver, base_url)
        self.header = HeaderPage(driver, base_url)

    def is_slider_visible(self) -> bool:
        """Проверить, что слайдер виден."""
        return self.is_visible(self.SLIDER)

    def is_features_visible(self) -> bool:
        """Проверить, что блок features виден."""
        return self.is_visible(self.FEATURES_ITEMS)

    def subscribe_to_newsletter(self, email: str):
        """Подписаться на рассылку."""
        self.dismiss_ad_popup()
        self.type_text(self.SUBSCRIPTION_EMAIL, email)
        self.dismiss_ad_popup()
        self.click(self.SUBSCRIPTION_BTN)
        return self

    def is_subscription_success(self) -> bool:
        """Проверить успешную подписку."""
        return self.is_visible(self.SUBSCRIPTION_SUCCESS)

    def get_title(self) -> str:
        """Получить заголовок страницы."""
        return self.driver.title