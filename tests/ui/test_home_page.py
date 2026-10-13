import allure
import pytest
from pages.home_page import HomePage


@allure.feature("UI: Home Page")
@pytest.mark.ui
class TestHomePage:
    """Тесты для главной страницы."""

    @allure.title("Проверка загрузки главной страницы")
    def test_home_page_loads(self, browser, ui_base_url):
        """Проверить, что главная страница загружается."""
        home = HomePage(browser, ui_base_url)

        with allure.step("Открыть главную страницу"):
            home.open("/")

        with allure.step("Проверить заголовок"):
            assert "Automation Exercise" in home.get_title()

        with allure.step("Проверить, что слайдер виден"):
            assert home.is_slider_visible()

    @allure.title("Проверка блока features на главной")
    def test_home_page_features(self, browser, ui_base_url):
        """Проверить, что блок features виден."""
        home = HomePage(browser, ui_base_url).open("/")

        with allure.step("Проверить блок features"):
            assert home.is_features_visible()

    @allure.title("Проверка подписки на рассылку")
    def test_newsletter_subscription(self, browser, ui_base_url):
        """Проверить подписку на новостную рассылку."""
        home = HomePage(browser, ui_base_url).open("/")

        with allure.step("Подписаться на рассылку"):
            home.subscribe_to_newsletter("test_subscriber@example.com")

        with allure.step("Проверить успех"):
            assert home.is_subscription_success()