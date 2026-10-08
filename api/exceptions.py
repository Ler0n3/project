class APIError(Exception):
    """Базовый класс для всех API-ошибок"""

    def __init__(self, status_code: int = None, message: str = None, response_text: str = None):
        self.status_code = status_code
        self.message = message
        self.response_text = response_text
        super().__init__(f"[{status_code}] {message}" if status_code else message)


class AuthenticationError(APIError):
    """Ошибка авторизации (401, 403)"""
    pass


class NotFoundError(APIError):
    """Ресурс не найден (404)"""
    pass


class ValidationError(APIError):
    """Ошибка валидации данных (400, 422)"""
    pass


class ServerError(APIError):
    """Ошибка сервера (500+)"""
    pass


class NetworkError(Exception):
    """Сетевые ошибки (timeout, connection, invalid URL)"""

    def __init__(self, message: str, original_exception: Exception = None, url: str = None):
        self.message = message
        self.original_exception = original_exception
        self.url = url
        super().__init__(message)