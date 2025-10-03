import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

BASE = "https://www.futbin.com/26/players"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def _fetch_page(page: int) -> pd.DataFrame:
    url = f"{BASE}?page={page}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")  # lxml = raskere og mer robust

    rows = soup.select("tr.player_tr")
    items = []
    for tr in rows:
        try:
            name = tr.get("data-player-name")
            rating = tr.get("data-rating")
            price = (tr.get("data-price") or "0").replace(",", "").strip()
            platform = tr.get("data-pricelist")
            price_i = int(price) if price.isdigit() else None
            items.append({
                "Name": name,
                "Rating": pd.to_numeric(rating, errors="coerce"),
                "Price": price_i,
                "Platform": platform,
            })
        except Exception:
            continue

    return pd.DataFrame(items)

def fetch_futbin_prices(pages: int = 2, delay: float = 1.5) -> pd.DataFrame:
    """Hent live FUT-priser fra Futbin over flere sider."""
    dfs = []
    for p in range(1, pages + 1):
        dfs.append(_fetch_page(p))
        time.sleep(delay)  # vennlig rate-limit
    return pd.concat(dfs, ignore_index=True)

def save_prices(df: pd.DataFrame, path: str = "data/processed/prices.csv") -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
