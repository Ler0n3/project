import allure
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.data_generator import generate_user_data


@allure.feature("UI: Login")
@pytest.mark.ui
class TestLogin:
    """Тесты для страницы логина."""

    @allure.title("Успешный логин с валидными данными")
    def test_login_valid(self, browser, ui_base_url):
        """Логин с корректными данными."""
        from api.base_api import BaseAPI
        from api.endpoints import BASE_URL, CREATE_ACCOUNT, DELETE_ACCOUNT

        user_data = generate_user_data()

        api = BaseAPI(base_url=BASE_URL)
        api.post(CREATE_ACCOUNT, data=user_data)

        with allure.step("Открыть страницу логина"):
            home = HomePage(browser, ui_base_url).open("/")
            home.header.go_to_login()

        with allure.step("Выполнить логин"):
            LoginPage(browser, ui_base_url).login(
                email=user_data["email"],
                password=user_data["password"]
            )

        with allure.step("Проверить, что пользователь залогинен"):
            assert home.header.is_logged_in()

        api.delete(DELETE_ACCOUNT, data={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        api.close()

    @allure.title("Негативный тест: логин с неверным паролем")
    def test_login_wrong_password(self, browser, ui_base_url):
        """Логин с неверным паролем."""
        with allure.step("Открыть страницу логина"):
            home = HomePage(browser, ui_base_url).open("/")
            home.header.go_to_login()

        with allure.step("Ввести неверные данные"):
            login = LoginPage(browser, ui_base_url)
            login.login(
                email="nonexistent_user@example.com",
                password="wrong_password"
            )

        with allure.step("Проверить, что отображается ошибка"):
            assert login.is_error_visible()

    @allure.title("Негативный тест: логин с несуществующим email")
    def test_login_wrong_email(self, browser, ui_base_url):
        """Логин с несуществующим email."""
        home = HomePage(browser, ui_base_url).open("/")
        home.header.go_to_login()

        login = LoginPage(browser, ui_base_url)
        login.login(
            email="nonexistent_email_12345@example.com",
            password="some_password"
        )

        assert login.is_error_visible()
        assert "incorrect" in login.get_error_text().lower()