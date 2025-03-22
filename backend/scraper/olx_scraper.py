from backend.scraper.base_scraper import BaseScraper


class OLXScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.olx.pl/nieruchomosci/")

    def scrape(self):
        self.open()
        # self.close()
