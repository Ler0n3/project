"""PageObject для страницы логина."""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница логина."""

    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH, "//p[contains(text(), 'Your email or password is incorrect')]")

    def login(self, email: str, password: str):
        """Выполнить логин."""
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BTN)
        return self

    def is_error_visible(self) -> bool:
        """Проверить, что отображается ошибка логина."""
        return self.is_visible(self.LOGIN_ERROR)

    def get_error_text(self) -> str:
        """Получить текст ошибки."""
        return self.get_text(self.LOGIN_ERROR)