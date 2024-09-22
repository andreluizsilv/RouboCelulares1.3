// Inicializa o mapa
var map = L.map('map').setView([-23.5505, -46.6333], 12); // Coordenadas do centro do mapa

// Adiciona a camada de tile do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Dados dos bairros (recebidos do servidor)
var bairros = {{ bairros_json|safe }};  // Usando o JSON gerado no Django

// Adiciona marcadores para cada bairro
bairros.forEach(function(bairro) {
    L.marker([bairro.latitude, bairro.longitude])
        .addTo(map)
        .bindPopup('<b>' + bairro.bairro + '</b><br>Número de Ocorrências: ' + bairro.num_ocorrencias)
        .on('click', function() {
            window.location.href = "/detalhes/" + bairro.id + "/";
        });
});
