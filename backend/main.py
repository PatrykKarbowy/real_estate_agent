from fastapi import FastAPI, HTTPException

from backend.chat_request import ChatRequest
from backend.llm_processor import parse_query
from backend.scraper.olx_scraper import OLXScraper

app = FastAPI()


@app.get("/search")
def search(city: str):
    scraper = OLXScraper(city)
    scraper.open()
    listings = scraper.scrape()
    return {"city": city, "listings": listings}

@app.post("/chat")
def chat(chat_request: ChatRequest):
    user_query = f"{chat_request.query}\n\nHere are the listings:\n{chat_request.listings}"
    response = parse_query(user_query)

    if isinstance(response, dict) and "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    print("działa")
    return {"response": response}