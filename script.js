// Liste des 13 compagnies aériennes + 51 sites de réservation (14 ici pour simuler, extensible à 64)
const PLATFORMS = {
    // Compagnies aériennes
    "Air France": "https://www.airfrance.fr",
    "easyJet": "https://www.easyjet.com/fr",
    "Ryanair": "https://www.ryanair.com/fr",
    "Transavia France": "https://www.transavia.com/fr-FR",
    "Vueling Airlines": "https://www.vueling.com/fr",
    "Lufthansa": "https://www.lufthansa.com/fr/fr",
    "British Airways": "https://www.britishairways.com/fr-fr",
    "Iberia": "https://www.iberia.com/fr",
    "Volotea": "https://www.volotea.com",
    "Air Corsica": "https://www.aircorsica.com",
    "KLM": "https://www.klm.fr",
    "Wizz Air": "https://wizzair.com/fr-fr",
    "TAP Air Portugal": "https://www.flytap.com/fr-fr",
    "Eurowings": "https://www.eurowings.com/fr",
    "French Bee": "https://www.frenchbee.com/fr",
    // Sites de réservation (5 ici pour simuler, extensible à 51)
    "Booking.com": "https://www.booking.com",
    "Airbnb": "https://www.airbnb.com",
    "Expedia": "https://www.expedia.com",
    "Hotels.com": "https://www.hotels.com",
    "Agoda": "https://www.agoda.com"
};

// Liste de codes promo avec conditions
const PROMO_CODES = [
    { code: "AFWELCOME", condition: "Nouveau client, vols long-courrier" },
    { code: "EASY20", condition: "Réservation avant 31/03/2025" },
    { code: "RYAN15", condition: "Vols low-cost, siège prioritaire requis" },
    { code: "TRANS10", condition: "Vols européens seulement" },
    { code: "VUEL20", condition: "Membre Vueling Club" },
    { code: "LH5OFF", condition: "Connexion via Frankfurt" },
    { code: "BA10SAVE", condition: "Vol Paris-Londres uniquement" },
    { code: "IBERIA15", condition: "Vols vers l’Espagne" },
    { code: "VOLOTEA5", condition: "Routes régionales françaises" },
    { code: "AIRCORSICA10", condition: "Liaisons Corse-continent" },
    { code: "KLM25", condition: "Partenaires Air France" },
    { code: "WIZZ30", condition: "Paiement en ligne uniquement" },
    { code: "TAP20", condition: "Vol vers Portugal" },
    { code: "EUROWINGS15", condition: "Vols courts-courriers" },
    { code: "FRENCHBEE25", condition: "Long-courrier DOM-TOM/USA" },
    { code: "GENIUS20", condition: "Membre Booking Genius Niveau 2" },
    { code: "REFER25", condition: "Nouveau client, parrainage requis" },
    { code: "SAVE10", condition: "Réservation avant 31/03/2025" },
    { code: "TRAVEL20", condition: "Séjour de 3+ nuits" },
    { code: "HOTEL15", condition: "Hôtels sélectionnés seulement" }
];

let chart;

function simulateScrape(url) {
    const basePrice = 600 + Math.random() * 100 - 50; // Entre 550 et 650 € (réaliste pour vols/hôtels 2025)
    console.log(`[DAN] Scraping ${url}... Prix brut : ${basePrice.toFixed(2)} €`);
    return basePrice;
}

function simulateTestCode(basePrice, code) {
    const promo = PROMO_CODES.find(p => p.code === code);
    const discount = {
        "AFWELCOME": 0.9, "EASY20": 0.8, "RYAN15": 0.85, "TRANS10": 0.9, "VUEL20": 0.8,
        "LH5OFF": 0.95, "BA10SAVE": 0.9, "IBERIA15": 0.85, "VOLOTEA5": 0.95, "AIRCORSICA10": 0.9,
        "KLM25": 0.75, "WIZZ30": 0.7, "TAP20": 0.8, "EUROWINGS15": 0.85, "FRENCHBEE25": 0.75,
        "GENIUS20": 0.8, "REFER25": 0.9, "SAVE10": 0.9, "TRAVEL20": 0.8, "HOTEL15": 0.85
    }[code] || (Math.random() * 0.2 + 0.7); // 10-30% par défaut
    const newPrice = basePrice * discount;
    const valid = newPrice < basePrice && Math.random() > 0.2; // 80% chance de succès
    console.log(`[DAN] Test code ${code} : Nouveau prix : ${newPrice.toFixed(2)} €${valid ? " (valide)" : ""}`);
    return { newPrice, valid, condition: promo ? promo.condition : "Aucune condition" };
}

function startSimulation() {
    const tbody = document.querySelector("#resultsTable tbody");
    tbody.innerHTML = "";
    const discounts = [];
    let index = 0;

    chart = new Chart(document.getElementById("discountChart"), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Réductions (%)',
                data: [],
                borderColor: '#007bff',
                fill: false
            }]
        },
        options: { scales: { y: { beginAtZero: true, max: 50 } } }
    });

    Object.entries(PLATFORMS).forEach(([platform, url], idx) => {
        setTimeout(() => {
            const basePrice = simulateScrape(url);
            let bestPrice = basePrice;
            let bestCode = "Aucun code valide";
            let bestDiscount = 0;
            let bestCondition = "Aucune condition";

            PROMO_CODES.forEach(promo => {
                const { newPrice, valid, condition } = simulateTestCode(basePrice, promo.code);
                if (valid && newPrice < bestPrice) {
                    bestPrice = newPrice;
                    bestCode = promo.code;
                    bestDiscount = (basePrice - bestPrice) / basePrice * 100;
                    bestCondition = condition;
                }
            });

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${platform}</td>
                <td>${bestPrice.toFixed(2)}</td>
                <td>${bestCode}</td>
                <td>${bestDiscount.toFixed(1)}</td>
                <td>${bestCondition}</td>
            `;
            tbody.appendChild(row);

            discounts.push(bestDiscount);
            chart.data.labels.push(index++);
            chart.data.datasets[0].data = discounts;
            chart.update();

            if (idx === Object.keys(PLATFORMS).length - 1) {
                setTimeout(displayFinalResults, 1000);
            }
        }, idx * 1000); // 1s par plateforme pour une simulation rapide
    });
}

function displayFinalResults() {
    const tbody = document.querySelector("#resultsTable tbody");
    const rows = Array.from(tbody.getElementsByTagName("tr"));
    rows.sort((a, b) => parseFloat(b.cells[3].textContent) - parseFloat(a.cells[3].textContent));
    tbody.innerHTML = "";
    rows.forEach(row => tbody.appendChild(row));
    console.log("[DAN] Simulation terminée ! Classement final affiché.");
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
}
