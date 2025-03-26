from backend.scraper.base_scraper import BaseScraper


class OLXScraper(BaseScraper):
    def __init__(self, city: str):
        super().__init__("https://www.olx.pl/nieruchomosci/", city)

    def scrape(self):
        soup = self.parse_html()
        if not soup:
            return []

        listings = []
        for item in soup.find_all("div", class_="offer-wrapper"):
            title_tag = item.find("a", class_="marginright5 link linkWithHash detailsLink")
            price_tag = item.find("p", class_="price")
            url = title_tag["href"] if title_tag else None
            title = title_tag.text.strip() if title_tag else "No title"
            price = price_tag.text.strip() if price_tag else "No price"

            listings.append({"title": title, "price": price, "url": url})

        return listings
