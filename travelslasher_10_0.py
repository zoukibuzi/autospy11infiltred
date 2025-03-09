import customtkinter as ctk
import json
from datetime import datetime, timedelta
import os
from scraper import scrape_retailmenot, scrape_dealabs

# Fichiers de cache
CACHE_FILE = "codes_cache.json"
USER_CODES_FILE = "user_codes.json"
CACHE_EXPIRY = timedelta(hours=1)

class TravelSlasherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("TravelSlasher 2025")
        self.geometry("800x600")

        # Thème cyberpunk
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.configure(bg="#000000")

        # Style personnalisé
        self.configure_styles()

        # Logo
        self.logo_label = ctk.CTkLabel(self, text="TRAVELSLASHER 2025", font=("Courier New", 30, "bold"), text_color="#FF0000")
        self.logo_label.pack(pady=20)

        # Slogan
        self.slogan_label = ctk.CTkLabel(self, text="> Codes promo pour voyager malin", font=("Courier New", 14), text_color="#FFFFFF")
        self.slogan_label.pack()

        # Tabview pour les onglets
        self.tabview = ctk.CTkTabview(self, fg_color="#1C1C1C", segmented_button_selected_color="#FF0000", segmented_button_selected_hover_color="#FF3333")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.airline_tab = self.tabview.add("Compagnies Aériennes")
        self.accommodation_tab = self.tabview.add("Plateformes d’Hébergement")

        # Populate initialement
        self.populate_tab("airline", self.airline_tab)
        self.populate_tab("accommodation", self.accommodation_tab)

        # Disclaimer
        disclaimer = ctk.CTkLabel(self, text="> Attention : L’utilisation de codes sans autorisation peut violer les conditions d’utilisation.", font=("Courier New", 12), text_color="#FF0000")
        disclaimer.pack(pady=10)

    def configure_styles(self):
        """Configure les styles pour un look cyberpunk."""
        ctk.CTkLabel(self).configure(font=("Courier New", 14), text_color="#FFFFFF")
        ctk.CTkButton(self).configure(font=("Courier New", 12), fg_color="#000000", border_color="#FF0000", border_width=2, text_color="#FF0000", hover_color="#FF3333")

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

        # Filtrer les codes non fiables
        reliable_codes = [code for code in codes if code.get("reliability", "0").isdigit() and int(code.get("reliability", "0")) > 70]

        # Mise à jour du cache
        cache = {
            "last_update": datetime.now().isoformat(),
            "airline": scrape_retailmenot("airline") + scrape_dealabs("airline"),
            "accommodation": scrape_retailmenot("accommodation") + scrape_dealabs("accommodation")
        }
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)
        return reliable_codes

    def populate_tab(self, category, tab):
        """Remplit un onglet avec les codes."""
        for widget in tab.winfo_children():
            widget.destroy()

        scraped_codes = self.fetch_codes(category)
        user_codes = self.load_user_codes(category)
        all_codes = scraped_codes + user_codes

        if not all_codes:
            no_codes_label = ctk.CTkLabel(tab, text="> Aucun code fiable trouvé.", font=("Courier New", 14), text_color="#FFFFFF")
            no_codes_label.pack(pady=20)
        else:
            for code in all_codes:
                frame = ctk.CTkFrame(tab, fg_color="#1C1C1C")
                frame.pack(fill="x", padx=10, pady=5)
                source = code.get("source", "Utilisateur")
                text = f"> {code['code']} - {code['discount']} ({source})"
                if source == "Utilisateur":
                    text += " (Non vérifié)"
                label = ctk.CTkLabel(frame, text=text, font=("Courier New", 14))
                label.pack(side="left")
                copy_btn = ctk.CTkButton(frame, text="Copier", width=100, command=lambda c=code['code']: self.copy_to_clipboard(c))
                copy_btn.pack(side="right")

        refresh_btn = ctk.CTkButton(tab, text="Rafraîchir", width=150, command=lambda: self.refresh_codes(category, tab))
        refresh_btn.pack(pady=5)
        add_btn = ctk.CTkButton(tab, text="Ajouter un code", width=150, command=lambda: self.add_custom_code_dialog(category, tab))
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
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter un code")
        dialog.geometry("300x200")
        dialog.configure(bg="#000000")

        ctk.CTkLabel(dialog, text="> Code :", font=("Courier New", 14), text_color="#FFFFFF").pack()
        code_entry = ctk.CTkEntry(dialog, font=("Courier New", 12))
        code_entry.pack(pady=5)
        ctk.CTkLabel(dialog, text="> Réduction :", font=("Courier New", 14), text_color="#FFFFFF").pack()
        discount_entry = ctk.CTkEntry(dialog, font=("Courier New", 12))
        discount_entry.pack(pady=5)

        def submit():
            self.add_user_code(category, code_entry.get(), discount_entry.get())
            dialog.destroy()
            self.populate_tab(category, tab)

        ctk.CTkButton(dialog, text="Ajouter", width=100, command=submit).pack(pady=10)

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
