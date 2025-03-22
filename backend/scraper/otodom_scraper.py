from backend.scraper.base_scraper import BaseScraper


class OtodomScraper(BaseScraper):
    def __init__(self):
        super().__init__("https://www.otodom.pl")

    def scrape(self):
        self.open()
        # self.close()
