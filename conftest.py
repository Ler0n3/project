import pytest
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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
    config.addinivalue_line("markers", "demo: Demonstration tests (намеренно падающие)")


@pytest.fixture(scope="session")
def browser_name(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def ui_base_url(request):
    return request.config.getoption("--ui-base-url")


@pytest.fixture
def browser(request, browser_name):
    """Фикстура создаёт WebDriver."""
    if browser_name == "chrome":
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        options.add_experimental_option("prefs", prefs)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")

    driver.implicitly_wait(5)

    request.node.driver = driver

    yield driver

    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для получения статуса теста.
    Делает скриншот, если тест упал.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        driver = getattr(item, "driver", None)
        if driver is not None:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{datetime.now().strftime('%H%M%S')}",
                attachment_type=allure.attachment_type.PNG
            )


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