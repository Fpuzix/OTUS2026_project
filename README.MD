# Project for OTUS 2026 UI/API Autotests


Тестируемые сервисы:

- **UI**: [SauceDemo](https://www.saucedemo.com/)
- **API**: [httpbin](https://httpbin.org/)

Стек:

- Python
- Pytest
- Selenium
- Allure
- Jenkins

---

## Структура проекта

```text
.
├── api/
├── data/
├── pages/
├── tests/
│   ├── api/
│   └── ui/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── Jenkinsfile
```

Локальный запуск:

- pytest tests -v

- pytest tests/api -v

- pytest tests/ui -v --headless

- pytest tests -v --alluredir=allure-results