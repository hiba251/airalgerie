import os
import json
from datetime import datetime, timezone

import pandas as pd

from scraper import AirAlgerieOffersScraper, ScrapeConfig
from parser import parse_offer


URL = "https://airalgerie.dz/en/discover/our-special-offers/"

HEADLESS = True
MAX_ITEMS = 200
DELAY = 2.0

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

# Nom unique pour éviter PermissionError si Excel a ouvert l'ancien fichier
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
OUT_CSV = os.path.join(OUT_DIR, f"offers_{RUN_ID}.csv")
OUT_SUMMARY = os.path.join(OUT_DIR, f"summary_{RUN_ID}.json")
OUT_BEST = os.path.join(OUT_DIR, f"best_offer_{RUN_ID}.json")
OUT_RAW = os.path.join(OUT_DIR, f"raw_texts_{RUN_ID}.txt")

# Taux fixes : 1 unité = X EUR (à ajuster si tu veux)
TO_EUR = {
    "EUR": 1.0,
    "DZD": 0.0068,
    "CAD": 0.68,
    "USD": 0.93,
    "GBP": 1.16,
    "CHF": 1.05,
}


def convert_to_eur(price_value, currency):
    c = (currency or "").upper().strip()
    rate = TO_EUR.get(c)
    if rate is None:
        return None
    try:
        return round(float(price_value) * float(rate), 2)
    except Exception:
        return None


def split_route(route):
    r = (route or "").replace("–", "-").replace("—", "-")
    parts = [p.strip() for p in r.split("-") if p.strip()]
    if len(parts) == 2:
        return parts[0], parts[1]
    return r, ""


def run():
    print("Ouverture du site:", URL)

    scraped_at = datetime.now(timezone.utc).isoformat()

    cfg = ScrapeConfig(
        url=URL,
        headless=HEADLESS,
        delay=DELAY,
        max_items=MAX_ITEMS
    )

    with AirAlgerieOffersScraper(cfg) as s:
        raw_texts = s.extract_raw_texts()

    print("Textes récupérés:", len(raw_texts))

    with open(OUT_RAW, "w", encoding="utf-8") as f:
        for t in raw_texts:
            f.write(t + "\n---\n")

    rows = []
    for t in raw_texts:
        item = parse_offer(t)
        if not item:
            continue

        route = str(item.get("route", "")).strip()
        currency = str(item.get("currency", "")).strip().upper()
        price_value = item.get("price_value", None)

        if not route or price_value is None or not currency:
            continue

        price_eur = convert_to_eur(price_value, currency)
        if price_eur is None:
            continue

        dep, arr = split_route(route)

        rows.append({
            "scraped_at": scraped_at,
            "departure": dep,
            "arrival": arr,
            "price_original": float(price_value),
            "currency": currency,
            "price_eur": float(price_eur),
            "source_url": URL
        })

    df = pd.DataFrame(rows).drop_duplicates()

    print("Offres parsées:", int(df.shape[0]))

    if df.empty:
        print("Aucune offre valide (conversion EUR impossible ou parsing vide).")
        return

    df = df.sort_values(by=["price_eur", "departure", "arrival"], ascending=[True, True, True])

    df.to_csv(OUT_CSV, index=False, sep=";", encoding="utf-8-sig")

    best = df.iloc[0].to_dict()
    with open(OUT_BEST, "w", encoding="utf-8") as f:
        json.dump(best, f, ensure_ascii=False, indent=2)

    summary = {
        "scraped_at": scraped_at,
        "source_url": URL,
        "n_raw_texts": len(raw_texts),
        "n_parsed_offers_eur": int(df.shape[0]),
        "best_offer_eur": best,
        "rates_to_eur_used": TO_EUR,
        "files": {
            "csv": OUT_CSV,
            "best_offer": OUT_BEST,
            "raw_texts": OUT_RAW,
            "summary": OUT_SUMMARY
        }
    }

    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("")
    print("Meilleure offre :")
    print("Route :", best["departure"], "->", best["arrival"])
    print("Prix :", f'{best["price_eur"]:.2f}', "EUR")
    print("Prix original :", f'{best["price_original"]:.2f}', best["currency"])
    print("")
    print("Top 5 offres :")
    print(df[["departure", "arrival", "price_eur", "price_original", "currency"]].head(5).to_string(index=False))
    print("")
    print("Fichiers générés :")
    print("CSV:", OUT_CSV)
    print("BEST:", OUT_BEST)
    print("SUMMARY:", OUT_SUMMARY)
    print("RAW:", OUT_RAW)


if __name__ == "__main__":
    run()