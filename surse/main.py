import requests
from bs4 import BeautifulSoup
from functii import scrap_movies, store_movies

movies = scrap_movies()

# Afișăm primele 20 ca preview:
print("\nPrimele 20 filme:")
for i, item in enumerate(movies[:20], start=1):
    print(f"{i}. {item['title']} ⭐{item['rating']} → {item['link']}")

store_movies(movies)
