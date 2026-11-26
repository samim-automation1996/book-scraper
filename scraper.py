import requests, csv, time
from bs4 import BeautifulSoup

ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
rows = []

for page in range(1, 51):
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"
    res = requests.get(url)
    if res.status_code != 200:
        break
    soup = BeautifulSoup(res.text, "html.parser")
    for book in soup.select("article.product_pod"):
        name = book.h3.a["title"]
        price = book.select_one(".price_color").text
        rating = ratings[book.select_one(".star-rating")["class"][1]]
        rows.append([name, price, rating])
    print("পেজ", page, "শেষ")
    time.sleep(0.5)

with open("books.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Name", "Price", "Rating"])
    w.writerows(rows)

print(len(rows), "বই সেভ হয়েছে")
