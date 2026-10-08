import pytest
from api.base_api import BaseAPI
from api.endpoints import BASE_URL


def pytest_addoption(parser):
    """Добавляем параметры командной строки."""
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser for UI tests: chrome or firefox")
    parser.addoption("--ui-base-url", action="store", default="https://automationexercise.com",
                     help="Base URL for UI tests")
    parser.addoption("--api-base-url", action="store", default=BASE_URL,
                     help="Base URL for API tests")


def pytest_configure(config):
    """Регистрируем маркеры."""
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "smoke: Smoke tests")
    config.addinivalue_line("markers", "regression: Regression tests")


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def ui_base_url(request):
    return request.config.getoption("--ui-base-url")


@pytest.fixture(scope="session")
def api_base_url(request):
    return request.config.getoption("--api-base-url")


@pytest.fixture(scope="session")
def api_client(api_base_url):
    """Фикстура для API-клиента (сессия на весь прогон)."""
    client = BaseAPI(base_url=api_base_url)
    yield client
    client.close()

@pytest.fixture
def created_user(api_client):
    """Создаёт пользователя и удаляет его после теста."""
    from api.endpoints import CREATE_ACCOUNT, DELETE_ACCOUNT
    from utils.data_generator import generate_user_data
    import allure

    for attempt in range(3):
        user_data = generate_user_data()
        response = api_client.post(CREATE_ACCOUNT, data=user_data)
        data = response.json()

        if data["responseCode"] == 201:
            break
        elif "already exists" in data["message"].lower():
            continue
        else:
            raise AssertionError(f"Не удалось создать пользователя: {data}")

    else:
        raise AssertionError("Не удалось создать пользователя после 3 попыток")

    with allure.step(f"Создан пользователь: {user_data['email']}"):
        allure.attach(
            str(data),
            name="Ответ на создание",
            attachment_type=allure.attachment_type.TEXT
        )

    yield user_data

    with allure.step(f"Удалить пользователя: {user_data['email']}"):
        api_client.delete(DELETE_ACCOUNT, data={
            "email": user_data["email"],
            "password": user_data["password"]
        })