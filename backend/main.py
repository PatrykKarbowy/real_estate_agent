from fastapi import FastAPI, Query

from backend.chat_request import ChatRequest
from backend.llm_processor import parse_query
from backend.scraper.gratka_scraper import GratkaScraper
from backend.scraper.olx_scraper import OLXScraper
from backend.scraper.otodom_scraper import OtodomScraper

app = FastAPI()

SCRAPER_MAP = {
    "olx": OLXScraper,
    "gratka": GratkaScraper,
    "otodom": OtodomScraper,
}

@app.get("/search")
def search(city: str, source: str = Query("olx", enum=SCRAPER_MAP.keys())):
    ScraperClass = SCRAPER_MAP[source]
    scraper = ScraperClass(city)
    scraper.open()
    listings = scraper.scrape()
    return {"city": city, "source": source, "listings": listings}

@app.post("/chat")
def chat(chat_request: ChatRequest):
    user_query = f"{chat_request.query}\n\nHere are the listings:\n{chat_request.listings}"
    response = parse_query(user_query)
    return {"response": response}