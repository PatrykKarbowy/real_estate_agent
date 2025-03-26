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
            "profile.default_content_setting_values.cookies": 2  # Block cookies
        })
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

    def _get_chromedriver(self):
        """Download and configure ChromeDriver automatically."""
        response = requests.get(CHROME_FOR_TESTING_API).json()
        version_info = response["channels"]["Stable"]
        chromedriver_url = next(
            item["url"] for item in version_info["downloads"]["chromedriver"]
            if item["platform"] == "win64"
        )

        project_root = Path(__file__).resolve().parent.parent.parent
        driver_folder = project_root / "chromedriver"
        driver_folder.mkdir(exist_ok=True)
        driver_executable = driver_folder / "chromedriver.exe"
        driver_zip_path = driver_folder / "chromedriver.zip"

        if not driver_executable.exists():
            print("Downloading latest ChromeDriver...")
            response = requests.get(chromedriver_url)
            with open(driver_zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(driver_zip_path, "r") as zip_ref:
                zip_ref.extractall(driver_folder)

            extracted_files = list(driver_folder.glob("**/chromedriver.exe"))
            if extracted_files:
                extracted_files[0].rename(driver_executable)

            driver_zip_path.unlink()

        return str(driver_executable)

    def open(self):
        """Open the webpage in the browser."""
        self.driver.get(self.url)

    def get_page_source(self):
        """Return the page's HTML source."""
        return self.driver.page_source

    def extract_body_content(self, html_content):
        """Extract the main body content from the HTML."""
        soup = BeautifulSoup(html_content, "html.parser")
        return str(soup.body) if soup.body else ""

    def clean_body_content(self, body_content):
        """Remove scripts/styles and return clean text."""
        soup = BeautifulSoup(body_content, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        cleaned_content = soup.get_text(separator="\n")
        return "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    def split_dom_content(self, dom_content, max_length=6000):
        """Split long content into smaller chunks."""
        return [
            dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
        ]

    @abstractmethod
    def scrape(self):
        """Abstract method for scrapers to implement."""
        pass

    def close(self):
        """Close the browser."""
        self.driver.quit()
