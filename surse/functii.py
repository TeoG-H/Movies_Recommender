import requests
from bs4 import BeautifulSoup
import csv
import os

def scrap_movies(pages=10):
    all_items = []
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://letterboxd.com/films/by/rating/",
    }
    for page in range(pages):
            BASE_URL = f"https://letterboxd.com/films/ajax/by/rating/page/{page+1   }/?esiAllowFilters=true"
            print(f"📥 Fetching page {page+1}")

            response = requests.get(url=BASE_URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for div in soup.select("li.posteritem > div.react-component"):
                title = (div.get("data-item-full-display-name")
                        or div.get("data-item-name"))
                link = div.get("data-item-link")
                rating = div.parent.get("data-average-rating")

                if not title:
                    img = div.select_one("img.image")
                    title = img.get("alt") if img else ""
                
                if title:
                    all_items.append({
                        "title": title.strip(),
                        "rating": float(rating) if rating else None,
                        "link": "https://letterboxd.com" + link if link else None
                    })
                
    print(f"\n✅ Filme colectate: {len(all_items)}")
    return all_items

def store_movies(movies):
    output_file = "date/letterboxd_top_movies.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Rating", "Link"])
        for item in movies:
            writer.writerow([item["title"], item["rating"], item["link"]])
    
    print(f"\n✅ Fișier salvat: {output_file}")
