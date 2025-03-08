import requests
from bs4 import BeautifulSoup

def scrape_retailmenot(category):
    """Scrape les codes depuis RetailMeNot."""
    url = "https://www.retailmenot.com/view/travel"  # À ajuster selon la catégorie
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        codes = []
        for promo in soup.select(".offer-card"):  # Sélecteurs hypothétiques
            code = promo.select_one(".code").text.strip() if promo.select_one(".code") else "N/A"
            discount = promo.select_one(".description").text.strip()
            reliability = promo.select_one(".success-rate").text.strip() if promo.select_one(".success-rate") else "Inconnu"
            if (category == "airline" and "flight" in discount.lower()) or (category == "accommodation" and "hotel" in discount.lower()):
                codes.append({"code": code, "discount": discount, "reliability": reliability, "source": "RetailMeNot"})
        return codes
    except Exception:
        return []

def scrape_dealabs(category):
    """Scrape les codes depuis Dealabs."""
    search_term = "airline promo code" if category == "airline" else "hotel promo code"
    url = f"https://www.dealabs.com/search?q={search_term.replace(' ', '+')}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        codes = []
        for deal in soup.select(".thread"):  # Sélecteurs hypothétiques
            title = deal.select_one(".thread-title").text.strip()
            if "code" in title.lower():
                code = title.split()[-1]  # Approximation
                discount = "Réduction inconnue"  # À améliorer
                reliability = deal.select_one(".vote-temp").text.strip() if deal.select_one(".vote-temp") else "0"
                codes.append({"code": code, "discount": discount, "reliability": reliability, "source": "Dealabs"})
        return codes
    except Exception:
        return []
