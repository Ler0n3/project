"""PageObject для страницы карточки товара."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """Страница карточки товара."""

    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".product-information span span")
    ADD_TO_CART_BTN = (By.XPATH, "//button[contains(., 'Add to cart')]")
    ADDED_MODAL = (By.XPATH, "//h4[contains(text(), 'Added!')]")
    VIEW_CART_BTN = (By.XPATH, "//u[contains(text(), 'View Cart')]")

    def get_product_name(self) -> str:
        """Получить название товара."""
        return self.get_text(self.PRODUCT_NAME)

    def get_product_price(self) -> str:
        """Получить цену товара."""
        return self.get_text(self.PRODUCT_PRICE)

    def add_to_cart(self):
        """Добавить товар в корзину."""
        self.click(self.ADD_TO_CART_BTN)
        return self

    def is_added_modal_visible(self) -> bool:
        """Проверить, что модалка 'Added!' появилась."""
        return self.is_visible(self.ADDED_MODAL)

    def click_view_cart(self):
        """Перейти в корзину из модалки."""
        self.click(self.VIEW_CART_BTN)
        return self