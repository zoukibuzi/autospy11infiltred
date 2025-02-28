// Liste des 50+1 plateformes (5 ici pour simulation, extensible à 51)
const PLATFORMS = {
    "Booking.com": "https://www.booking.com",
    "Airbnb": "https://www.airbnb.com",
    "Expedia": "https://www.expedia.com",
    "Hotels.com": "https://www.hotels.com",
    "Agoda": "https://www.agoda.com"
};

// Liste de codes promo corrigée
const PROMO_CODES = [
    "GENIUS20", "REFER25", "SAVE10", "TRAVEL20", "HOTEL15",
    "EXP10", "AGODA20", "BOOK25", "STAY30", "DEAL15",
    "FLY20", "SAVE15", "TRIP25", "HOTDEAL", "CODE10"
];

let chart;

function simulateScrape(url) {
    const basePrice = 600 + Math.random() * 50 - 25; // Entre 575 et 625 €
    console.log(`[DAN] Scraping ${url}... Prix brut : ${basePrice.toFixed(2)} €`);
    return basePrice;
}

function simulateTestCode(basePrice, code) {
    const discount = code === "GENIUS20" ? 0.8 : (Math.random() * 0.2 + 0.7); // 20% pour GENIUS20, sinon 10-30%
    const newPrice = basePrice * discount;
    const valid = newPrice < basePrice && Math.random() > 0.3; // 70% chance de succès
    console.log(`[DAN] Test code ${code} : Nouveau prix : ${newPrice.toFixed(2)} €${valid ? " (valide)" : ""}`);
    return { newPrice, valid };
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

            PROMO_CODES.forEach(code => {
                const { newPrice, valid } = simulateTestCode(basePrice, code);
                if (valid && newPrice < bestPrice) {
                    bestPrice = newPrice;
                    bestCode = code;
                    bestDiscount = (basePrice - bestPrice) / basePrice * 100;
                }
            });

            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${platform}</td>
                <td>${bestPrice.toFixed(2)}</td>
                <td>${bestCode}</td>
                <td>${bestDiscount.toFixed(1)}</td>
            `;
            tbody.appendChild(row);

            discounts.push(bestDiscount);
            chart.data.labels.push(index++);
            chart.data.datasets[0].data = discounts;
            chart.update();

            if (idx === Object.keys(PLATFORMS).length - 1) {
                setTimeout(displayFinalResults, 1000);
            }
        }, idx * 1500);
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