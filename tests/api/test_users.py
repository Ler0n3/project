import allure
import pytest
from api.endpoints import (
    CREATE_ACCOUNT,
    UPDATE_ACCOUNT,
    DELETE_ACCOUNT,
    GET_USER_BY_EMAIL,
)
from api.exceptions import APIError, NotFoundError, ValidationError
from utils.data_generator import generate_user_data


@allure.feature("Users")
@allure.story("Создание аккаунта")
@pytest.mark.api
class TestCreateAccount:
    """Тесты на создание нового аккаунта."""

    @allure.title("Создание аккаунта с валидными данными")
    def test_create_account_valid(self, api_client):
        """Позитивный тест: создание нового пользователя."""
        user_data = generate_user_data()

        with allure.step(f"Отправить POST-запрос на /createAccount"):
            response = api_client.post(CREATE_ACCOUNT, data=user_data)

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode = 201"):
            data = response.json()
            assert data["responseCode"] == 201
            assert "User created" in data["message"]

        with allure.step("Проверить, что пользователь создан (getUserDetailByEmail)"):
            response = api_client.get(
                GET_USER_BY_EMAIL,
                params={"email": user_data["email"]}
            )
            user_info = response.json()
            assert user_info["responseCode"] == 200
            assert user_info["user"]["email"] == user_data["email"]

        with allure.step("Удалить созданного пользователя"):
            api_client.delete(DELETE_ACCOUNT, data={
                "email": user_data["email"],
                "password": user_data["password"]
            })

    @allure.title("Создание аккаунта без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_account_missing_field(self, api_client, missing_field):
        """Негативный тест: пропущено обязательное поле."""
        user_data = generate_user_data()
        del user_data[missing_field]

        with allure.step(f"Отправить POST-запрос без поля '{missing_field}'"):
            response = api_client.post(CREATE_ACCOUNT, data=user_data)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400
            assert "Bad request" in data["message"]

    @allure.title("Создание аккаунта с уже существующим email")
    def test_create_account_duplicate_email(self, api_client, created_user):
        """Негативный тест: попытка создать пользователя с занятым email."""
        duplicate_data = generate_user_data()
        duplicate_data["email"] = created_user["email"]

        with allure.step("Отправить POST-запрос с email уже существующего пользователя"):
            response = api_client.post(CREATE_ACCOUNT, data=duplicate_data)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400
            assert "already exists" in data["message"].lower()

@allure.feature("Users")
@allure.story("Обновление аккаунта")
@pytest.mark.api
class TestUpdateAccount:
    """Тесты на обновление данных аккаунта."""

    @allure.title("Обновление аккаунта с валидными данными")
    def test_update_account_valid(self, api_client, created_user):
        """Позитивный тест: обновление данных существующего пользователя."""
        updated_data = created_user.copy()
        updated_data["name"] = "UpdatedName"
        updated_data["firstname"] = "UpdatedFirst"
        updated_data["lastname"] = "UpdatedLast"

        with allure.step("Отправить PUT-запрос на /updateAccount"):
            response = api_client.put(UPDATE_ACCOUNT, data=updated_data)

        with allure.step("Проверить responseCode = 200"):
            data = response.json()
            assert data["responseCode"] == 200
            assert "User updated" in data["message"]

        with allure.step("Проверить, что данные обновились (getUserDetailByEmail)"):
            response = api_client.get(
                GET_USER_BY_EMAIL,
                params={"email": updated_data["email"]}
            )
            user_info = response.json()
            assert user_info["user"]["first_name"] == "UpdatedFirst"
            assert user_info["user"]["last_name"] == "UpdatedLast"

    @allure.title("Обновление аккаунта без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_update_account_missing_field(self, api_client, created_user, missing_field):
        """Негативный тест: пропущено обязательное поле при обновлении."""
        updated_data = created_user.copy()
        del updated_data[missing_field]

        with allure.step(f"Отправить PUT-запрос без поля '{missing_field}'"):
            response = api_client.put(UPDATE_ACCOUNT, data=updated_data)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400

    @allure.title("Обновление несуществующего аккаунта")
    def test_update_account_nonexistent(self, api_client):
        """Негативный тест: обновление пользователя, которого нет."""
        user_data = generate_user_data()

        with allure.step("Отправить PUT-запрос с данными несуществующего пользователя"):
            response = api_client.put(UPDATE_ACCOUNT, data=user_data)

        with allure.step("Проверить responseCode = 404"):
            data = response.json()
            assert data["responseCode"] == 404

@allure.feature("Users")
@allure.story("Удаление аккаунта")
@pytest.mark.api
class TestDeleteAccount:
    """Тесты на удаление аккаунта."""

    @allure.title("Удаление существующего аккаунта")
    def test_delete_account_valid(self, api_client):
        """Позитивный тест: удаление пользователя."""
        user_data = generate_user_data()

        with allure.step("Создать пользователя для удаления"):
            api_client.post(CREATE_ACCOUNT, data=user_data)

        with allure.step("Отправить DELETE-запрос на /deleteAccount"):
            response = api_client.delete(DELETE_ACCOUNT, data={
                "email": user_data["email"],
                "password": user_data["password"]
            })

        with allure.step("Проверить responseCode = 200"):
            data = response.json()
            assert data["responseCode"] == 200
            assert "Account deleted" in data["message"]

        with allure.step("Проверить, что пользователя больше нет"):
            response = api_client.get(
                GET_USER_BY_EMAIL,
                params={"email": user_data["email"]}
            )
            user_info = response.json()
            assert user_info["responseCode"] == 404

    @allure.title("Удаление аккаунта без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_delete_account_missing_field(self, api_client, missing_field):
        """Негативный тест: пропущено обязательное поле."""
        user_data = generate_user_data()
        del user_data[missing_field]

        with allure.step(f"Отправить DELETE-запрос без поля '{missing_field}'"):
            response = api_client.delete(DELETE_ACCOUNT, data=user_data)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400

    @allure.title("Удаление несуществующего аккаунта")
    def test_delete_account_nonexistent(self, api_client):
        """Негативный тест: удаление несуществующего пользователя."""
        user_data = generate_user_data()

        with allure.step("Отправить DELETE-запрос с несуществующими данными"):
            response = api_client.delete(DELETE_ACCOUNT, data={
                "email": user_data["email"],
                "password": user_data["password"]
            })

        with allure.step("Проверить responseCode = 404"):
            data = response.json()
            assert data["responseCode"] == 404

@allure.feature("Users")
@allure.story("Получение данных пользователя")
@pytest.mark.api
class TestGetUserByEmail:
    """Тесты на получение данных пользователя по email."""

    @allure.title("Получение данных существующего пользователя")
    def test_get_user_by_email_valid(self, api_client, created_user):
        """Позитивный тест: получение данных по email."""
        with allure.step(f"Отправить GET-запрос с email: {created_user['email']}"):
            response = api_client.get(
                GET_USER_BY_EMAIL,
                params={"email": created_user["email"]}
            )

        with allure.step("Проверить responseCode = 200"):
            data = response.json()
            assert data["responseCode"] == 200

        with allure.step("Проверить, что данные пользователя совпадают"):
            user = data["user"]
            assert user["email"] == created_user["email"]
            assert user["name"] == created_user["name"]

    @allure.title("Получение данных без параметра email")
    def test_get_user_by_email_missing_param(self, api_client):
        """Негативный тест: запрос без параметра email."""
        with allure.step("Отправить GET-запрос без параметра email"):
            response = api_client.get(GET_USER_BY_EMAIL)

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400
            assert "email" in data["message"].lower()

    @allure.title("Получение данных несуществующего пользователя")
    def test_get_user_by_email_nonexistent(self, api_client):
        """Негативный тест: пользователя с таким email нет."""
        fake_email = "nonexistent_user_12345@example.com"

        with allure.step(f"Отправить GET-запрос с email: {fake_email}"):
            response = api_client.get(
                GET_USER_BY_EMAIL,
                params={"email": fake_email}
            )

        with allure.step("Проверить responseCode = 404"):
            data = response.json()
            assert data["responseCode"] == 404