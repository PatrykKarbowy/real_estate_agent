from fastapi import FastAPI

from backend.scraper.olx_scraper import OLXScraper

app = FastAPI()

@app.get("/search")
def search():
    scraper = OLXScraper()
    scraper.open_page()
    return {"test": "test"}