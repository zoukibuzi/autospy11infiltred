import asyncio
import aiohttp
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from concurrent.futures import ThreadPoolExecutor
import logging
import anticaptchaofficial.recaptchav2proxyless
import torpy.http.requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import unittest

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='travelslasher.log')

# Liste des 50+1 plateformes
PLATFORMS = {
    "Booking.com": "https://www.booking.com",
    "Expedia": "https://www.expedia.com",
    "Hotels.com": "https://www.hotels.com",
    "Agoda": "https://www.agoda.com",
    "Trip.com": "https://www.trip.com",
    "Kayak": "https://www.kayak.com",
    "Lastminute.com": "https://www.lastminute.com",
    "Trivago": "https://www.trivago.com",
    "Hostelworld": "https://www.hostelworld.com",
    "Priceline": "https://www.priceline.com",
    "Orbitz": "https://www.orbitz.com",
    "Travelocity": "https://www.travelocity.com",
    "Hotwire": "https://www.hotwire.com",
    "CheapTickets": "https://www.cheaptickets.com",
    "HotelTonight": "https://www.hoteltonight.com",
    "AccorHotels": "https://all.accor.com",
    "Marriott": "https://www.marriott.com",
    "Hilton": "https://www.hilton.com",
    "IHG": "https://www.ihg.com",
    "Wyndham": "https://www.wyndhamhotels.com",
    "Choice Hotels": "https://www.choicehotels.com",
    "Best Western": "https://www.bestwestern.com",
    "Radisson": "https://www.radissonhotels.com",
    "Hyatt": "https://www.hyatt.com",
    "Vrbo": "https://www.vrbo.com",
    "HomeAway": "https://www.homeaway.com",
    "Tripadvisor": "https://www.tripadvisor.com",
    "Skyscanner": "https://www.skyscanner.com",
    "Opodo": "https://www.opodo.com",
    "eDreams": "https://www.edreams.com",
    "Ctrip": "https://www.ctrip.com",
    "MakeMyTrip": "https://www.makemytrip.com",
    "Yatra": "https://www.yatra.com",
    "Goibibo": "https://www.goibibo.com",
    "Cleartrip": "https://www.cleartrip.com",
    "Travelzoo": "https://www.travelzoo.com",
    "Hotelbeds": "https://www.hotelbeds.com",
    "HRS": "https://www.hrs.com",
    "RoomKey": "https://www.roomkey.com",
    "ZenHotels": "https://www.zenhotels.com",
    "Snaptravel": "https://www.snaptravel.com",
    "Stayz": "https://www.stayz.com.au",
    "Wotif": "https://www.wotif.com",
    "Laterooms": "https://www.laterooms.com",
    "Ostrovok": "https://www.ostrovok.ru",
    "Despegar": "https://www.despegar.com",
    "Hotel Urbano": "https://www.hotelurbano.com",
    "Logitravel": "https://www.logitravel.com",
    "HotelsCombined": "https://www.hotelscombined.com",
    "Airbnb": "https://www.airbnb.com"
}

# Sources légales et illégales
LEGAL_SOURCES = ["https://www.dealabs.com", "https://www.retailmenot.com", "https://www.honey.com"]
ILLEGAL_SOURCES = ["http://darkwebforum.onion", "telegram://leaks", "pastebin.com"]

# IA avancée
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
nlp = pipeline("text-classification", model=model, tokenizer=tokenizer)

def bypass_captcha(driver, site_key, url):
    solver = anticaptchaofficial.recaptchav2proxyless()
    solver.set_key("YOUR_ANTI_CAPTCHA_API_KEY")  # Remplace par ta clé
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    g_response = solver.solve_and_return_solution()
    if g_response:
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{g_response}";')
        return True
    logging.error("Échec CAPTCHA Anti-Captcha, essai 2Captcha...")
    # Ajout 2Captcha si besoin (optionnel)
    return False

def setup_driver():
    options = Options()
    options.headless = False  # Live visualisation
    options.add_argument("--proxy-server=socks5://127.0.0.1:9050")  # Tor proxy
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

async def scrape_legal_source(source, session):
    try:
        async with session.get(source, timeout=10) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            codes = [elem.text for elem in soup.select(".promo-code")]
            return codes[:10]  # Limite à 10 par source
    except Exception as e:
        logging.error(f"Erreur scraping légal {source} : {e}")
        return []

async def scrape_illegal_source(source):
    try:
        with torpy.http.requests.tor_requests_session() as session:
            response = session.get(source)
            soup = BeautifulSoup(response.text, "html.parser")
            codes = [elem.text for elem in soup.select(".leak-code")]
            return codes[:10]
    except Exception as e:
        logging.error(f"Erreur scraping illégal {source} : {e}")
        return []

async def gather_codes():
    codes = set(PROMO_CODES)
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_legal_source(source, session) for source in LEGAL_SOURCES] + \
                [scrape_illegal_source(source) for source in ILLEGAL_SOURCES]
        results = await asyncio.gather(*tasks)
        for result in results:
            codes.update(result)
    return list(codes)[:1000]  # Limite à 1000 pour perf

def scrape_base_price(url, driver):
    driver.get(url)
    time.sleep(3)
    try:
        price_elem = driver.find_element(By.CLASS_NAME, "price")
        price = float(price_elem.text.replace("€", "").replace(",", "").strip())
        logging.info(f"Prix brut {url} : {price:.2f} €")
        return price
    except:
        return 600

def test_promo_code(driver, url, base_price, code):
    driver.get(url)
    time.sleep(2)
    try:
        promo_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "promo-code"))  # À adapter
        )
        promo_field.send_keys(code)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()
        time.sleep(3)
        
        if "g-recaptcha" in driver.page_source:
            site_key = driver.find_element(By.CLASS_NAME, "g-recaptcha").get_attribute("data-sitekey")
            bypass_captcha(driver, site_key, url)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Apply')]").click()
            time.sleep(3)
        
        new_price_elem = driver.find_element(By.CLASS_NAME, "price")
        new_price = float(new_price_elem.text.replace("€", "").replace(",", "").strip())
        if new_price < base_price:
            return new_price, True
        return base_price, False
    except Exception as e:
        logging.error(f"Erreur test code {code} : {e}")
        return base_price, False

def analyze_discount(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    score = torch.softmax(outputs.logits, dim=1)[0][1].item()
    return score * 100  # % réduction estimé

class ScraperUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TravelSlasher 10.0 - Live Scraping")
        self.tree = ttk.Treeview(self.root, columns=("Platform", "Price", "Code", "Discount"), show="headings")
        self.tree.heading("Platform", text="Plateforme")
        self.tree.heading("Price", text="Prix Réduit (€)")
        self.tree.heading("Code", text="Code Promo")
        self.tree.heading("Discount", text="Réduction (%)")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.start_button = tk.Button(self.root, text="Lancer Scraping", command=self.start_scraping)
        self.start_button.pack(pady=10)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.discounts = []

    def update_ui(self, platform, price, code, discount):
        self.tree.insert("", "end", values=(platform, f"{price:.2f}", code, f"{discount:.1f}"))
        self.discounts.append(discount)
        self.ax.clear()
        self.ax.plot(self.discounts, label="Réductions (%)")
        self.ax.legend()
        self.canvas.draw()

    def start_scraping(self):
        threading.Thread(target=lambda: asyncio.run(run_checker(self)), daemon=True).start()

    def on_closing(self):
        with open("results.json", "w") as f:
            json.dump({"discounts": self.discounts}, f)
        self.root.quit()
        self.root.destroy()

async def check_codes(platform, url, codes, ui):
    driver = setup_driver()
    base_price = scrape_base_price(url, driver)
    best_price = base_price
    best_code = None
    best_discount = 0
    
    ui.update_ui(platform, base_price, "N/A", 0)
    for code in random.sample(codes, min(50, len(codes))):  # Test 50 codes max par plateforme
        new_price, valid = test_promo_code(driver, url, base_price, code)
        if valid and new_price < best_price:
            best_price = new_price
            best_code = code
            discount = (base_price - new_price) / base_price * 100
            best_discount = discount
            ui.update_ui(platform, best_price, best_code, best_discount)
            logging.info(f"Meilleure réduction trouvée : {platform} - {best_code} ({discount:.1f}%)")
        time.sleep(1)
    
    driver.quit()
    return {"price": best_price, "code": best_code or "Aucun code valide", "discount": best_discount, "url": url}

async def run_checker(ui):
    codes = await gather_codes()
    results = {}
    with ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        tasks = [loop.run_in_executor(executor, lambda p=p, u=u: asyncio.run(check_codes(p, u, codes, ui))) for p, u in PLATFORMS.items()]
        results_list = await asyncio.gather(*tasks)
        results = {p: r for p, r in zip(PLATFORMS.keys(), results_list)}
    
    display_results(results)

def display_results(results):
    logging.info("TravelSlasher 10.0 - Classement Final")
    sorted_results = sorted(results.items(), key=lambda x: x[1]["discount"], reverse=True)
    for platform, data in sorted_results:
        print(f"{platform} : Prix Réduit : {data['price']:.2f} € | Code : {data['code']} | Réduction : {data['discount']:.1f}% | Site : {data['url']}")

class TestTravelSlasher(unittest.TestCase):
    def test_scrape_base_price(self):
        driver = setup_driver()
        price = scrape_base_price("https://www.booking.com", driver)
        driver.quit()
        self.assertTrue(isinstance(price, float))

if __name__ == "__main__":
    ui = ScraperUI()
    ui.root.mainloop()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)