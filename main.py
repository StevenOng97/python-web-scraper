from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import Scraper
app = FastAPI()

articles = Scraper()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/{cat}")
@app.get("/api/articles")

async def read_items():
  return articles.scrapeMultiple()

@app.get("/api/article/{url}")

async def read_item(url):
  return articles.scrapeSingle(url)