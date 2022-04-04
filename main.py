from fastapi import FastAPI
from scraper import Scraper
app = FastAPI()

quotes = Scraper()

# @app.get("/{cat}")
@app.get("/api/articles")

async def read_items():
  return quotes.scrapeMultiple()

@app.get("/api/article/{url}")

async def read_item(url):
  return quotes.scrapeSingle(url)