import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

def fetch_futbin_prices(page=1):
    """
    Henter spillerpriser fra Futbin (FC26).
    page = hvilken side av spillere (1 = toppspillere).
    Returnerer DataFrame med navn, rating, pris og plattform.
    """
    url = f"https://www.futbin.com/players?page={page}&version=fc26"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    players = []
    for row in soup.select("tr.player_tr"):
        try:
            name = row.get("data-player-name")
            rating = row.get("data-rating")
            price = row.get("data-price")
            platform = row.get("data-pricelist")
            players.append([name, rating, price, platform])
        except:
            continue

    df = pd.DataFrame(players, columns=["Name", "Rating", "Price", "Platform"])
    df["ScrapedAt"] = datetime.now()
    return df


def save_prices(df, path="data/processed/prices.csv"):
    """Lagrer prisene til CSV i data/processed/."""
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} players to {path}")
