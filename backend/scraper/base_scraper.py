import requests
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from abc import ABC, abstractmethod

CHROME_FOR_TESTING_API = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"


class BaseScraper(ABC):
    def __init__(self, url, city):
        self.url = f"{url}/{city.replace(' ', '-').lower()}"
        self.driver_path = self._get_chromedriver()
        self.service = Service(self.driver_path)
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.cookies": 2
        })
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def _get_chromedriver(self):
        response = requests.get(CHROME_FOR_TESTING_API).json()
        version_info = response["channels"]["Stable"]
        chromedriver_url = next(
            item["url"] for item in version_info["downloads"]["chromedriver"]
            if item["platform"] == "win64"
        )

        project_root = Path(__file__).resolve().parent.parent.parent
        driver_folder = project_root / "chromedriver"
        driver_folder.mkdir(exist_ok=True)
        driver_executable = driver_folder / "chromedriver-win64" / "chromedriver.exe"
        driver_zip_path = driver_folder / "chromedriver.zip"

        if not driver_executable.exists():
            print("Downloading latest ChromeDriver...")
            response = requests.get(chromedriver_url)
            with open(driver_zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(driver_zip_path, "r") as zip_ref:
                zip_ref.extractall(driver_folder)

            driver_zip_path.unlink()

        return str(driver_executable)

    def get_html(self):
        response = requests.get(self.url)
        print(response.text)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch page: {response.status_code}")
            return None

    def parse_html(self):
        html_content = self.get_html()
        if html_content:
            soup = BeautifulSoup(html_content, "lxml")  # Use "html.parser" if lxml is unavailable
            return soup
        return None

    def open(self):
        self.driver.get(self.url)

    @abstractmethod
    def scrape(self):
        pass

    def close(self):
        self.driver.quit()
