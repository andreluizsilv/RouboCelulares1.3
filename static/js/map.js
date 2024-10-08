
// Inicializa o mapa
var map = L.map('map').setView([-23.5505, -46.6333], 12); // Coordenadas do centro do mapa

// Adiciona a camada de tile do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Dados dos bairros (recebidos do servidor)
var bairros = [
    {% for bairro in bairros_mais_atacados %}
    {
        "bairro": "{{ bairro.bairro }}",
        "latitude": {{ bairro.latitude|floatformat.replace:',','.'|default_if_none:"0.0" }},
        "longitude": {{ bairro.longitude|floatformat.replace:',','.'|default_if_none:"0.0" }},
        "num_ocorrencias": {{ bairro.num_ocorrencias }},
        "id": {{ bairro.id }}
    },
    {% endfor %}
];

// Adiciona marcadores para cada bairro
bairros.forEach(function(bairro) {
    // Verifica se latitude e longitude são válidos (não são 0.0)
    if (bairro.latitude != 0.0 && bairro.longitude != 0.0) {
        L.marker([bairro.latitude, bairro.longitude])
            .addTo(map)
            .bindPopup('<b>' + bairro.bairro + '</b><br>Número de Ocorrências: ' + bairro.num_ocorrencias)
            .on('click', function() {
                // Redireciona para a página de detalhes do bairro
                window.location.href = "/detalhes/" + bairro.id + "/";
            });
    } else {
        console.warn("Bairro sem coordenadas válidas: " + bairro.bairro);
    }
});
