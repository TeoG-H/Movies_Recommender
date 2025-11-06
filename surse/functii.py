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
            print(f" Fetching page {page+1}")

            response = requests.get(url=BASE_URL, headers=HEADERS, timeout=10) #cerere HTTP
            response.raise_for_status() #arunca eroare daca pagina nu se incarca
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
                
    print(f"\n Filme colectate: {len(all_items)}")
    return all_items

def store_movies(movies):
    output_file = "date/letterboxd_top_movies.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Rating", "Link"])
        for item in movies:
            writer.writerow([item["title"], item["rating"], item["link"]])
    
    print(f"\n Fișier salvat: {output_file}")



def cast():

    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://letterboxd.com/",
    "Accept-Language": "en-US,en;q=0.9"
    }

    url = "https://letterboxd.com/film/band-of-brothers/crew/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("❌ Nu pot încărca pagina:", e)
    return
    soup = BeautifulSoup(response.text, "html.parser")

    print("merge")
        
    # des = movie_page.select("div.truncate > p")
    #     #print(des[0].text)


    # c =movie_page.select("div.cast-list  p a")
    # cast=[a.get_text(strip=True) for a in c]
    # print("cast\n")
    # for i in cast:
    #      print(i)

        
    # crew= movie_page.select("#tab-crew div.text-sluglist ")
    # index=crew[:2]
    # directors=[a.get_text(strip=True) for a in index[0].select("p a")]
    # producers=[a.get_text(strip=True) for a in index[1].select("p a")]


    # print("director\n")
    # for i in directors:
    #      print(i)
    # print("producatori\n")
    # for i in producers:
    #     print(i)
   


    # genres= movie_page.select("#tab-genres div.text-sluglist ")
    # if(len(genres)>1):
    #     genuri=[a.get_text(strip=True) for a in genres[0].select("p a")]
    #     themes=[a.get_text(strip=True) for a in genres[1].select("p a")]
    # else:
    #     genuri=[a.get_text(strip=True) for a in genres[0].select("p a")]
    #     themes=[]


    # print("genuri")
    # for i in genuri:
    #     print(i)


    # print("teme")
    # for i in themes:
    #     print(i)

