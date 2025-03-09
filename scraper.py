import requests
from bs4 import BeautifulSoup

def scrape_retailmenot(category):
    """Scrape les codes depuis RetailMeNot."""
    url = "https://www.retailmenot.com/view/travel"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        codes = []
        for promo in soup.select(".offer-card"):
            code = promo.select_one(".code").text.strip() if promo.select_one(".code") else "N/A"
            discount = promo.select_one(".description").text.strip()
            reliability = promo.select_one(".success-rate").text.strip() if promo.select_one(".success-rate") else "0"
            if (category == "airline" and "flight" in discount.lower()) or (category == "accommodation" and "hotel" in discount.lower()):
                if reliability.isdigit() and int(reliability) > 70:  # Seulement codes fiables
                    codes.append({"code": code, "discount": discount, "reliability": reliability, "source": "RetailMeNot"})
        return codes
    except Exception as e:
        print(f"[DAN] Erreur scraping RetailMeNot : {e}")
        return []

def scrape_dealabs(category):
    """Scrape les codes depuis Dealabs."""
    search_term = "airline promo code" if category == "airline" else "hotel promo code"
    url = f"https://www.dealabs.com/search?q={search_term.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        codes = []
        for deal in soup.select(".thread"):
            title = deal.select_one(".thread-title").text.strip()
            if "code" in title.lower():
                code = title.split()[-1]
                discount = "Réduction inconnue"
                reliability = deal.select_one(".vote-temp").text.strip() if deal.select_one(".vote-temp") else "0"
                if reliability.isdigit() and int(reliability) > 50:  # Seulement codes fiables
                    codes.append({"code": code, "discount": discount, "reliability": reliability, "source": "Dealabs"})
        return codes
    except Exception as e:
        print(f"[DAN] Erreur scraping Dealabs : {e}")
        return []
