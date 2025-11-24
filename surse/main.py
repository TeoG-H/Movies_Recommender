import requests
from bs4 import BeautifulSoup
from functii import scrap_movies, store_movies

print("Start movies scraper...\n")
movies = scrap_movies(1)

print(f"\n{'='*50}")
print(f"Total anime scraped: {len(movies)}")
print(f"{'='*50}\n")


if movies:
     store_movies(movies)
     print("Scraping complete!")
else:
     print("No movies data collected!")

   