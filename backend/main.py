from fastapi import FastAPI

from backend.scraper.olx_scraper import OLXScraper

app = FastAPI()


@app.get("/search")
def search(city: str):
    scraper = OLXScraper(city)
    scraper.scrape();
    return {"test": "test"}
