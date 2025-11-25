import requests
import time
import random
from bs4 import BeautifulSoup
import csv
import os

def scrap_movies(pages=1):
    all_items = [] 
    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://letterboxd.com/films/by/rating/",
    }
    for page in range(pages):
            BASE_URL = f"https://letterboxd.com/films/ajax/by/rating/page/{page+1   }/?esiAllowFilters=true"
            print(f" Fetching page {page+1}")

            try:
                response = requests.get(url=BASE_URL, headers=HEADERS, timeout=10) 
                response.raise_for_status() 
            except Exception as e:
                print(f"Eroor on page {page+1}: {e}")

            else:
                soup = BeautifulSoup(response.text, "html.parser")
                i=0
                for div in soup.select("li.posteritem > div.react-component"):
                    link_tag = div.get("data-item-link")
                    link = "https://letterboxd.com" + link_tag if link_tag else None
                    rating_tag = div.parent.get("data-average-rating")
                    rating=float(rating_tag) if rating_tag else None
                    i=i+1
                    if link:
                        print(f"pagina {page+1}, filmul {i}")
                        movies_details = scrape_movies_details(link, rating)
                        if movies_details:
                            all_items.append(movies_details)
             
            if page < pages-1:
                time.sleep(random.uniform(1, 3))


    #print(all_items[0])
    return all_items



def scrape_movies_details(url, rating):
    #time.sleep(1)
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://letterboxd.com/",
    "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        movie_page = BeautifulSoup(response.text, "html.parser")


        title_tag=movie_page.select_one(".name.js-widont.prettify")
        title = title_tag.get_text(strip=True) if title_tag else ""

        des_tag = movie_page.select_one("div.truncate > p")
        description = des_tag.get_text(strip=True) if des_tag else ""

        cast_tags =movie_page.select("div.cast-list  p a") 
        cast=[a.get_text(strip=True) for a in cast_tags] if cast_tags else []
            
        crew = movie_page.select("#tab-crew div.text-sluglist ")

        if len(crew) >= 1:
            directors = [a.get_text(strip=True) for a in crew[0].select("p a")]
        else:
            directors = []

        if len(crew) >= 2:
            producers = [a.get_text(strip=True) for a in crew[1].select("p a")]
        else:
            producers = []


        genres = movie_page.select("#tab-genres div.text-sluglist ")

        if len(genres) >= 1:
            genuri = [a.get_text(strip=True) for a in genres[0].select("p a")]
        else:
            genuri = []

        if len(genres) >= 2:
            themes = [a.get_text(strip=True) for a in genres[1].select("p a")  if "show all" not in a.get_text(strip=True).lower()]
        else:
            themes = []

        movie_details= {
            "title": title,
            "rating": rating,
            "link": url,
            "description": description,
            "cast": cast,
            "directors": directors,
            "producers": producers,
            "genres": genuri,
            "themes": themes,
        }
        return movie_details
    

    except Exception as e:
            print(f"Eroor : {e}")
            return None

def store_movies(movies):
    output_file = "date/letterboxd_top_movies.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Rating", "Link", "Description", "Cast", "Directors","Producers", "Genres", "Themes"])
        for item in movies:
            writer.writerow([item["title"], item["rating"], item["link"], item["description"], item["cast"], item["directors"], item["producers"], item["genres"], item["themes"]])
    
    print(f"\n Fișier salvat: {output_file}")