import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_google_results_kg(keyword, country='kg'):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={keyword}&num=10&gl={country}&hl=ru"  # gl=kg — Кыргызстан
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())  # Для отладки, чтобы увидеть структуру HTML

    domains = []
    for result in soup.select("div.g"):
        link = result.find("a")["href"]
        if link.startswith("/url?q="):
            domain = link.split("/url?q=")[1].split("&")[0]
            domains.append(domain)
    return domains

# Пример: поиск в Кыргызстане
keyword = "кофемашина в Бишкеке"
country = "kg"  # kg — Кыргызстан для поиска в Кыргызстане
top_domains = get_google_results_kg(keyword, country)
print(f"Топ-10 доменов для '{keyword}':")
for domain in top_domains:
    print(domain)