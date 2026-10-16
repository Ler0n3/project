# OTUS Python QA Engineer — Проектная работа

Фреймворк для UI- и API-тестирования веб-приложения [Automation Exercise](https://automationexercise.com/).

## Что внутри

- **API-тесты** (28) — тестируют эндпоинты `automationexercise.com/api`
- **UI-тесты** (15) — тестируют веб-интерфейс через Selenium + PageObject
- **Demo-тест** (1) — намеренно падающий тест для демонстрации скриншотов в Allure
- **Allure-отчётность** — шаги, заголовки, вложения, скриншоты при падении
- **CI-пайплайн** — Jenkins с разделением запуска по маркерам

## Стек

| Инструмент | Назначение |
|-----------|-----------|
| Python 3.13 | Язык |
| pytest | Запуск тестов |
| Selenium + webdriver-manager | UI-автоматизация |
| requests | API-клиент |
| Faker | Генерация тестовых данных |
| Allure | Отчётность |
| flake8 | Линтер |
| Jenkins | CI |

## Структура проекта

```
project/
├── api/                      # API-клиент
│   ├── base_api.py           # Базовый клиент (get/post/put/delete)
│   ├── endpoints.py          # Эндпоинты
│   └── exceptions.py         # Кастомные исключения
├── pages/                    # PageObject для UI
│   ├── base_page.py
│   ├── header_page.py
│   ├── home_page.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── product_detail_page.py
│   └── cart_page.py
├── tests/
│   ├── api/                  # API-тесты (@pytest.mark.api)
│   │   ├── test_login.py
│   │   ├── test_products.py
│   │   └── test_users.py
│   ├── ui/                   # UI-тесты (@pytest.mark.ui)
│   │   ├── test_cart.py
│   │   ├── test_home_page.py
│   │   ├── test_login.py
│   │   └── test_products.py
│   └── ui_demo/              # Демо-тест (@pytest.mark.demo)
│       └── test_screenshot_demo.py
├── utils/
│   └── data_generator.py     # Генератор уникальных данных с Faker
├── docs/                     # Доказательства работы CI
│   ├── screenshots/          # Скриншоты Jenkins и Allure-отчётов
│   └── builds/               # Логи билдов
├── conftest.py               # Фикстуры и хуки
├── pytest.ini                # Конфигурация pytest
├── requirements.txt          # Зависимости
├── Jenkinsfile               # CI-пайплайн
└── README.md
```

## Разделение тестов по маркерам

| Маркер | Что запускает | Файлы |
|--------|---------------|-------|
| `api` | 28 API-тестов | `tests/api/` |
| `ui` | 15 UI-тестов | `tests/ui/` |
| `demo` | 1 демо-тест (падает специально) | `tests/ui_demo/` |

## ⚠️ Про Demo-тест

Файл `tests/ui_demo/test_screenshot_demo.py` содержит **намеренно падающий тест** (`assert False`). Он нужен для **демонстрации механизма прикрепления скриншотов** при падении в Allure-отчёте.

**Важно:**
- Демо-тест **не входит** в основной прогон (`TEST_SUITE=all`, `api`, `ui`)
- Запускается **только** при явном выборе `TEST_SUITE=demo` в Jenkins
- Падение теста — **ожидаемое поведение**, а не баг
- Цель: показать, что при падении в Allure прикрепляется скриншот

## Локальный запуск

### Установка

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### Запуск тестов

```bash
# Все реальные тесты (API + UI, без демо)
pytest tests/ -m "api or ui" -v

# Только API
pytest tests/ -m api -v

# Только UI
pytest tests/ -m ui -v

# Только демо (намеренно падает)
pytest tests/ -m demo -v
```

### Allure-отчёт локально

```bash
pytest tests/ -m "api or ui" --alluredir=allure-results
allure serve allure-results
```

## CI: Jenkins

### Что делает пайплайн

1. **Checkout** — скачивает код из GitHub
2. **Setup** — создаёт venv, ставит зависимости
3. **Lint** — прогоняет flake8 (не валит билд)
4. **Test** — запускает тесты по выбранному режиму
5. **Deploy** — условный шаг (только `main` + `ENVIRONMENT=prod`)

### Параметры билда

| Параметр | Значения | Описание |
|----------|----------|----------|
| `TEST_SUITE` | `all` / `api` / `ui` / `demo` | Какой набор тестов запускать |
| `ENVIRONMENT` | `dev` / `stage` / `prod` | Окружение (для условия деплоя) |

### Режимы запуска

| `TEST_SUITE` | Что запускается | Ожидаемый результат |
|-------------|-----------------|---------------------|
| `all` | 43 теста (28 API + 15 UI) | ✅ Зелёный билд |
| `api` | 28 API-тестов | ✅ Зелёный билд |
| `ui` | 15 UI-тестов | ✅ Зелёный билд |
| `demo` | 1 демо-тест | ❌ Красный билд (скриншот в Allure) |

### Автоматический запуск

- **По расписанию:** cron `H 2 * * *` — ночной регресс в 2:00 ежедневно
- **Вручную:** кнопка **Build with Parameters**

### Отчёты в Jenkins

После билда доступны:

- **Test Result** (JUnit) — статистика тестов, тренды
- **Allure Report** — детальный отчёт со шагами и скриншотами
- **Артефакты билда** — `flake8.log`, `results.xml`, `allure-results/`

Каждый билд очищает `allure-results/` перед запуском, поэтому отчёт содержит **только тесты текущего прогона**.

### Как запустить билд

1. Открыть Jenkins → job `project_otus`
2. **Build with Parameters**
3. Выбрать `TEST_SUITE` (например, `all`)
4. **Собрать**
5. После завершения — смотреть `Allure Report` в левом меню билда

## Доказательства работы CI

Все скриншоты и логи билдов лежат в папке `docs/`.

### Скриншоты (`docs/screenshots/`)

| Файл                                              | Что показывает |
|---------------------------------------------------|----------------|
| `01_dashboard.png`                                | Главная Jenkins со списком билдов и графиками |
| `02_allure_tools.png`                             | Настройка Allure Commandline в Manage Jenkins → Tools |
| `03_global_env.png`                               | Глобальные переменные окружения (Python, Java) |
| `04_job_config.png`                               | Конфигурация job: Pipeline script from SCM, Git, URL, credentials |
| `05_allure_all.png`                               | Allure-отчёт режима `all` — 43 passed |
| `06_allure_api.png`                               | Allure-отчёт режима `api` — 28 passed |
| `07_allure_ui.png`                                | Allure-отчёт режима `ui` — 15 passed |
| `08_01_allure_demo.png` и `08_02_allure_demo.png` | Allure-отчёт режима `demo` — 1 failed + прикреплённый скриншот |

### Логи билдов (`docs/builds/`)

| Файл | Режим | Результат |
|------|-------|-----------|
| `build_all.txt` | `all` | ✅ `43 passed`, SUCCESS |
| `build_api.txt` | `api` | ✅ `28 passed`, SUCCESS |
| `build_ui.txt` | `ui` | ✅ `15 passed`, SUCCESS |
| `build_demo_screenshot.txt` | `demo` | ❌ `1 failed`, FAILURE (намеренно) |

### Сводная таблица прогонов

| Режим | Тестов | Результат | Отчёт                                                               |
|-------|--------|-----------|---------------------------------------------------------------------|
| `all` | 43 | ✅ SUCCESS | [Allure](docs/screenshots/05_allure_all.png)                        |
| `api` | 28 | ✅ SUCCESS | [Allure](docs/screenshots/06_allure_api.png)                        |
| `ui` | 15 | ✅ SUCCESS | [Allure](docs/screenshots/07_allure_ui.png)                         |
| `demo` | 1 | ❌ FAILURE (намеренно) | [Allure + скриншот падения](docs/screenshots/08_02_allure_demo.png) |

## Особенности реализации

- **PageObject** — вся работа с UI через классы страниц
- **Уникальные данные** — Faker + UUID, чтобы тесты не конфликтовали
- **Обработка попапов куки** — `dismiss_ad_popup()` с ожиданием исчезновения overlay
- **Скриншот при падении** — реализован через хук `pytest_runtest_makereport`
- **Кастомные исключения API** — `APIError`, `NetworkError`, `NotFoundError`
- **Retry для API** — 3 попытки при сетевых ошибках

## Результаты

| Тип | Тестов | Статус |
|-----|--------|--------|
| API | 28 | ✅ |
| UI | 15 | ✅ |
| Demo | 1 | ❌ (намеренно) |
| **Итого** | **44** | **43 passed, 1 demo** |