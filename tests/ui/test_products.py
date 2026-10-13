import allure
import pytest
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage


@allure.feature("UI: Products")
@pytest.mark.ui
class TestProducts:
    """Тесты для каталога товаров."""

    @allure.title("Открыть страницу товаров через меню")
    def test_open_products_page(self, browser, ui_base_url):
        """Проверить переход на страницу товаров."""
        with allure.step("Открыть главную страницу"):
            home = HomePage(browser, ui_base_url).open("/")

        with allure.step("Перейти в Products через меню"):
            home.header.go_to_products()

        with allure.step("Проверить, что открыта страница товаров"):
            products = ProductsPage(browser, ui_base_url)
            assert "products" in products.get_current_url().lower()


    @allure.title("Открыть карточку товара из каталога")
    def test_open_product_detail(self, browser, ui_base_url):
        """Открыть первый товар из каталога."""
        with allure.step("Открыть страницу товаров"):
            products = ProductsPage(browser, ui_base_url).open("/products")

        with allure.step("Открыть первый товар"):
            products.click_first_product()

        with allure.step("Проверить, что открылась карточка"):
            detail = ProductDetailPage(browser, ui_base_url)
            assert detail.get_product_name() != ""
            assert detail.get_product_price() != ""

    @allure.title("Параметризованный поиск разных товаров")
    @pytest.mark.parametrize("query", ["T-Shirt", "Jeans", "Dress", "Top"])
    def test_search_various_products(self, browser, ui_base_url, query):
        """Поиск разных товаров."""
        with allure.step(f"Открыть страницу товаров"):
            products = ProductsPage(browser, ui_base_url).open("/products")

        with allure.step(f"Найти '{query}'"):
            products.search_product(query)

        with allure.step("Проверить, что отображается результат"):
            assert products.is_search_results_visible()