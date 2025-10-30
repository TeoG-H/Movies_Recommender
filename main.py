import requests
from bs4 import BeautifulSoup

BASE_URL = "https://letterboxd.com/films/ajax/by/rating/?esiAllowFilters=true&page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://letterboxd.com/films/by/rating/",
}

all_items = []
PAGE_LIMIT = 14  # suficiente pentru 1000 de filme
TARGET_COUNT = 1000

for page in range(1, PAGE_LIMIT + 1):
    url = BASE_URL.format(page)
    print(f"📥 Fetching page {page} - {url}")
    
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    for div in soup.select("li.posteritem > div.react-component"):
        title = (div.get("data-item-full-display-name")
                 or div.get("data-item-name"))
        link = div.get("data-item-link")  # link la film
        rating = div.parent.get("data-average-rating")  # din <li posteritem>
        
        if not title:
            img = div.select_one("img.image")
            title = img.get("alt") if img else ""
        
        if title:
            all_items.append({
                "title": title.strip(),
                "rating": float(rating) if rating else None,
                "link": "https://letterboxd.com" + link if link else None
            })
        
        if len(all_items) >= TARGET_COUNT:
            break

    if len(all_items) >= TARGET_COUNT:
        break

print(f"\n✅ Filme colectate: {len(all_items)}")

# Afișăm primele 20 ca preview:
print("\nPrimele 20 filme:")
for i, item in enumerate(all_items[:20], start=1):
    print(f"{i}. {item['title']} ⭐{item['rating']} → {item['link']}")
import csv

output_file = "top1000_letterboxd.csv"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Rating", "Link"])
    for item in all_items:
        writer.writerow([item["title"], item["rating"], item["link"]])

print(f"\n✅ Fișier salvat: {output_file}")
