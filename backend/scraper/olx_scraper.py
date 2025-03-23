from backend.scraper.base_scraper import BaseScraper


class OLXScraper(BaseScraper):
    def __init__(self, city: str):
        super().__init__("https://www.olx.pl/nieruchomosci/")
        self.city = city

    def scrape(self):
        self.open(self.city)
        # self.close()
