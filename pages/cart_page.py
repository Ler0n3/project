"""PageObject для страницы корзины."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Страница корзины."""

    CART_ITEMS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".cart_description h4 a")
    DELETE_BTN = (By.CSS_SELECTOR, ".cart_quantity_delete")
    EMPTY_CART = (By.XPATH, "//b[contains(text(), 'Cart is empty')]")

    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине."""
        try:
            return len(self.find_all(self.CART_ITEMS))
        except Exception:
            return 0

    def is_cart_empty(self) -> bool:
        """Проверить, что корзина пуста."""
        return self.is_visible(self.EMPTY_CART)

    def get_first_product_name(self) -> str:
        """Получить название первого товара."""
        return self.get_text(self.PRODUCT_NAME)

    def remove_first_product(self):
        """Удалить первый товар из корзины."""
        self.click(self.DELETE_BTN)
        return self