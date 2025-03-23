from backend.scraper.base_scraper import BaseScraper


class OtodomScraper(BaseScraper):
    def __init__(self, city: str):
        super().__init__("https://gratka.pl/nieruchomosci")
        self.city = city

    def scrape(self):
        self.open(self.city)
        # self.close()
