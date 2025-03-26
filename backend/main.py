from fastapi import FastAPI

from backend.scraper.olx_scraper import OLXScraper

app = FastAPI()


@app.get("/search")
def search(city: str):
    scraper = OLXScraper(city)
    scraper.open()
    listings = scraper.scrape()
    return {"city": city, "listings": listings}

@app.get("/chat")
def test():
    pass
