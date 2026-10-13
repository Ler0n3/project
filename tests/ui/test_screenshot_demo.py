import allure
import pytest
from pages.home_page import HomePage


@allure.feature("UI: Screenshot Demo")
@pytest.mark.ui
class TestScreenshotDemo:
    """Демонстрация скриншота при падении."""

    @allure.title("Демонстрация скриншота при падении")
    def test_screenshot_on_failure(self, browser, ui_base_url):
        """Намеренно падает, чтобы показать скриншот в Allure."""
        with allure.step("Открыть главную страницу"):
            home = HomePage(browser, ui_base_url).open("/")

        with allure.step("Намеренно падающий assert"):
            assert False, "Тест упал специально для демонстрации скриншота"