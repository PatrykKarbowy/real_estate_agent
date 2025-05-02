from backend.scraper.base_scraper import BaseScraper


class GratkaScraper(BaseScraper):
    def __init__(self, city: str):
        super().__init__("https://www.gratka.pl/nieruchomosci/", city)

    def scrape(self):
        """Scrapes OLX listings for the specified city."""
        html = self.get_page_source()
        body_content = self.extract_body_content(html)
        cleaned_content = self.clean_body_content(body_content)

        return cleaned_content
