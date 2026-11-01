import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()

    # Путь к Яндекс Браузеру
    options.binary_location = (
        r"C:\Program Files\Yandex\YandexBrowser\Application\browser.exe"
    )

    # Отдельный профиль с авторизацией Stepik
    options.add_argument(
        r"--user-data-dir=C:\Users\Julia\Documents\stepik_yandex_profile"
    )

    # Путь к YandexDriver
    service = Service(
        executable_path=r"C:\Users\Julia\Documents\project2\yandexdriver.exe"
    )

    browser = webdriver.Chrome(
        service=service,
        options=options
    )

    browser.maximize_window()

    yield browser

    browser.quit()