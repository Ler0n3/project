import allure
import pytest
from api.endpoints import VERIFY_LOGIN
from utils.data_generator import generate_user_data


@allure.feature("Login")
@allure.story("Проверка логина (verifyLogin)")
@pytest.mark.api
class TestVerifyLogin:
    """Тесты для эндпоинта verifyLogin."""

    @allure.title("Успешный логин с валидными данными")
    def test_verify_login_valid(self, api_client, created_user):
        """Позитивный тест: логин с корректными данными."""
        with allure.step("Отправить POST-запрос на /verifyLogin"):
            response = api_client.post(VERIFY_LOGIN, data={
                "email": created_user["email"],
                "password": created_user["password"]
            })

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode = 200"):
            data = response.json()
            assert data["responseCode"] == 200
            assert "User exists" in data["message"]

    @allure.title("Логин с неверным паролем")
    def test_verify_login_wrong_password(self, api_client, created_user):
        """Негативный тест: неверный пароль."""
        with allure.step("Отправить POST-запрос с неверным паролем"):
            response = api_client.post(VERIFY_LOGIN, data={
                "email": created_user["email"],
                "password": "wrong_password_12345"
            })

        with allure.step("Проверить responseCode = 404"):
            data = response.json()
            assert data["responseCode"] == 404
            assert "User not found" in data["message"]

    @allure.title("Логин с несуществующим email")
    def test_verify_login_wrong_email(self, api_client):
        """Негативный тест: несуществующий email."""
        with allure.step("Отправить POST-запрос с несуществующим email"):
            response = api_client.post(VERIFY_LOGIN, data={
                "email": "nonexistent_user_99999@example.com",
                "password": "some_password"
            })

        with allure.step("Проверить responseCode = 404"):
            data = response.json()
            assert data["responseCode"] == 404

    @allure.title("Логин без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_verify_login_missing_field(self, api_client, created_user, missing_field):
        """Негативный тест: пропущено обязательное поле."""
        credentials = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        del credentials[missing_field]

        with allure.step(f"Отправить POST-запрос без поля '{missing_field}'"):
            response = api_client.post(VERIFY_LOGIN, data=credentials)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400
            assert "Bad request" in data["message"]

    @allure.title("Логин с пустыми данными")
    def test_verify_login_empty_credentials(self, api_client):
        """Негативный тест: пустые email и password."""
        with allure.step("Отправить POST-запрос с пустыми данными"):
            response = api_client.post(VERIFY_LOGIN, data={
                "email": "",
                "password": ""
            })

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 404

    @allure.title("Логин с неверным HTTP-методом (GET)")
    def test_verify_login_wrong_method(self, api_client):
        """Негативный тест: GET вместо POST."""
        with allure.step("Отправить GET-запрос на /verifyLogin"):
            response = api_client.get(VERIFY_LOGIN)

        with allure.step("Проверить responseCode = 405 (Method Not Allowed)"):
            data = response.json()
            assert data["responseCode"] == 405
            assert "method is not supported" in data["message"].lower()