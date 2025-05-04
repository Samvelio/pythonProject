# conftest.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                    choices=["chrome", "firefox", "yandex"])
    parser.addoption("--url", action="store", default="https://demo.opencart.com/")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")


def driver_factory(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),
                                 options=options)
    elif browser_name == "yandex":
        yandex_binary_path = None
        possible_paths = [
            "/usr/bin/yandex-browser",
            "/Applications/Yandex.app/Contents/MacOS/Yandex",
            "C:\\Users\\%USERNAME%\\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe"
        ]

        for path in possible_paths:
            if os.path.exists(os.path.expandvars(path)):
                yandex_binary_path = os.path.expandvars(path)
                break

        if not yandex_binary_path:
            raise pytest.UsageError("Yandex browser executable not found. Please install it or specify path manually")

        options = ChromeOptions()
        options.binary_location = yandex_binary_path
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                options=options)
    else:
        raise pytest.UsageError(f"Unsupported browser: {browser_name}")

    return driver


@pytest.fixture
def browser(request):
    driver = driver_factory(request)
    driver.maximize_window()
    driver.url = request.config.getoption("--url")

    yield driver

    driver.quit()


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
