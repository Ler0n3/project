"""
Генератор тестовых данных на основе Faker.
"""
import time
from faker import Faker

fake = Faker()


def generate_email() -> str:
    """Уникальный email с timestamp — гарантирует уникальность между запусками."""
    timestamp = int(time.time() * 1000)
    random_str = fake.random_int(min=1000, max=9999)
    return f"test_{timestamp}_{random_str}@example.com"


def generate_user_data() -> dict:
    """Генерирует полный набор данных для регистрации."""
    return {
        "name": fake.first_name(),
        "email": generate_email(),  # ← используем гарантированно уникальный email
        "password": fake.password(length=12),
        "title": fake.random_element(elements=("Mr", "Mrs")),
        "birth_date": str(fake.random_int(min=1, max=28)),
        "birth_month": str(fake.random_int(min=1, max=12)),
        "birth_year": str(fake.random_int(min=1980, max=2000)),
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": "India",
        "zipcode": fake.postcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.phone_number(),
    }