"""PageObject для шапки сайта."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HeaderPage(BasePage):
    """Шапка сайта — общая для всех страниц."""

    SIGNUP_LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Signup / Login')]")
    CART_LINK = (By.XPATH, "//a[contains(text(), 'Cart')]")
    PRODUCTS_LINK = (By.XPATH, "//a[contains(text(), 'Products')]")
    LOGGED_IN_AS = (By.XPATH, "//*[contains(., 'Logged in as')]")

    def go_to_login(self):
        """Перейти на страницу логина."""
        self.click(self.SIGNUP_LOGIN_LINK)
        return self

    def go_to_cart(self):
        """Перейти в корзину."""
        self.click(self.CART_LINK)
        return self

    def go_to_products(self):
        """Перейти в каталог товаров."""
        self.click(self.PRODUCTS_LINK)
        return self

    def is_logged_in(self) -> bool:
        """Проверить, что пользователь залогинен."""
        return self.is_visible(self.LOGGED_IN_AS)