"""
Эндпоинты API Automation Exercise.
Документация: https://automationexercise.com/api_list
"""

BASE_URL = "https://automationexercise.com/api"

# ========== PRODUCTS ==========
PRODUCTS_LIST = f"{BASE_URL}/productsList"
BRANDS_LIST = f"{BASE_URL}/brandsList"
SEARCH_PRODUCT = f"{BASE_URL}/searchProduct"

# ========== USERS ==========
CREATE_ACCOUNT = f"{BASE_URL}/createAccount"
UPDATE_ACCOUNT = f"{BASE_URL}/updateAccount"
DELETE_ACCOUNT = f"{BASE_URL}/deleteAccount"
GET_USER_BY_EMAIL = f"{BASE_URL}/getUserDetailByEmail"

# ========== LOGIN ==========
VERIFY_LOGIN = f"{BASE_URL}/verifyLogin"