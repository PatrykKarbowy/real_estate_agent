from backend.scraper.base_scraper import BaseScraper


class GratkaScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://gratka.pl/nieruchomosci")

    def scrape(self):
        self.open()
        # self.close()
