import allure
import pytest
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage


@allure.feature("UI: Cart")
@pytest.mark.ui
class TestCart:
    """Тесты для корзины."""

    @allure.title("Добавить товар в корзину")
    def test_add_product_to_cart(self, browser, ui_base_url):
        """Добавить первый товар в корзину и проверить."""
        with allure.step("Открыть страницу товаров"):
            products = ProductsPage(browser, ui_base_url).open("/products")

        with allure.step("Открыть первый товар"):
            products.click_first_product()

        with allure.step("Запомнить название товара"):
            detail = ProductDetailPage(browser, ui_base_url)
            product_name = detail.get_product_name()

        with allure.step("Добавить товар в корзину"):
            detail.add_to_cart()

        with allure.step("Проверить, что модалка 'Added!' появилась"):
            assert detail.is_added_modal_visible()

        with allure.step("Перейти в корзину"):
            detail.click_view_cart()

        with allure.step("Проверить, что товар в корзине"):
            cart = CartPage(browser, ui_base_url)
            assert cart.get_cart_items_count() > 0
            assert product_name.lower() in cart.get_first_product_name().lower()

    @allure.title("Удалить товар из корзины")
    def test_remove_product_from_cart(self, browser, ui_base_url):
        """Добавить и удалить товар из корзины."""
        with allure.step("Открыть страницу товаров"):
            products = ProductsPage(browser, ui_base_url).open("/products")

        with allure.step("Открыть первый товар"):
            products.click_first_product()

        with allure.step("Добавить товар в корзину"):
            detail = ProductDetailPage(browser, ui_base_url)
            detail.add_to_cart()
            detail.click_view_cart()

        with allure.step("Удалить товар"):
            cart = CartPage(browser, ui_base_url)
            cart.remove_first_product()

        with allure.step("Проверить, что корзина пуста"):
            assert cart.is_cart_empty()

    @allure.title("Перейти в корзину через шапку")
    def test_open_cart_from_header(self, browser, ui_base_url):
        """Проверить переход в корзину через меню."""
        with allure.step("Открыть главную страницу"):
            home = HomePage(browser, ui_base_url).open("/")

        with allure.step("Перейти в Cart"):
            home.header.go_to_cart()

        with allure.step("Проверить, что открылась страница корзины"):
            cart = CartPage(browser, ui_base_url)
            assert "cart" in cart.get_current_url().lower()