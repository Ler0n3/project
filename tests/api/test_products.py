import allure
import pytest
from api.endpoints import PRODUCTS_LIST, BRANDS_LIST, SEARCH_PRODUCT
from api.exceptions import NotFoundError, ValidationError

@allure.feature("Products")
@allure.story("Работа с продуктами и брендами")
@pytest.mark.api
class TestProducts:

    @allure.title("Проверка получения списка всех продуктов")
    def test_get_products_list(self, api_client):
        """Полная проверка получения списка продуктов."""
        with allure.step("Отправить GET-запрос на /productsList"):
            response = api_client.get(PRODUCTS_LIST)

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode в теле"):
            data = response.json()
            assert data["responseCode"] == 200

        with allure.step("Проверить структуру ответа"):
            assert "products" in data
            assert isinstance(data["products"], list)
            assert len(data["products"]) > 0

    @allure.title("Проверка получения списка брендов")
    def test_get_brands_list(self, api_client):
        """Проверка получения списка брендов."""
        with allure.step("Отправить GET-запрос на /brandsList"):
            response = api_client.get(BRANDS_LIST)

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode в теле"):
            data = response.json()
            assert data["responseCode"] == 200

        with allure.step("Проверить структуру ответа"):
            assert "brands" in data
            assert isinstance(data["brands"], list)
            assert len(data["brands"]) > 0

    @allure.title("Поиск продукта по валидному параметру")
    def test_search_product_valid(self, api_client):
        """Поиск продукта по валидному параметру."""
        search_query = "top"

        with allure.step(f"Отправить POST-запрос на /searchProduct с параметром '{search_query}'"):
            response = api_client.post(SEARCH_PRODUCT, data={"search_product": search_query})

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode в теле"):
            data = response.json()
            assert data["responseCode"] == 200

        with allure.step("Проверить, что найдены продукты"):
            assert "products" in data
            assert isinstance(data["products"], list)
            assert len(data["products"]) > 0

    @allure.title("Негативный тест: поиск без параметра")
    def test_search_product_without_param(self, api_client):
        """Негативный тест: поиск без параметра."""
        with allure.step("Отправить POST-запрос на /searchProduct без параметров"):
            response = api_client.post(SEARCH_PRODUCT)

        with allure.step("Проверить HTTP-статус 200"):
            assert response.status_code == 200

        with allure.step("Проверить responseCode = 400"):
            data = response.json()
            assert data["responseCode"] == 400

        with allure.step("Проверить сообщение об ошибке"):
            assert "Bad request" in data["message"]

    @allure.feature("Network errors")
    @allure.story("Обработка сетевых ошибок")
    @pytest.mark.api
    class TestNetworkErrors:

        @allure.title("Негативный тест: несуществующий эндпоинт")
        def test_nonexistent_endpoint(self, api_client):
            """Проверяем, что несуществующий эндпоинт возвращает 404."""
            with allure.step("Отправить GET-запрос на /nonexistent-endpoint"):
                response = api_client.get("/nonexistent-endpoint")

            with allure.step("Проверить, что статус 404"):
                with pytest.raises(NotFoundError):
                    api_client._check_status(response, expected_status=200)