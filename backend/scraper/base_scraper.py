import requests
import zipfile
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from abc import ABC, abstractmethod

CHROME_FOR_TESTING_API = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"

class BaseScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.driver_path = self.get_chromedriver()
        self.service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=self.service)

    def get_chromedriver(self):
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

    def open_page(self):
        self.driver.get(self.url)

    @abstractmethod
    def scrape(self, filters):
        pass

    def close(self):
        self.driver.quit()
