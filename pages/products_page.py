"""PageObject для страницы каталога товаров."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Страница каталога товаров."""

    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BTN = (By.ID, "submit_search")
    SEARCHED_TITLE = (By.XPATH, "//h2[contains(text(), 'Searched Products')]")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, ".product-image-wrapper")
    VIEW_PRODUCT_BTN = (By.XPATH, ".//a[contains(text(), 'View Product')]")

    def search_product(self, query: str):
        """Найти товар по названию."""
        self.dismiss_ad_popup()
        self.type_text(self.SEARCH_INPUT, query)
        self.dismiss_ad_popup()
        self.click(self.SEARCH_BTN)
        return self

    def is_search_results_visible(self) -> bool:
        """Проверить, что отображается заголовок 'Searched Products'."""
        try:
            self.wait.until(
                lambda d: "searched products" in d.page_source.lower()
            )
            return True
        except Exception:
            return False

    def click_first_product(self):
        """Открыть первый товар из списка."""
        self.dismiss_ad_popup()
        products = self.find_all(self.PRODUCT_ITEMS)
        view_btn = products[0].find_element(*self.VIEW_PRODUCT_BTN)
        view_btn.click()
        return self