const bairros = JSON.parse(document.getElementById('bairros-data').textContent);

var map = L.map('map').setView([-23.5505, -46.6333], 12);

// Adiciona a camada do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Adiciona marcadores no mapa
bairros.forEach(function(bairro) {
    if (bairro.latitude !== 0.0 && bairro.longitude !== 0.0) {
        L.marker([bairro.latitude, bairro.longitude])
            .addTo(map)
            .bindPopup('<b>' + bairro.bairro + '</b><br>Número de Ocorrências: ' + bairro.num_ocorrencias)
            .on('click', function() {
                window.location.href = "/detalhes/" + bairro.id + "/";
            });
    } else {
        console.warn("Bairro sem coordenadas válidas: " + bairro.bairro);
    }
});
