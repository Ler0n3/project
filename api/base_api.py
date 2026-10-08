"""
Базовый API-клиент.
Умеет выполнять GET, POST, PUT, DELETE запросы.
"""

import logging
import time
import requests
from api.exceptions import (
    APIError, AuthenticationError, NotFoundError,
    ValidationError, ServerError, NetworkError
)

logger = logging.getLogger(__name__)


class BaseAPI:
    """Базовый клиент для работы с API."""

    def __init__(self, base_url: str = None, timeout: int = 30, max_retries: int = 3):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

    def _request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Основной метод отправки запроса с retry."""
        if not url.startswith("http"):
            url = f"{self.base_url}{url}"

        logger.info(f"[{method}] {url}")
        if "params" in kwargs:
            logger.info(f"  Params: {kwargs['params']}")
        if "data" in kwargs:
            logger.info(f"  Data: {kwargs['data']}")

        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=self.timeout,
                    **kwargs
                )
                logger.info(f"  Response: {response.status_code}")
                return response
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                last_exception = e
                logger.warning(f"  Attempt {attempt}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries:
                    time.sleep(2)  # пауза перед повтором
            except requests.exceptions.RequestException as e:
                logger.error(f"  Request error: {url}")
                raise NetworkError(f"Request error: {url}", e, url)

        logger.error(f"  All {self.max_retries} attempts failed for: {url}")
        raise NetworkError(f"All retries failed: {url}", last_exception, url)

    def _check_status(self, response, expected_status: int = 200):
        """Проверяет HTTP-статус-код."""
        status = response.status_code
        if status == expected_status:
            return
        if status in (401, 403):
            raise AuthenticationError(status, response.reason, response.text)
        elif status == 404:
            raise NotFoundError(status, response.reason, response.text)
        elif status in (400, 422):
            raise ValidationError(status, response.reason, response.text)
        elif status >= 500:
            raise ServerError(status, response.reason, response.text)
        else:
            raise APIError(status, response.reason, response.text)

    def get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def close(self):
        self.session.close()