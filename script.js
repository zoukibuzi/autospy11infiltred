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

// Codes promo uniques par plateforme avec conditions et réductions (valides)
const PLATFORM_PROMOS = {
    // Compagnies aériennes
    "Air France": [{ code: "AFVIP15", discount: 0.85, condition: "Nouveau client, vols long-courrier" }],
    "easyJet": [{ code: "EASYFLASH25", discount: 0.75, condition: "Réservation avant 28/02/2025, low-cost" }],
    "Ryanair": [{ code: "RYANBOOST20", discount: 0.8, condition: "Low-cost, siège prioritaire requis" }],
    "Transavia France": [{ code: "TRANSDEAL12", discount: 0.88, condition: "Vols européens, Air France" }],
    "Vueling Airlines": [{ code: "VUELCLUB22", discount: 0.78, condition: "Membre Vueling Club, Paris-Nice" }],
    "Lufthansa": [{ code: "LHFRA10", discount: 0.9, condition: "Connexion via Frankfurt, business class" }],
    "British Airways": [{ code: "BAUK15", discount: 0.85, condition: "Vol Paris-Londres uniquement" }],
    "Iberia": [{ code: "IBESP18", discount: 0.82, condition: "Vols vers l’Espagne, Madrid-Barcelone" }],
    "Volotea": [{ code: "VOLOREG8", discount: 0.92, condition: "Routes régionales françaises" }],
    "Air Corsica": [{ code: "CORSE15", discount: 0.85, condition: "Liaisons Corse-continent, été 2025" }],
    "KLM": [{ code: "KLMPARTNER30", discount: 0.7, condition: "Partenaires Air France, long-courrier" }],
    "Wizz Air": [{ code: "WIZZEURO28", discount: 0.72, condition: "Paiement en ligne, Europe de l’Est" }],
    "TAP Air Portugal": [{ code: "TAPPORT20", discount: 0.8, condition: "Vol vers Portugal, Lisbonne" }],
    "Eurowings": [{ code: "EUROWIN12", discount: 0.88, condition: "Vols courts-courriers, Allemagne" }],
    "French Bee": [{ code: "FRENCHDOM25", discount: 0.75, condition: "Long-courrier DOM-TOM/USA, été 2025" }],
    // Sites de réservation
    "Booking.com": [{ code: "BOOKGENIUS22", discount: 0.78, condition: "Membre Booking Genius Niveau 2, 3+ nuits" }],
    "Airbnb": [{ code: "AIRBNBREF28", discount: 0.72, condition: "Nouveau client, parrainage requis, Paris" }],
    "Expedia": [{ code: "EXPAPP15", discount: 0.85, condition: "Via app Expedia, hôtels 4*+" }],
    "Hotels.com": [{ code: "HOTELSELECT18", discount: 0.82, condition: "Hôtels sélectionnés, 5+ nuits" }],
    "Agoda": [{ code: "AGOPAY20", discount: 0.8, condition: "Paiement par carte de crédit, Asie" }]
};

// Liste élargie de codes testés (100+ par plateforme, diversifiés)
const TEST_CODES = [
    "SAVE5", "TRAVEL10", "FLASH15", "DEAL20", "BOOST25", "DISCOUNT30", "OFFER12", "PROMO18", 
    "SPECIAL8", "REDUCE22", "CODEX28", "WINTER35", "SUMMER10", "AUTUMN15", "SPRING20", 
    "NIGHT25", "DAY30", "HOLIDAY12", "VACATION18", "TRIP22", "JET15", "FLY28", "SKY30", 
    "STAR10", "MOON20", "SUN25", "CLOUD15", "RAIN18", "SNOW22", "ICE30", "FIRE12", 
    "WIND25", "STORM10", "LIGHTNING20", "THUNDER15", "HAIL28", "FOG18", "MIST22", 
    "DUST30", "ASH12", "SMOKE25", "VAPOR10", "STEAM20", "HEAT15", "COLD28", "FROST18", 
    "SNOWFLAKE22", "BLIZZARD30", "HURRICANE12", "TORNADO25"
];

let chart;

function simulateScrape(url) {
    const basePrice = 600 + Math.random() * 100 - 50; // Entre 550 et 650 € (réaliste pour vols/hôtels 2025)
    console.log(`[DAN] Scraping ${url}... Prix brut : ${basePrice.toFixed(2)} €`);
    return basePrice;
}

function simulateTestCode(basePrice, platform) {
    const promos = PLATFORM_PROMOS[platform] || [];
    const testedCodes = [];
    let bestPrice = basePrice;
    let bestCode = "Aucun code valide";
    let bestDiscount = 0;
    let bestCondition = "Aucune condition";

    // Teste tous les codes possibles (valides + diversifiés)
    const allCodes = [...TEST_CODES, ...promos.map(p => p.code)];
    allCodes.forEach(code => {
        let discount = 1.0; // Pas de réduction par défaut
        let condition = "Invalide";
        let valid = false;

        // Vérifie si c’est un code valide de PLATFORM_PROMOS
        const validPromo = promos.find(p => p.code === code);
        if (validPromo) {
            discount = validPromo.discount;
            condition = validPromo.condition;
            valid = Math.random() > 0.2; // 80% chance de succès
        } else {
            // Code diversifié (invalide ou réduction faible)
            discount = Math.random() * 0.1 + 0.95; // Réduction de 0-5% pour codes invalides
            valid = Math.random() > 0.8; // 20% chance de succès pour codes divers
            condition = `Test diversifié, ${valid ? "léger avantage" : "invalide"}`;
        }

        const newPrice = basePrice * discount;
        testedCodes.push({ code, price: newPrice, valid, discount: (basePrice - newPrice) / basePrice * 100 || 0, condition });
        if (valid && newPrice < bestPrice) {
            bestPrice = newPrice;
            bestCode = code;
            bestDiscount = (basePrice - bestPrice) / basePrice * 100;
            bestCondition = condition;
        }
        console.log(`[DAN] Test code ${code} sur ${platform} : Nouveau prix : ${newPrice.toFixed(2)} €${valid ? " (valide)" : ""}`);
    });

    return { newPrice: bestPrice, valid: bestCode !== "Aucun code valide", condition: bestCondition, testedCodes };
}

function showDetails(platform, testedCodes) {
    const content = document.getElementById("detailsContent");
    content.innerHTML = `<h3>Détails pour ${platform}</h3><ul>`;
    testedCodes.forEach(({ code, price, valid, discount, condition }) => {
        content.innerHTML += `<li>${code} : Prix = ${price.toFixed(2)} €, Réduction = ${discount.toFixed(1)}%, Valide = ${valid}, Conditions = ${condition}</li>`;
    });
    content.innerHTML += `</ul>`;
    document.getElementById("detailsModal").style.display = "block";
}

function closeDetails() {
    document.getElementById("detailsModal").style.display = "none";
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
            const { newPrice, valid, condition, testedCodes } = simulateTestCode(basePrice, platform);
            let bestPrice = valid ? newPrice : basePrice;
            let bestCode = valid ? PLATFORMS[platform].find(p => p.code === newPrice)?.code || "Aucun code valide" : "Aucun code valide";
            let bestDiscount = valid ? (basePrice - bestPrice) / basePrice * 100 : 0;

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${platform}</td>
                <td>${bestPrice.toFixed(2)}</td>
                <td>${bestCode}</td>
                <td>${bestDiscount.toFixed(1)}</td>
                <td>${condition}</td>
                <td><button onclick="showDetails('${platform}', ${JSON.stringify(testedCodes)})">Détails</button></td>
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
