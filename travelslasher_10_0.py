import customtkinter
import json
from datetime import datetime, timedelta
import os
from scraper import scrape_retailmenot, scrape_dealabs  # Module séparé pour le scraping

# Fichiers de cache
CACHE_FILE = "codes_cache.json"
USER_CODES_FILE = "user_codes.json"
CACHE_EXPIRY = timedelta(hours=1)

class TravelSlasherApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("TravelSlasher 2025")
        self.geometry("800x600")
        
        # Thème moderne
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # Tabview pour les onglets
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        self.airline_tab = self.tabview.add("Compagnies Aériennes")
        self.accommodation_tab = self.tabview.add("Plateformes d’Hébergement")

        # Populate initialement
        self.populate_tab("airline", self.airline_tab)
        self.populate_tab("accommodation", self.accommodation_tab)

        # Disclaimer
        disclaimer = customtkinter.CTkLabel(self, text="Attention : L’utilisation de codes sans autorisation peut violer les conditions d’utilisation.", text_color="red")
        disclaimer.pack(pady=10)

    def fetch_codes(self, category, force_refresh=False):
        """Récupère les codes, avec cache pour éviter les requêtes inutiles."""
        if not force_refresh:
            try:
                with open(CACHE_FILE, "r") as f:
                    cache = json.load(f)
                    last_update = datetime.fromisoformat(cache["last_update"])
                    if datetime.now() - last_update < CACHE_EXPIRY:
                        return cache.get(category, [])
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                pass

        # Scraping
        codes = []
        codes.extend(scrape_retailmenot(category))
        codes.extend(scrape_dealabs(category))

        # Mise à jour du cache
        cache = {
            "last_update": datetime.now().isoformat(),
            "airline": scrape_retailmenot("airline") + scrape_dealabs("airline"),
            "accommodation": scrape_retailmenot("accommodation") + scrape_dealabs("accommodation")
        }
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)
        return codes

    def populate_tab(self, category, tab):
        """Remplit un onglet avec les codes."""
        for widget in tab.winfo_children():
            widget.destroy()

        scraped_codes = self.fetch_codes(category)
        user_codes = self.load_user_codes(category)
        all_codes = scraped_codes + user_codes

        for code in all_codes:
            frame = customtkinter.CTkFrame(tab)
            frame.pack(fill="x", padx=10, pady=5)
            source = code.get("source", "Utilisateur")
            text = f"{code['code']} - {code['discount']} ({source})"
            if source == "Utilisateur":
                text += " (Non vérifié)"
            label = customtkinter.CTkLabel(frame, text=text)
            label.pack(side="left")
            copy_btn = customtkinter.CTkButton(frame, text="Copier", command=lambda c=code['code']: self.copy_to_clipboard(c))
            copy_btn.pack(side="right")

        refresh_btn = customtkinter.CTkButton(tab, text="Rafraîchir", command=lambda: self.refresh_codes(category, tab))
        refresh_btn.pack(pady=5)
        add_btn = customtkinter.CTkButton(tab, text="Ajouter un code", command=lambda: self.add_custom_code_dialog(category, tab))
        add_btn.pack(pady=5)

    def copy_to_clipboard(self, text):
        import pyperclip
        pyperclip.copy(text)

    def load_user_codes(self, category):
        """Charge les codes ajoutés par l’utilisateur."""
        try:
            with open(USER_CODES_FILE, "r") as f:
                return json.load(f).get(category, [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_custom_code_dialog(self, category, tab):
        """Ouvre une fenêtre pour ajouter un code personnalisé."""
        dialog = customtkinter.CTkToplevel(self)
        dialog.title("Ajouter un code")
        dialog.geometry("300x200")

        customtkinter.CTkLabel(dialog, text="Code :").pack()
        code_entry = customtkinter.CTkEntry(dialog)
        code_entry.pack()
        customtkinter.CTkLabel(dialog, text="Réduction :").pack()
        discount_entry = customtkinter.CTkEntry(dialog)
        discount_entry.pack()

        def submit():
            self.add_user_code(category, code_entry.get(), discount_entry.get())
            dialog.destroy()
            self.populate_tab(category, tab)

        customtkinter.CTkButton(dialog, text="Ajouter", command=submit).pack(pady=10)

    def add_user_code(self, category, code, discount):
        """Ajoute un code utilisateur."""
        try:
            with open(USER_CODES_FILE, "r") as f:
                user_codes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            user_codes = {"airline": [], "accommodation": []}

        category_codes = user_codes.get(category, [])
        category_codes.append({"code": code, "discount": discount, "source": "Utilisateur"})
        user_codes[category] = category_codes
        with open(USER_CODES_FILE, "w") as f:
            json.dump(user_codes, f)

    def refresh_codes(self, category, tab):
        """Force le rafraîchissement des codes."""
        self.fetch_codes(category, force_refresh=True)
        self.populate_tab(category, tab)

if __name__ == "__main__":
    app = TravelSlasherApp()
    app.mainloop()
